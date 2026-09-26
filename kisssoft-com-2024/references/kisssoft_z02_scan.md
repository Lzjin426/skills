# KISSsoft Z013 / Z014 COM 接口扫描报告

**生成时间：** 2026-07-09 23:11:40
**KISSsoft 版本：** 2024 -SP1
**License 编号：** 1113
**安装路径：** `C:\Program Files\KISSsoft AG\KISSsoft 2024`

## 1. 测试方法说明

- 读取 `kisssoft_com_variables_inventory_v3.md` 中 Z013 / Z014 的变量列表；
- 由于 v3.md 对每个模块只列出前 100 个变量（按字母顺序），本脚本按同一规则重新扫描 `\rpt` 下的所有 `.rpt` 模板，得到完整变量集合；
- 使用 `win32com.client.Dispatch('KISSsoftCOM2024.KISSsoft')` 连接 COM 对象；
- 对每个模块执行：`GetModule(mod, False)` → `LoadFile` → `Calculate`；
- 使用 `GetVarAsJson` / `GetVar` 读取变量，记录可用性；
- 对两个模块分别调用 `CallFunc`、`CallFuncNParam`、`CallJsonFunc`，记录非空返回值；
- 总耗时：33.4 秒。

## 2. 变量清单统计

| 模块 | v3.md 列出数 | RPT 模板实际唯一数 | 合并后测试数 |
|------|---------------|-------------------|-------------|
| Z013 | 19 | 481 | 481 |
| Z014 | 18 | 594 | 594 |

## 3. 模块 Z013：齿条齿轮（Rack and pinion）

- **示例文件：** `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Rack and Pinion.Z13`
- **文件存在：** True
- **模块有效：** True
- **LoadFile 成功：** True
- **Calculate 成功：** True
- **CalculateRetVal：** True
- **测试变量总数：** 538
- **可用变量数：** 232

### 3.1 Z013 最常用的 30 个输入变量

| 序号 | 变量路径 | 状态 | GetVarAsJson 返回值 | GetVar 返回值 |
|------|---------|------|---------------------|---------------|
| 1 | `ZS.Geo.mn` | ok | {"return_value": 1.5, "status_code": "ok"} | 1.5 |
| 2 | `ZS.Geo.beta` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 3 | `ZR[0].z` | ok | {"return_value": 18.0, "status_code": "ok"} | 18 |
| 4 | `ZR[1].z` | ok | {"return_value": -9000.0, "status_code": "ok"} | -9000 |
| 5 | `ZR[2].z` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 6 | `ZR[0].b` | ok | {"return_value": 20.0, "status_code": "ok"} | 20 |
| 7 | `ZR[1].b` | ok | {"return_value": 18.0, "status_code": "ok"} | 18 |
| 8 | `ZR[2].b` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 9 | `ZR[0].x.nul` | ok | {"return_value": 0.25, "status_code": "ok"} | 0.25 |
| 10 | `ZR[1].x.nul` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 11 | `ZR[2].x.nul` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 12 | `ZR[0].da.nul` | ok | {"return_value": 30.75, "status_code": "ok"} | 30.75 |
| 13 | `ZR[0].df.nul` | ok | {"return_value": 24.0, "status_code": "ok"} | 24 |
| 14 | `ZR[0].d.nul` | ok | {"return_value": 27.0, "status_code": "ok"} | 27 |
| 15 | `ZR[1].da.nul` | ok | {"return_value": -13497.0, "status_code": "ok"} | -13497 |
| 16 | `ZR[1].df.nul` | ok | {"return_value": -13503.75, "status_code": "ok"} | -13503.75 |
| 17 | `ZR[1].d.nul` | ok | {"return_value": -13500.0, "status_code": "ok"} | -13500 |
| 18 | `ZR[2].da.nul` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 19 | `ZR[2].df.nul` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 20 | `ZR[2].d.nul` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 21 | `ZR[0].mat.bez` | ok | {"return_value": "42 CrMo 4 (3)", "status_code": "ok"} | 42 CrMo 4 (3) |
| 22 | `ZR[1].mat.bez` | ok | {"return_value": "C45 (1)", "status_code": "ok"} | C45 (1) |
| 23 | `ZR[2].mat.bez` | json_only | {"return_value": "", "status_code": "ok"} |  |
| 24 | `RechSt.RechenMethID` | ok | {"return_value": 10080, "status_code": "ok"} | 10080 |
| 25 | `RechSt.RechenMeth` | ok | {"return_value": 3, "status_code": "ok"} | 3 |
| 26 | `RechSt.RechenMethSpez` | ok | {"return_value": 0, "status_code": "ok"} | 0 |
| 27 | `RechSt.GeometrieMeth` | ok | {"return_value": 1, "status_code": "ok"} | 1 |
| 28 | `RechSt.Konfig` | ok | {"return_value": 3, "status_code": "ok"} | 3 |
| 29 | `RechSt.TolWahl` | ok | {"return_value": 3, "status_code": "ok"} | 3 |
| 30 | `Zst.KHbVariant` | ok | {"return_value": 0, "status_code": "ok"} | 0 |

