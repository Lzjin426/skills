# KISSsoft 2024 COM 接口进阶测试报告
- 生成时间：2026-07-10T08:24:50.616550
- 主机：main-long
- KISSsoft 安装路径：C:\Program Files\KISSsoft AG\KISSsoft 2024
- ProgID：`KISSsoftCOM2024.KISSsoft`
- 示例文件（Z012）：`C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12`
- 示例文件（Z013）：`C:\Program Files\KISSsoft AG\KISSsoft 2024\example\02 Spur Rack And Pinion.Z13`
- 接触分析控制文件：`C:\Program Files\KISSsoft AG\KISSsoft 2024\dat\Example_caControl.dat`

## 任务 1：Z012 上 ZR[0].b 参数扫描
在 Z012 模块中加载示例齿轮副，保持其他输入不变，仅改变齿宽 `ZR[0].b`，
每次 `Calculate()` 后读取 `ZPP[0].Fuss.SFnorm` 与 `ZPP[0].Flanke.SH`。

- 初始状态：ZR[0].b=44, SFnorm=2.5513426055976466955, SH=1.3328422678131217616

| ZR[0].b (mm) | ZPP[0].Fuss.SFnorm | ZPP[0].Flanke.SH | 消息数 |
|-------------|-------------------|------------------|--------|
| 40 | 2.3309467736510800506 | 1.2742829807027808986 | 0 |
| 42 | 2.4417210235968278553 | 1.3039711768127217884 | 0 |
| 44 | 2.5513426055976466955 | 1.3328422678131217616 | 0 |
| 46 | 2.6673127240339034039 | 1.3328422678131217616 | 0 |
| 48 | 2.7832828424701601122 | 1.3328422678131217616 | 0 |
| 50 | 2.8992529609064163765 | 1.3328422678131217616 | 0 |

## 任务 2：输入变量修改对输出变量的影响
逐个修改输入变量，每次重新计算，确认输出是否变化。

| 修改的输入变量 | 输出变量 | 修改前 | 修改后 | 是否变化 |
|---------------|----------|--------|--------|----------|
| 基线 | ZPP[0].Fuss.SFnorm | 2.5513426055976466955 | 2.5513426055976466955 | 否 |
| 基线 | ZPP[0].Flanke.SH | 1.3328422678131217616 | 1.3328422678131217616 | 否 |
| 基线 | ZR[0].da.nul | 164.98199999999999932 | 164.98199999999999932 | 否 |
| 基线 | ZR[0].df.nul | 137.98199999999999932 | 137.98199999999999932 | 否 |
| ZR[0].b | ZPP[0].Fuss.SFnorm | 2.5513426055976466955 | 2.4417210235968278553 | 是 |
| ZR[0].b | ZPP[0].Flanke.SH | 1.3328422678131217616 | 1.3039711768127217884 | 是 |
| ZR[0].b | ZR[0].da.nul | 164.98199999999999932 | 164.98199999999999932 | 否 |
| ZR[0].b | ZR[0].df.nul | 137.98199999999999932 | 137.98199999999999932 | 否 |
| ZR[0].x.nul | ZPP[0].Fuss.SFnorm | 2.5513426055976466955 | 2.5671503796537029629 | 是 |
| ZR[0].x.nul | ZPP[0].Flanke.SH | 1.3328422678131217616 | 1.3349290103284625619 | 是 |
| ZR[0].x.nul | ZR[0].da.nul | 164.98199999999999932 | 166.19999999999998863 | 是 |
| ZR[0].x.nul | ZR[0].df.nul | 137.98199999999999932 | 139.19999999999998863 | 是 |
| ZS.Geo.mn | ZPP[0].Fuss.SFnorm | 2.5513426055976466955 | 2.5513426055976466955 | 否 |
| ZS.Geo.mn | ZPP[0].Flanke.SH | 1.3328422678131217616 | 1.3328422678131217616 | 否 |
| ZS.Geo.mn | ZR[0].da.nul | 164.98199999999999932 | 137.65950000000000841 | 是 |
| ZS.Geo.mn | ZR[0].df.nul | 137.98199999999999932 | 126.48349999999999227 | 是 |

## 任务 3：接触分析调用
使用手册示例中的函数名 `CalculatePathOfContactForPairKS`，通过 `CallFuncNParam` 调用，
控制文件为 `C:\Program Files\KISSsoft AG\KISSsoft 2024\dat\Example_caControl.dat`，结果目录为 `C:\Users\Full stop\Desktop\kisssoft_ca_out`。
同时尝试 `CallJsonFunc` 作为对照。

- **输出文件已生成**：`C:\Users\Full stop\Desktop\kisssoft_ca_out\anglereport.txt`

前 10 行内容：

