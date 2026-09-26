---
name: kisssoft-com-2024
description: 教 AI 用 Python + pywin32 通过 COM 自动化 KISSsoft 2024。当用户需要控制 KISSsoft 2024、加载计算模块、批量计算、参数扫描、读取结果、生成报告或排查 COM 问题时触发本 skill。
---

# KISSsoft 2024 COM 自动化操作手册

> 本 skill 不是 API 字典，而是给新 AI 的**操作指南**：看到用户请求后，知道按什么顺序调用哪些 COM 方法完成任务。

## 1. 何时使用本 skill

- 用户说"用 Python 控制 KISSsoft"、"自动化 KISSsoft"、"批量算 KISSsoft"
- 用户要读取 KISSsoft 结果、做参数扫描、生成报告
- 用户遇到 KISSsoft COM 连接、模块加载、变量读取问题
- 用户提到 `Z012`、`W010`、`M010`、`F010` 等模块

## 2. 环境前提

- Windows 主机，已安装 KISSsoft 2024
- Python + `pywin32`
- 必须有 CC1/COM Basic 或 CC2/COM Expert license
- 当前可用模块（通过 `CheckLicense` 验证）：Z011–Z016、Z050/060/070/080/090、W010、M010/040/050/060、F010–F050、A010/A020、K010
- S020 加载失败；K019 `CalculateRetVal` 返回 False；其余未授权模块需先在 license 工具中点击"应用/保存"并重启 COM 进程

## 3. 最小工作示例

```python
import win32com.client
import json

ks = win32com.client.Dispatch("KISSsoftCOM2024.KISSsoft")
ks.SetSilentMode(1)  # 避免弹窗
ks.GetModule("Z012", 0)  # 两个参数！
ks.LoadFile(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")
ks.Calculate()

r = json.loads(ks.GetVarAsJson("ZPP[0].Fuss.SFnorm"))
print(r["return_value"])  # 2.55

ks.ReleaseModule()
```

## 4. 核心工作流

任何 KISSsoft COM 任务都按这个顺序：

1. **连接**：`ks = win32com.client.Dispatch("KISSsoftCOM2024.KISSsoft")`
2. **静默**：`ks.SetSilentMode(1)`（可选，避免 GUI 阻塞）
3. **加载模块**：`ks.GetModule(module_id, 0)`，再检查 `ks.IsModuleValid()`
4. **加载文件**：`ks.LoadFile(filepath)`（文件扩展名必须与模块匹配）
5. **计算**：`ks.Calculate()` 或 `ks.CalculateRetVal()`
6. **读取结果**：`ks.GetVarAsJson("变量路径")`
7. **修改参数**：`ks.SetVar("变量路径", "字符串值")`
8. **重复计算**：回到步骤 5
9. **释放模块**：`ks.ReleaseModule()`（切换模块前必须做）

## 5. 常用任务模式

### 5.1 读取安全系数（Z012）

```python
ks.GetModule("Z012", 0)
ks.LoadFile(r"...\01 Spur (ISO 6336).Z12")
ks.Calculate()

sf = json.loads(ks.GetVarAsJson("ZPP[0].Fuss.SFnorm"))["return_value"]
sh = json.loads(ks.GetVarAsJson("ZPP[0].Flanke.SH"))["return_value"]
print(f"SF={sf}, SH={sh}")
```

### 5.2 参数扫描

```python
results = []
for b in [40, 42, 44, 46, 48, 50]:
    ks.SetVar("ZR[0].b", str(b))
    ks.Calculate()
    results.append({
        "b": b,
        "SF": json.loads(ks.GetVarAsJson("ZPP[0].Fuss.SFnorm"))["return_value"],
        "SH": json.loads(ks.GetVarAsJson("ZPP[0].Flanke.SH"))["return_value"],
    })
```

### 5.3 批量处理多个文件

```python
for filepath in file_list:
    ks.LoadFile(filepath)
    ks.Calculate()
    sf = json.loads(ks.GetVarAsJson("ZPP[0].Fuss.SFnorm"))["return_value"]
    print(filepath, sf)
```

### 5.4 读取材料数据库

```python
mat_id = json.loads(ks.GetVarAsJson("ZR[0].mat.DBID"))["return_value"]
name = ks.GetDBName("KMAT", "KLUB", 0, mat_id, 0)
nu40 = ks.GetDBValue("KMAT", "KLUB", mat_id, "NU40")
```

签名：

- `GetDBName(db_name, table, flag, ID, order)`
- `GetDBValue(db_name, table, ID, fieldname)`

### 5.5 生成报告

