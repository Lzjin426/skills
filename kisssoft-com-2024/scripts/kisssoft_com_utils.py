"""
KISSsoft 2024 COM 自动化工具函数

用法：
    import kisssoft_com_utils as kc
    ks = kc.connect()
    kc.load_module_and_file(ks, "Z012", r"C:\\path\\to\\file.Z12")
    kc.calculate(ks)
    print(kc.get_var(ks, "ZPP[0].Fuss.SFnorm"))
"""
import os
import json
import win32com.client

PROGID = "KISSsoftCOM2024.KISSsoft"

# 当前 license 下 CheckLicense 返回 True 的模块
# 实际可加载并计算的 24 个：S020 加载失败，K019 CalculateRetVal 返回 False
LICENSED_MODULES = {
    "Z011", "Z012", "Z013", "Z014", "Z015", "Z016",
    "Z050", "Z060", "Z070", "Z080", "Z090",
    "W010", "M010", "M040", "M050", "M060",
    "F010", "F020", "F030", "F040", "F050",
    "A010", "A020", "K010",
}

# 模块 ID 与文件扩展名的映射（示例）
MODULE_EXTENSIONS = {
    "Z011": ".Z11", "Z012": ".Z12", "Z013": ".Z13",
    "Z014": ".Z14", "Z015": ".Z15", "Z016": ".Z16",
    "Z050": ".Z50", "Z060": ".Z60", "Z070": ".Z70",
    "Z080": ".Z80", "Z090": ".Z90",
    "W010": ".W10", "S020": ".S20",
    "M010": ".M10", "M040": ".M40", "M050": ".M50", "M060": ".M60",
    "F010": ".F10", "F020": ".F20", "F030": ".F30", "F040": ".F40", "F050": ".F50",
    "A010": ".A10", "A020": ".A20",
    "K010": ".K10", "K019": ".K19",
}

# 常用结果变量（按模块）
COMMON_RESULT_VARS = {
    "Z011": ["ZR[0].da.nul", "ZR[0].df.nul", "ZR[0].d", "ZR[0].Vqual", "ZR[0].runOut.brtotI"],
    "Z012": ["ZPP[0].Fuss.SFnorm", "ZPP[0].Flanke.SH", "ZPP[1].Fuss.SFnorm", "ZPP[1].Flanke.SH"],
    "Z013": ["ZPP[0].Fuss.SFnorm", "ZPP[0].Flanke.SH", "ZP[0].Eps.aEffE"],
    "Z014": ["ZPleft[0].KHbPlanet[2]", "ZPleft[1].Eps.gEffI", "ZPP[0].Fuss.SFnorm"],
    "Z015": ["ZP[1].MP_ISO.Slam", "ZPP[0].Fuss.SFnorm", "ZPP[0].Flanke.SH"],
    "Z016": ["ZP[1].MP_ISO.Slam", "ZPP[0].Fuss.SFnorm", "ZPP[0].Flanke.SH"],
    "Z050": ["ZP[0].uDIN", "BeveloidR[0].dFf.e.r.nul", "BeveloidR[1].alphaC.l"],
    "Z060": ["RechSt.QualityChange[56]", "ZPP[0].Fuss.sFn", "ZR[0].Tol.Rs"],
    "Z070": ["caResults.ContactTemperature.min", "ZkegR[1].hfm", "ZkegR[1].hi"],
    "Z080": ["ZS.Schn.PVLP", "ZS.Schn.Knu", "ZS.Schn.Lufter"],
    "Z090": ["belt.elast", "z090k.beltSpannmin", "sheave[0].AxKftBet"],
    "W010": ["bearingDamage.damageLS.size", "WelG.WelleNichtlinear", "WelG.campbell.shaftSelectionNum"],
    "M010": ["m01r.tempW", "m01w.tauTa[2]", "m01n.tauTa[0]"],
    "M040": ["m04s.dehn_pmind", "m04s.MG_sp", "m04t.fase_mutter"],
    "M050": ["m050.safety", "m050.b", "m050.d3"],
    "M060": ["m060.SF[0]", "m060.Trating", "m060.mat[1].bez"],
    "F010": ["fd.gewalzt", "fd.tauc_zul", "fd.conical.Tol_e22"],
    "F020": ["f2.F0", "f2.Rm", "f2.De"],
    "F030": ["f3.F2", "f3.beta10", "f3.AM"],
    "F040": ["f4.Fc", "f4.delta", "f4.K4"],
    "F050": ["f5.da", "f5.theta2", "f5.Rh"],
    "A010": ["a010.Ig", "a010.operForce", "a010.SN"],
    "A020": ["a020.da", "a020.qmaxA", "a020.t3"],
    "K010": ["k10.ObMass2", "k10.TolName", "k10.ActualNumber"],
}


def connect():
    """连接到 KISSsoft COM 服务器。"""
    ks = win32com.client.Dispatch(PROGID)
    return ks


def is_module_licensed(ks, module_id):
    """检查 license 是否包含指定模块。"""
    return bool(ks.CheckLicense(module_id))


def load_module(ks, module_id, interactive=False):
    """加载指定模块。未授权模块返回 False。"""
    ks.GetModule(module_id, interactive)
    return ks.IsModuleValid()


def load_module_and_file(ks, module_id, filepath, interactive=False):
    """加载模块并读取文件。"""
    if not load_module(ks, module_id, interactive):
        raise RuntimeError(f"无法加载模块 {module_id}，请检查 license")
    ks.LoadFile(filepath)
    return True