```

phi1	phi2	t1z	t2z	csalpha	csbeta	
0.1230181544	-3.14144863	1624.720196	4858.336054	959.1124557	943.4069355	
0.1203726027	-3.140578473	1624.71576	4858.563252	958.3384808	942.6923138	
0.117727051	-3.139708326	1624.677205	4858.710298	957.4567928	941.8759184	
0.1150814993	-3.138838269	1624.677921	4859.03074	955.8415039	940.3485686	
0.1124359476	-3.137968211	1624.679931	4859.374718	954.2377837	938.8361788	
0.1097903959	-3.137098149	1624.681815	4859.736542	952.6706066	937.3630265	
0.1071448442	-3.136228084	1624.683047	4860.114577	951.1376457	935.926802	
0.1044992925	-3.135358017	1624.682469	4860.504444	949.6257947	934.5144249	
```
- 无消息

#### CallJsonFunc 尝试
- CallJsonFunc 失败：(-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571), 2)

操作日志：
```
已加载 Z012 并执行 Calculate
CallFuncNParam(['CalculatePathOfContactForPairKS', control, out_dir]) 成功
结果目录内文件：['anglereport.txt']
```

## 任务 4：优化/尺寸设计函数调用
尝试调用 `roughSizing`、`RoughSizing`、`fineSizing`、`FineSizing` 等函数，
观察几何变量 `ZR[0].z`、`ZR[0].b`、`ZS.Geo.mn` 是否发生变化。

| 函数名 | 调用方式 | 返回 | 几何变量是否变化 | 变化变量 |
|--------|----------|------|------------------|----------|
| `roughSizing` | CallFunc | OK | 否 | — |
| `RoughSizing` | CallFunc | OK | 否 | — |
| `fineSizing` | CallFunc | OK | 否 | — |
| `FineSizing` | CallFunc | OK | 否 | — |
| `roughSizing` | CallFuncNParam | OK | 否 | — |
| `RoughSizing` | CallFuncNParam | OK | 否 | — |
| `fineSizing` | CallFuncNParam | OK | 否 | — |
| `FineSizing` | CallFuncNParam | OK | 否 | — |
| `RoughSizing` | CallJsonFunc | ERR: (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571), 2) | 否 | — |
| `FineSizing` | CallJsonFunc | ERR: (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571), 2) | 否 | — |

> 注：`CallFunc` 对未知函数名也返回“成功”，但不做任何操作；`CallJsonFunc` 对未注册的函数会抛出异常。

## 任务 5：多模块切换（Z012 ↔ Z013）
测试 `ReleaseModule` 后切换到 Z013，再切回 Z012，确认状态是否干净。

| 步骤 | IsModuleValid | 操作 | 结果 |
|------|---------------|------|------|
| 加载 Z012 | True | LoadFile + Calculate | SFnorm=2.5513426055976466955, SH=1.3328422678131217616 |
| ReleaseModule | False | 释放 Z012 | — |
| 加载 Z013 | True | LoadFile + Calculate | OK (IsModuleValid=True) |
| ReleaseModule | False | 释放 Z013 | — |
| 重新加载 Z012 | True | LoadFile + Calculate | SFnorm=2.5513426055976466955, SH=1.3328422678131217616 |

- **状态是否干净**：是（SFnorm 与 SH 与首次 Z012 结果一致）

## 附录：KISSsoftCOM2024.KISSsoft 方法清单（从类型库导出）
```
- GetModule(modul, interactive)
- Calculate()
- CalculateRetVal()
- CallFunc(name)
- SetVar(name, value)
- GetVar(name)
- ShowInterface(wait)
- IsActiveInterface()
- isActive()
- ReleaseModule()
- SetCallback(name, callback)
- LoadFile(fileName)
- LoadFileData(data)
- CheckLicense(name)
- GetININame()
- SaveFile(fileName)
- GetVersionFromFile(fileName)
- GetModulFromFile(fileName)
- GetKsoftVersionFromFile(fileName)
- GetKsoftVersion()
- SetSilentMode(silent)
- Report(show)
- ReportWithParameters(infile, outfile, show, art)
- Message() -> strings, types, numElem
- CallFuncNParam(paramArray)
- GetModuleOEM(modul, interactive, OEMcode)
- GetKsoftVersionSettings()
- GetDBName(db_name, table, flag, ID, order)
- GetDBValue(db_name, table, ID, fieldname)
- SetDebugFile(fileName)
- GetResultCount()
- GetNextResult()
- GetVarAsJson(nameBstr)
- CallJsonFunc(functionName, arrayOfJsonArgs)
- SetLanguage(index)
- GetLanguage()
- GetKsoftPatchLevel()
- IsModuleValid()
- LoadLicenseFile(name)
- LicenseNumber()
```