```python
ks.ReportWithParameters(
    r"C:\Program Files\KISSsoft AG\KISSsoft 2024\rpt\Z012resc.rpt",
    r"C:\Users\full stop\Desktop\report.rtf",
    0,  # show=0 不弹窗
    0,  # art=0 RTF
)
```

- `art=0/1`：RTF（含嵌入 PNG）
- `art=2`：HTML

### 5.6 接触分析

```python
import os
control = r"C:\Program Files\KISSsoft AG\KISSsoft 2024\dat\Example_caControl.dat"
out_dir = r"C:\Users\full stop\Desktop\kisssoft_ca_out"
os.makedirs(out_dir, exist_ok=True)
ks.CallFuncNParam(["CalculatePathOfContactForPairKS", control, out_dir])
# 结果：out_dir\anglereport.txt（UTF-16 LE）
```

### 5.7 切换模块

```python
ks.ReleaseModule()
ks.GetModule("F010", 0)
ks.LoadFile(r"...\01 Compression Spring.F10")
ks.Calculate()
print(json.loads(ks.GetVarAsJson("fd.tauc_zul"))["return_value"])
ks.ReleaseModule()
```

## 6. 按模块的最小示例

每个模块都遵循同一模式：**加载模块 → 加载文件 → 计算 → 读变量**。区别只在文件路径和变量名。

| 模块 | 示例文件 | 关键结果变量 |
|---|---|---|
| Z011 | `example\01 Spur.Z11` | `ZR[0].da.nul`, `ZR[0].Vqual` |
| Z012 | `example\01 Spur (ISO 6336).Z12` | `ZPP[0].Fuss.SFnorm`, `ZPP[0].Flanke.SH` |
| Z013 | `example\01 Spur Rack and Pinion.Z13` | `ZP[0].Eps.aEffE`, `ZPP[1].sigF_ISO13691` |
| Z014 | `example\01 Spur Planetary (ISO 6336).Z14` | `ZPleft[0].KHbPlanet[2]`, `ZPleft[1].Eps.gEffI` |
| Z015 | `example\01 Three Gears (DIN 3990).Z15` | `ZP[1].MP_ISO.Slam`, `ZPP[0].Fuss.SFnorm` |
| Z016 | `example\03 Four Gears (ISO 6336).Z16` | `ZP[1].MP_ISO.Slam`, `ZPP[0].Fuss.SFnorm` |
| Z050 | `example\01 Spur Beveloid (Crowning).Z50` | `ZP[0].uDIN`, `BeveloidR[0].dFf.e.r.nul` |
| Z060 | `example\01 Face Gear.Z60` | `RechSt.QualityChange[56]`, `ZPP[0].Fuss.sFn` |
| Z070 | `example\01 Bevel (KN 3028 FH).z70` | `caResults.ContactTemperature.min`, `ZkegR[1].hfm` |
| Z080 | `example\01 Worm (DIN 3996 Example 1).Z80` | `ZS.Schn.PVLP`, `ZS.Schn.Knu` |
| Z090 | `example\01 V Belt.Z90` | `belt.elast`, `z090k.beltSpannmin` |
| W010 | `example\01 Shafts.W10` | `bearingDamage.damageLS.size`, `WelG.WelleNichtlinear` |
| M010 | `example\01 Cylindrical Interference Fit.M10` | `m01r.tempW`, `m01w.tauTa[2]` |
| M040 | `example\01 Bolts (VDI 2230 Example 1).M40` | `m04s.dehn_pmind`, `m04s.MG_sp` |
| M050 | `example\09 Shaft Ring.M50` | `m050.safety`, `m050.b` |
| M060 | `example\11 Hirth (Voith).M60` | `m060.SF[0]`, `m060.Trating` |
| F010 | `example\01 Compression Spring.F10` | `fd.gewalzt`, `fd.tauc_zul` |
| F020 | `example\03 Tension Spring.F20` | `f2.F0`, `f2.Rm` |
| F030 | `example\04 Leg Spring.F30` | `f3.F2`, `f3.beta10` |
| F040 | `example\05 Disk Spring.F40` | `f4.Fc`, `f4.delta` |
| F050 | `example\06 Torsion Bar Spring.F50` | `f5.da`, `f5.theta2` |
| A010 | `example\01 Gear Synchroniser.A10` | `a010.Ig`, `a010.operForce` |
| A020 | `example\02 Coupling.A20` | `a020.da`, `a020.qmaxA` |
| K010 | `example\01 Tolerance Calculation.K10` | `k10.ObMass2`, `k10.ActualNumber` |

完整变量列表见 `references/kisssoft_vars_index.md` 和各模块的 `references/kisssoft_vars_<module>.md`。