def calculate(ks, ret_val=False):
    """执行计算。"""
    if ret_val:
        return ks.CalculateRetVal()
    ks.Calculate()
    return None


def set_var(ks, name, value):
    """设置变量，值自动转字符串。"""
    ks.SetVar(name, str(value))


def get_var(ks, name, as_json=False):
    """读取变量。推荐 as_json=True。"""
    if as_json:
        r = ks.GetVarAsJson(name)
        try:
            return json.loads(r)
        except json.JSONDecodeError:
            return {"raw": r}
    return ks.GetVar(name)


def get_result(ks, name, default=None):
    """安全读取结果变量，返回 return_value 或 default。"""
    r = get_var(ks, name, as_json=True)
    if isinstance(r, dict) and r.get("status_code") == "ok":
        return r.get("return_value")
    return default


def get_db_name(ks, db_name, table, flag, db_id, order=0):
    """读取数据库记录名称。完整签名 GetDBName(db_name, table, flag, ID, order)。"""
    return ks.GetDBName(db_name, table, flag, db_id, order)


def get_db_value(ks, db_name, table, db_id, fieldname):
    """读取数据库字段值。完整签名 GetDBValue(db_name, table, ID, fieldname)。"""
    return ks.GetDBValue(db_name, table, db_id, fieldname)


def get_db_id_from_var(ks, var_name):
    """从变量路径获取数据库 ID（如 ZR[0].mat.DBID）。"""
    return get_result(ks, var_name)


def call_json_func(ks, func_name, args=None):
    """调用内部函数并返回解析后的 JSON。"""
    if args is None:
        args = []
    r = ks.CallJsonFunc(func_name, args)
    try:
        return json.loads(r)
    except json.JSONDecodeError:
        return {"raw": r}


def call_json_func_ok(ks, func_name, args=None, default=None):
    """调用内部函数，成功时返回 return_value，否则返回 default。"""
    r = call_json_func(ks, func_name, args)
    if isinstance(r, dict) and r.get("status_code") == "ok":
        return r.get("return_value")
    return default


def parameter_sweep(ks, var_name, values, result_vars):
    """参数扫描。返回 [(var_value, {result_var: value})] 列表。"""
    results = []
    for v in values:
        set_var(ks, var_name, v)
        calculate(ks)
        row = {}
        for rv in result_vars:
            row[rv] = get_result(ks, rv)
        results.append((v, row))
    return results


def generate_report(ks, template_path, output_path, show=0, art=0):
    """使用模板生成 RTF/HTML 报告。"""
    ks.ReportWithParameters(template_path, output_path, show, art)
    return output_path


def generate_report_json(ks, rpt_template=None, args=None):
    """通过 CallJsonFunc('GenerateReport', ...) 生成临时报告，返回临时路径。"""
    if args is None:
        args = ['{}']
    if rpt_template:
        args = [rpt_template]
    return call_json_func_ok(ks, "GenerateReport", args)


def run_contact_analysis(ks, control_file, output_dir):
    """运行接触分析。结果输出到 output_dir。"""
    os.makedirs(output_dir, exist_ok=True)
    ks.CallFuncNParam(["CalculatePathOfContactForPairKS", control_file, output_dir])
    return os.path.join(output_dir, "anglereport.txt")


def save_file(ks, filepath):
    """保存当前计算文件。"""
    ks.SaveFile(filepath)
    return filepath


def release(ks):
    """释放当前模块。"""
    ks.ReleaseModule()


def file_info(ks, filepath):
    """读取文件元信息。"""
    return {
        "module": ks.GetModulFromFile(filepath),
        "version": ks.GetVersionFromFile(filepath),
        "kisssoft_version": ks.GetKsoftVersionFromFile(filepath),
    }


def batch_calculate(module_id, filepaths, input_vars=None, result_vars=None):
    """批量计算多个文件。"""
    if result_vars is None:
        result_vars = COMMON_RESULT_VARS.get(module_id, [])
    ks = connect()
    load_module(ks, module_id)
    all_results = []
    for fp in filepaths:
        ks.LoadFile(fp)
        if input_vars:
            for name, value in input_vars.items():
                set_var(ks, name, value)
        calculate(ks)
        all_results.append({
            "file": fp,
            **{rv: get_result(ks, rv) for rv in result_vars}
        })
    release(ks)
    return all_results


if __name__ == "__main__":
    # 示例用法
    ks = connect()
    mod = "Z012"
    filepath = r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12"
    load_module_and_file(ks, mod, filepath)
    calculate(ks)
    print("ZPP[0].Fuss.SFnorm:", get_result(ks, "ZPP[0].Fuss.SFnorm"))
    print("ZPP[0].Flanke.SH:", get_result(ks, "ZPP[0].Flanke.SH"))

    # 读取材料数据库信息
    mat_id = get_result(ks, "ZR[0].mat.DBID")
    print("ZR[0].mat.DBID:", mat_id)
    if mat_id:
        print("Material name:", get_db_name(ks, "KMAT", "KLUB", 0, mat_id, 0))
        print("NU40:", get_db_value(ks, "KMAT", "KLUB", mat_id, "NU40"))

    # 调用内部函数
    print("ModuleID:", call_json_func_ok(ks, "ModuleID"))
    print("Temp_Dir:", call_json_func_ok(ks, "Temp_Dir"))

    # 参数扫描示例
    sweep = parameter_sweep(ks, "ZR[0].b", [40, 42, 44, 46, 48, 50],
                            ["ZPP[0].Fuss.SFnorm", "ZPP[0].Flanke.SH"])
    print("Sweep results:")
    for v, row in sweep:
        print(v, row)
    release(ks)