### 3.2 Z013 最常用的 30 个输出变量

| 序号 | 变量路径 | 状态 | GetVarAsJson 返回值 | GetVar 返回值 |
|------|---------|------|---------------------|---------------|
| 1 | `ZPP[0].Fuss.SF` | ok | {"return_value": 3.1114299644092527, "status_code": "ok"} | 3.1114299644092526798 |
| 2 | `ZPP[0].Fuss.SFnorm` | ok | {"return_value": 3.1114299644092527, "status_code": "ok"} | 3.1114299644092526798 |
| 3 | `ZPP[0].Flanke.SH` | ok | {"return_value": 0.7059888470407865, "status_code": "ok"} | 0.70598884704078646024 |
| 4 | `ZPP[1].Fuss.SF` | ok | {"return_value": 1.5639849403629518, "status_code": "ok"} | 1.5639849403629517699 |
| 5 | `ZPP[1].Fuss.SFnorm` | ok | {"return_value": 1.5639849403629518, "status_code": "ok"} | 1.5639849403629517699 |
| 6 | `ZPP[1].Flanke.SH` | ok | {"return_value": 0.5066947052083709, "status_code": "ok"} | 0.50669470520837089911 |
| 7 | `ZPP[2].Fuss.SF` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 8 | `ZPP[2].Fuss.SFnorm` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 9 | `ZPP[2].Flanke.SH` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 10 | `ZPP[3].Fuss.SF` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 11 | `ZPP[3].Fuss.SFnorm` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 12 | `ZPP[3].Flanke.SH` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 13 | `ZP[0].u` | ok | {"return_value": -500.0, "status_code": "ok"} | -500 |
| 14 | `ZP[1].u` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 15 | `ZP[2].u` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 16 | `ZP[0].KHb_nominal` | ok | {"return_value": 1.381597736967783, "status_code": "ok"} | 1.3815977369677829856 |
| 17 | `ZP[1].KHb_nominal` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 18 | `ZP[2].KHb_nominal` | ok | {"return_value": 1.0, "status_code": "ok"} | 1 |
| 19 | `ZPP[0].gamPC.A` | ok | {"return_value": 0.31779792929061484, "status_code": "ok"} | 0.31779792929061484452 |
| 20 | `ZPP[0].gamPC.B` | ok | {"return_value": 0.1544833896817538, "status_code": "ok"} | 0.15448338968175379105 |
| 21 | `ZPP[0].gamPC.C` | ok | {"return_value": 0.10024541094114647, "status_code": "ok"} | 0.10024541094114647333 |
| 22 | `ZPP[1].gamPC.A` | ok | {"return_value": 0.0002865299486239266, "status_code": "ok"} | 0.0002865299486239265836 |
| 23 | `ZPP[1].gamPC.B` | ok | {"return_value": -4.009913059372858e-05, "status_code": "ok"} | -4.009913059372857691e-05 |
| 24 | `ZPP[1].gamPC.C` | ok | {"return_value": -0.00014857508807493078, "status_code": "ok"} | -0.00014857508807493077785 |
| 25 | `ZPP[2].gamPC.A` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 26 | `ZPP[2].gamPC.B` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 27 | `ZPP[2].gamPC.C` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 28 | `caResults.TransmissionError.delta` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 29 | `caResults.MaxHertzianStress` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 30 | `caResults.PowerLoss.average` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |

## 3. 模块 Z014：行星齿轮（Planetary gear）

- **示例文件：** `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Planetary (ISO 6336).Z14`
- **文件存在：** True
- **模块有效：** True
- **LoadFile 成功：** True
- **Calculate 成功：** True
- **CalculateRetVal：** True
- **测试变量总数：** 636
- **可用变量数：** 328

### 3.1 Z014 最常用的 30 个输入变量

| 序号 | 变量路径 | 状态 | GetVarAsJson 返回值 | GetVar 返回值 |
|------|---------|------|---------------------|---------------|
| 1 | `ZS.Geo.mn` | ok | {"return_value": 1.3, "status_code": "ok"} | 1.3000000000000000444 |
| 2 | `ZS.Geo.beta` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 3 | `ZR[0].z` | ok | {"return_value": 22.0, "status_code": "ok"} | 22 |
| 4 | `ZR[1].z` | ok | {"return_value": 27.0, "status_code": "ok"} | 27 |
| 5 | `ZR[2].z` | ok | {"return_value": -77.0, "status_code": "ok"} | -77 |
| 6 | `ZR[0].b` | ok | {"return_value": 10.0, "status_code": "ok"} | 10 |
| 7 | `ZR[1].b` | ok | {"return_value": 10.0, "status_code": "ok"} | 10 |
| 8 | `ZR[2].b` | ok | {"return_value": 10.0, "status_code": "ok"} | 10 |
| 9 | `ZR[0].x.nul` | ok | {"return_value": 0.3, "status_code": "ok"} | 0.2999999999999999889 |
| 10 | `ZR[1].x.nul` | ok | {"return_value": 0.5890261985367122, "status_code": "ok"} | 0.58902619853671223105 |
| 11 | `ZR[2].x.nul` | ok | {"return_value": -0.9020773200296776, "status_code": "ok"} | -0.90207732002967755403 |
| 12 | `ZR[0].da.nul` | ok | {"return_value": 31.748, "status_code": "ok"} | 31.748000000000001108 |
| 13 | `ZR[0].df.nul` | ok | {"return_value": 26.130000000000003, "status_code": "ok"} | 26.130000000000002558 |
| 14 | `ZR[0].d.nul` | ok | {"return_value": 28.6, "status_code": "ok"} | 28.600000000000001421 |
| 15 | `ZR[1].da.nul` | ok | {"return_value": 38.99946811619545, "status_code": "ok"} | 38.999468116195451728 |
| 16 | `ZR[1].df.nul` | ok | {"return_value": 33.38146811619545, "status_code": "ok"} | 33.381468116195449625 |
| 17 | `ZR[1].d.nul` | ok | {"return_value": 35.1, "status_code": "ok"} | 35.100000000000001421 |
| 18 | `ZR[2].da.nul` | ok | {"return_value": -99.84540103207718, "status_code": "ok"} | -99.845401032077177206 |
| 19 | `ZR[2].df.nul` | ok | {"return_value": -105.3659980402812, "status_code": "ok"} | -105.3659980402811982 |
| 20 | `ZR[2].d.nul` | ok | {"return_value": -100.10000000000001, "status_code": "ok"} | -100.10000000000000853 |
| 21 | `ZR[0].mat.bez` | ok | {"return_value": "18CrNiMo7-6", "status_code": "ok"} | 18CrNiMo7-6 |
| 22 | `ZR[1].mat.bez` | ok | {"return_value": "18CrNiMo7-6", "status_code": "ok"} | 18CrNiMo7-6 |
| 23 | `ZR[2].mat.bez` | ok | {"return_value": "34 CrNiMo 6 (1)", "status_code": "ok"} | 34 CrNiMo 6 (1) |
| 24 | `RechSt.RechenMethID` | ok | {"return_value": 10029, "status_code": "ok"} | 10029 |
| 25 | `RechSt.RechenMeth` | ok | {"return_value": 0, "status_code": "ok"} | 0 |
| 26 | `RechSt.RechenMethSpez` | ok | {"return_value": 0, "status_code": "ok"} | 0 |
| 27 | `RechSt.GeometrieMeth` | ok | {"return_value": 1, "status_code": "ok"} | 1 |
| 28 | `RechSt.Konfig` | ok | {"return_value": 4, "status_code": "ok"} | 4 |
| 29 | `RechSt.TolWahl` | ok | {"return_value": 0, "status_code": "ok"} | 0 |
| 30 | `Zst.KHbVariant` | ok | {"return_value": 0, "status_code": "ok"} | 0 |