## 7. 内部函数调用

`CallJsonFunc` 用于调用内部函数，返回 JSON 字符串：

```python
r = json.loads(ks.CallJsonFunc("ModuleID", []))
print(r)  # {"status_code": "ok", "return_value": "Z012"}

r = json.loads(ks.CallJsonFunc("CalculateStdCA", ["1"]))
print(r)  # {"status_code": "ok", "return_value": True}
```

常用函数：

- `CalculateStdCA` / `CalculateCA`：接触分析相关计算
- `CalculateOptionsForX`：变位系数相关
- `GenerateReport`：生成临时报告
- `ModuleID`：返回当前模块
- `Temp_Dir`：返回临时目录
- `GetConsistency` / `GetGearCount` / `GetPairCount` / `GetZPPCount`：状态查询

注意：参数必须是字符串列表，布尔值会导致服务器异常。

## 8. 常见错误与排查

| 现象 | 原因 | 解决 |
|---|---|---|
| `Dispatch` 失败 | KISSsoft 未安装或 COM 未注册 | 检查安装和注册表 `KISSsoftCOM2024.KISSsoft` |
| `GetModule` 后 `IsModuleValid()` 为 False | 模块未授权 | 用 `ks.CheckLicense(module_id)` 确认；在 license 工具中点击"应用/保存"并重启进程 |
| `LoadFile` 失败 | 文件扩展名与模块不匹配 | 确认 `Z012` 用 `.Z12`，`F010` 用 `.F10` 等 |
| `Calculate` 无结果或报错 | 模型不完整或输入错误 | 先用 KISSsoft GUI 打开同一文件确认能算 |
| `GetVarAsJson` 返回 `not_found` | 变量路径错误或模块不同 | 用模块对应的 `.rpt` 模板或参考 `references/kisssoft_vars_<module>.md` 找正确路径 |
| `SetVar` 无效 | 值未转字符串 | 所有值必须 `str(value)` |
| `CallJsonFunc` 抛异常 | 参数类型错误 | 使用字符串列表，如 `["1"]` 而非 `[True]` |
| 切换模块后变量混乱 | 未 `ReleaseModule` | 切换模块前务必调用 `ks.ReleaseModule()` |
| 长时间无响应 | GUI 弹窗阻塞 | 开头调用 `ks.SetSilentMode(1)` |
| 报告生成后找不到 PDF | 默认输出是 RTF | 用 `ReportWithParameters` 指定输出路径，或从变量读取后用 reportlab 生成 PDF |

## 9. 设计原则

- **始终用 `GetVarAsJson`**，不要用 `GetVar`（后者常返回空字符串）
- **值都转字符串** 再传给 `SetVar`
- **切换模块前 ReleaseModule**
- **批量任务先 SetSilentMode(1)**
- **不确定变量路径时先查模块变量文档**
- **没有内置 Optimize/DOE COM 函数**，优化用外部循环：`SetVar → Calculate → GetVar`

## 10. 可复用脚本

`scripts/kisssoft_com_utils.py` 封装了常用函数：

```python
import sys
sys.path.insert(0, r"C:\Users\full stop\Desktop")
import kisssoft_com_utils as kc

ks = kc.connect()
kc.load_module_and_file(ks, "Z012", r"...\01 Spur (ISO 6336).Z12")
kc.calculate(ks)
print(kc.get_result(ks, "ZPP[0].Fuss.SFnorm"))

kc.parameter_sweep(ks, "ZR[0].b", [40, 42, 44], ["ZPP[0].Fuss.SFnorm", "ZPP[0].Flanke.SH"])
kc.release(ks)
```

## 11. 参考资料

- `references/kisssoft_com_reference.md`：完整方法签名（需要查具体参数时看）
- `references/kisssoft_vars_index.md`：24 个模块变量扫描索引
- `references/kisssoft_vars_<module>.md`：各模块完整变量列表
- `references/kisssoft_module_loadability.md`：哪些模块能真正加载计算
- `references/kisssoft_db_methods_scan.md`：数据库读取方法签名和示例
- `references/kisssoft_functions_deep_scan.md`：内部函数枚举结果
- `references/kisssoft_graphics_report_scan.md`：图形与报告函数
- `references/kisssoft_parameterized_batch_scan.md`：参数化函数与批量模式
- `references/kisssoft_optimization_doe_scan.md`：优化/DOE 探索结论
- `references/kisssoft_kisssys_scan.md`：KISSsys 自动化可行性
- `references/kisssoft_license_file_notes.md`：license 文件结构和启用模块说明