### 3.2 Z014 最常用的 30 个输出变量

| 序号 | 变量路径 | 状态 | GetVarAsJson 返回值 | GetVar 返回值 |
|------|---------|------|---------------------|---------------|
| 1 | `ZPP[0].Fuss.SF` | ok | {"return_value": 4.31351958261616, "status_code": "ok"} | 4.3135195826161600863 |
| 2 | `ZPP[0].Fuss.SFnorm` | ok | {"return_value": 4.31351958261616, "status_code": "ok"} | 4.3135195826161600863 |
| 3 | `ZPP[0].Flanke.SH` | ok | {"return_value": 1.3108478731706683, "status_code": "ok"} | 1.3108478731706683096 |
| 4 | `ZPP[1].Fuss.SF` | ok | {"return_value": 3.2473492340130137, "status_code": "ok"} | 3.2473492340130136746 |
| 5 | `ZPP[1].Fuss.SFnorm` | ok | {"return_value": 3.2473492340130137, "status_code": "ok"} | 3.2473492340130136746 |
| 6 | `ZPP[1].Flanke.SH` | ok | {"return_value": 1.4618260047131129, "status_code": "ok"} | 1.4618260047131128587 |
| 7 | `ZPP[2].Fuss.SF` | ok | {"return_value": 3.4016704001273066, "status_code": "ok"} | 3.4016704001273065927 |
| 8 | `ZPP[2].Fuss.SFnorm` | ok | {"return_value": 3.4016704001273066, "status_code": "ok"} | 3.4016704001273065927 |
| 9 | `ZPP[2].Flanke.SH` | ok | {"return_value": 2.2775295812406013, "status_code": "ok"} | 2.2775295812406013418 |
| 10 | `ZPP[3].Fuss.SF` | ok | {"return_value": 3.041802271433001, "status_code": "ok"} | 3.0418022714330010814 |
| 11 | `ZPP[3].Fuss.SFnorm` | ok | {"return_value": 3.041802271433001, "status_code": "ok"} | 3.0418022714330010814 |
| 12 | `ZPP[3].Flanke.SH` | ok | {"return_value": 1.1331909197647878, "status_code": "ok"} | 1.1331909197647878074 |
| 13 | `ZP[0].u` | ok | {"return_value": 1.2272727272727273, "status_code": "ok"} | 1.2272727272727272929 |
| 14 | `ZP[1].u` | ok | {"return_value": -2.8518518518518516, "status_code": "ok"} | -2.851851851851851638 |
| 15 | `ZP[2].u` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 16 | `ZP[0].KHb_nominal` | ok | {"return_value": 1.4279290815521817, "status_code": "ok"} | 1.4279290815521816782 |
| 17 | `ZP[1].KHb_nominal` | ok | {"return_value": 1.446396638760996, "status_code": "ok"} | 1.4463966387609958897 |
| 18 | `ZP[2].KHb_nominal` | ok | {"return_value": 1.0, "status_code": "ok"} | 1 |
| 19 | `ZPP[0].gamPC.A` | ok | {"return_value": 0.25926951064618964, "status_code": "ok"} | 0.25926951064618963816 |
| 20 | `ZPP[0].gamPC.B` | ok | {"return_value": 0.2048672922331198, "status_code": "ok"} | 0.20486729223311980763 |
| 21 | `ZPP[0].gamPC.C` | ok | {"return_value": 0.0681189848380033, "status_code": "ok"} | 0.068118984838003299176 |
| 22 | `ZPP[1].gamPC.A` | ok | {"return_value": 3.0466912987517794, "status_code": "ok"} | 3.0466912987517793532 |
| 23 | `ZPP[1].gamPC.B` | ok | {"return_value": 3.0910190322735396, "status_code": "ok"} | 3.0910190322735395796 |
| 24 | `ZPP[1].gamPC.C` | ok | {"return_value": 3.202443579039931, "status_code": "ok"} | 3.202443579039930821 |
| 25 | `ZPP[2].gamPC.A` | ok | {"return_value": -0.15397792184423703, "status_code": "ok"} | -0.15397792184423703121 |
| 26 | `ZPP[2].gamPC.B` | ok | {"return_value": -0.0905552256457281, "status_code": "ok"} | -0.090555225645728099071 |
| 27 | `ZPP[2].gamPC.C` | ok | {"return_value": -0.0695005829817153, "status_code": "ok"} | -0.069500582981715297581 |
| 28 | `caResults.TransmissionError.delta` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 29 | `caResults.MaxHertzianStress` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |
| 30 | `caResults.PowerLoss.average` | ok | {"return_value": 0.0, "status_code": "ok"} | 0 |

## 4. CallFunc / CallFuncNParam / CallJsonFunc 测试结果

- `CallFunc` 与 `CallFuncNParam` 对所有候选函数均返回 `None`；
- `CallJsonFunc` 对每个函数名都返回了一个 JSON 对象，其中大部分是 `not_implemented` / `bad_function_call` 状态信息，少数返回实际值或成功状态。

| 函数名 | Z013 CallJsonFunc | Z014 CallJsonFunc |
|--------|-------------------|-------------------|
| `Calculate` | `{"return_value":1,"status_code":"ok"}` | `{"return_value":1,"status_code":"ok"}` |
| `CalculateStdCA` | `{"return_value":true,"status_code":"ok"}` | `{"return_value":true,"status_code":"ok"}` |
| `Circle` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `Gears` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `GenerateUIVar` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `GetConsistency` | `{"return_value":1,"status_code":"ok"}` | `{"return_value":1,"status_code":"ok"}` |
| `Line` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `Module` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `ModuleID` | `{"return_value":"Z013","status_code":"ok"}` | `{"return_value":"Z014","status_code":"ok"}` |
| `NewGraphic` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `Position` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `SHIFT` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `Safety` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `SetColor` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `ShowDialog` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `ShowGraphic` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `Spur` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `Temp_Dir` | `{"return_value":"C:/Windows/TEMP/KISS_4\\","status_code":"ok"}` | `{"return_value":"C:/Windows/TEMP/KISS_4\\","status_code":"ok"}` |
| `Text` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `addItem` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `alf12_23` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `alf23_34` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `append_to_file` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `calculate` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `close_file` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `coordinateSystem` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `coverages` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `defineBoundary` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `defineGearPair` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `distances` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `file` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `gear` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `gear2` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `graphic_to_x` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `graphic_to_y` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `happens` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `meshing` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `open_file` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `roughSizingGearbox` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `x_to_graphic` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `y_to_graphic` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `CALCULATE` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `roughSizing` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `RoughSizing` | `{"status_code":"bad_function_call","status_msg":false}` | `{"status_code":"bad_function_call","status_msg":false}` |
| `roughsizing` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `ROUGH SIZING` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `RoughSizingGearbox` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `RoughsizingGearbox` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `fineSizing` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `FineSizing` | `{"status_code":"bad_function_call","status_msg":false}` | `{"return_value":true,"status_code":"ok"}` |
| `sizing` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `Sizing` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `SIZING` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `export` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `Export` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `EXPORT` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `saveReport` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `SaveReport` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `generateReport` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `GenerateReport` | `{"status_code":"bad_function_call","status_msg":null}` | `{"status_code":"bad_function_call","status_msg":null}` |
| `contactAnalysis` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `ContactAnalysis` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `toothFormCalculation` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `ToothFormCalculation` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `loadFile` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `loadfile` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `GetModule` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `getModule` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `calculateStdCA` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `getConsistency` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `moduleID` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `generateUIVar` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `showDialog` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `newGraphic` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `showGraphic` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `setColor` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `line` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `circle` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `text` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `message` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `AddItem` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `DefineGearPair` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `DefineBoundary` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `execute` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |
| `temp_Dir` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` | `{"status_code":"not_implemented","status_msg":"The call function was not found"}` |

### 返回成功状态 / 实际值的 CallJsonFunc

| 模块 | 函数名 | 返回值 |
|------|--------|--------|
| Z013 | `Calculate` | `{"return_value": 1, "status_code": "ok"}` |
| Z013 | `CalculateStdCA` | `{"return_value": true, "status_code": "ok"}` |
| Z013 | `GetConsistency` | `{"return_value": 1, "status_code": "ok"}` |
| Z013 | `ModuleID` | `{"return_value": "Z013", "status_code": "ok"}` |
| Z013 | `Temp_Dir` | `{"return_value": "C:/Windows/TEMP/KISS_4\\", "status_code": "ok"}` |
| Z014 | `Calculate` | `{"return_value": 1, "status_code": "ok"}` |
| Z014 | `CalculateStdCA` | `{"return_value": true, "status_code": "ok"}` |
| Z014 | `FineSizing` | `{"return_value": true, "status_code": "ok"}` |
| Z014 | `GetConsistency` | `{"return_value": 1, "status_code": "ok"}` |
| Z014 | `ModuleID` | `{"return_value": "Z014", "status_code": "ok"}` |
| Z014 | `Temp_Dir` | `{"return_value": "C:/Windows/TEMP/KISS_4\\", "status_code": "ok"}` |

## 5. 最重要的 3 个发现

1. **跨模块通用可用变量**：在 Z013 和 Z014 两个模块中都能读取的变量主要集中在计算控制（`RechSt.*`）和全局设置（`Setup.*`、`METRICUNITS`）上。

   - `RechSt.CalculateP_Usage`：2/2 模块可用
   - `RechSt.Flankbreak`：2/2 模块可用
   - `RechSt.GeometrieMeth`：2/2 模块可用
   - `RechSt.Konfig`：2/2 模块可用
   - `RechSt.MicropittingStandard`：2/2 模块可用
   - `RechSt.RechenMeth`：2/2 模块可用
   - `RechSt.RechenMethID`：2/2 模块可用
   - `RechSt.RechenMethSpez`：2/2 模块可用
   - `RechSt.ScoringStandard`：2/2 模块可用
   - `RechSt.TolDIN3962`：2/2 模块可用

2. **输入与输出变量可用性差异**：

   - **Z013**：成功读取 30 个常用输入变量、30 个常用输出变量。未读取到的变量大多是因为在 COM 接口中未暴露（RPT 模板中存在但 COM 未注册），并非文件未加载。
   - **Z014**：成功读取 30 个常用输入变量、30 个常用输出变量。未读取到的变量大多是因为在 COM 接口中未暴露（RPT 模板中存在但 COM 未注册），并非文件未加载。

3. **CallJsonFunc 存在成功返回**：在 `CallJsonFunc` 遍历测试中，少数函数名返回了 `status_code: ok` 或实际值，例如：`Calculate`（返回 1）、`CalculateStdCA`（返回 true）、`ModuleID`（返回模块 ID）、`GetConsistency`（返回 1）、`Temp_Dir`（返回临时目录）。在 Z014 中 `FineSizing` 还返回了 true。这些函数在 COM 层确实被注册并返回了状态/结果，而不是无副作用的空白调用。

## 6. 限制与备注

- `GetVarAsJson` 返回的 `status_code` 为 `ok` 表示变量在当前模块中已注册；`not_found` 表示 RPT 模板中存在但 COM 接口未暴露。
- 输入 / 输出分类是基于变量前缀的启发式规则，部分变量可能兼具输入与输出属性。
- 齿条齿轮（Z013）和行星齿轮（Z014）的数组索引含义不同（Z013 中 `ZR[1]` 通常指齿条，Z014 中 `ZR[0/1/2]` 通常指太阳轮 / 行星轮 / 齿圈），实际读取时应根据模块语义理解。
