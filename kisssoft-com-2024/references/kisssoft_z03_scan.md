# KISSsoft Z015/Z016 COM 接口扫描结果

- 扫描来源: `C:\Users\Full stop\Desktop\kisssoft_com_variables_inventory_v3.md` 及 `C:\Program Files\KISSsoft AG\KISSsoft 2024\rpt` 下的 Z015/Z016 报告模板
- 示例目录: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example`
- 脚本目录: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\skript`

## 1. Z015 常用输入/输出变量 (30 个)

| 序号 | 变量路径 |
|------|----------|
| 1 | `ZR[0].x.nul` |
| 2 | `ZS.Geo.beta` |
| 3 | `ZS.Geo.mn` |
| 4 | `ZR[0].da.E` |
| 5 | `ZR[0].da.nul` |
| 6 | `ZR[0].df.E` |
| 7 | `ZR[0].df.nul` |
| 8 | `ZP[0].Eps.b` |
| 9 | `ZP[0].Eps.a` |
| 10 | `ZR[0].KM.MdK.nul` |
| 11 | `ZR[0].KM.Wk.nul` |
| 12 | `ZR[0].mat.typ` |
| 13 | `ZR[0].mat.DBID` |
| 14 | `ZR[0].mat.bez` |
| 15 | `ZPP[0].Flanke.SH` |
| 16 | `ZPP[0].Fuss.SF` |
| 17 | `ZPP[0].Fuss.SFnorm` |
| 18 | `ZR[0].mat.E` |
| 19 | `ZPP[0].Fuss.sigF` |
| 20 | `ZR[0].b` |
| 21 | `ZR[0].z` |
| 22 | `ZPP[0].Flanke.sigHP` |
| 23 | `ZPP[0].Fuss.sigFP` |
| 24 | `ZP[0].a` |
| 25 | `ZP[0].u` |
| 26 | `ZR[0].n` |
| 27 | `ZP[0].Flanke.sigH` |
| 28 | `ZS.Geo.alfn` |
| 29 | `ZS.Geo.mt` |
| 30 | `ZP[0].Eps.aEffE` |

## 2. Z016 常用输入/输出变量 (30 个)

| 序号 | 变量路径 |
|------|----------|
| 1 | `ZR[0].x.nul` |
| 2 | `ZS.Geo.beta` |
| 3 | `ZS.Geo.mn` |
| 4 | `ZR[0].da.E` |
| 5 | `ZR[0].da.nul` |
| 6 | `ZR[0].df.E` |
| 7 | `ZR[0].df.nul` |
| 8 | `ZP[0].Eps.b` |
| 9 | `ZP[0].Eps.a` |
| 10 | `ZR[0].KM.MdK.nul` |
| 11 | `ZR[0].KM.Wk.nul` |
| 12 | `ZR[0].mat.typ` |
| 13 | `ZR[0].mat.DBID` |
| 14 | `ZR[0].mat.bez` |
| 15 | `ZPP[0].Flanke.SH` |
| 16 | `ZPP[0].Fuss.SF` |
| 17 | `ZPP[0].Fuss.SFnorm` |
| 18 | `ZR[0].mat.E` |
| 19 | `ZPP[0].Fuss.sigF` |
| 20 | `ZR[0].b` |
| 21 | `ZR[0].z` |
| 22 | `ZPP[0].Flanke.sigHP` |
| 23 | `ZPP[0].Fuss.sigFP` |
| 24 | `ZP[0].a` |
| 25 | `ZP[0].u` |
| 26 | `ZR[0].n` |
| 27 | `ZP[0].Flanke.sigH` |
| 28 | `ZS.Geo.alfn` |
| 29 | `ZS.Geo.mt` |
| 30 | `ZP[0].Eps.aEffE` |

## 3. COM 接口读取结果

- ProgID: `KISSsoftCOM2024.KISSsoft`
- 连接状态: connected

### Z015
- 状态: calculated
- 示例文件: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Three Gears (DIN 3990).Z15`

| 变量 | 读取结果 (JSON) |
|------|-----------------|
| `ZR[0].x.nul` | {"return_value":0.5,"status_code":"ok"} |
| `ZS.Geo.beta` | {"return_value":0.0,"status_code":"ok"} |
| `ZS.Geo.mn` | {"return_value":0.2,"status_code":"ok"} |
| `ZR[0].da.E` | {"return_value":2.9760000000000004,"status_code":"ok"} |
| `ZR[0].da.nul` | {"return_value":2.9760000000000004,"status_code":"ok"} |
| `ZR[0].df.E` | {"return_value":2.0561429339975543,"status_code":"ok"} |
| `ZR[0].df.nul` | {"return_value":2.1000000000000005,"status_code":"ok"} |
| `ZP[0].Eps.b` | {"return_value":0.0,"status_code":"ok"} |
| `ZP[0].Eps.a` | {"return_value":1.2494285207507256,"status_code":"ok"} |
| `ZR[0].KM.MdK.nul` | {"return_value":3.3097205723772394,"status_code":"ok"} |
| `ZR[0].KM.Wk.nul` | {"return_value":1.5780830406019004,"status_code":"ok"} |
| `ZR[0].mat.typ` | {"return_value":2,"status_code":"ok"} |
| `ZR[0].mat.DBID` | {"return_value":10110,"status_code":"ok"} |
| `ZR[0].mat.bez` | {"return_value":"42 CrMo 4 (1)","status_code":"ok"} |
| `ZPP[0].Flanke.SH` | {"return_value":0.4118847830818135,"status_code":"ok"} |
| `ZPP[0].Fuss.SF` | {"return_value":4.865082122429253,"status_code":"ok"} |
| `ZPP[0].Fuss.SFnorm` | {"return_value":4.865082122429253,"status_code":"ok"} |
| `ZR[0].mat.E` | {"return_value":206000.0,"status_code":"ok"} |
| `ZPP[0].Fuss.sigF` | {"return_value":109.77006243602098,"status_code":"ok"} |
| `ZR[0].b` | {"return_value":2.0,"status_code":"ok"} |
| `ZR[0].z` | {"return_value":12.0,"status_code":"ok"} |
| `ZPP[0].Flanke.sigHP` | {"return_value":426.81052981622236,"status_code":"ok"} |
| `ZPP[0].Fuss.sigFP` | {"return_value":534.0403683354285,"status_code":"ok"} |
| `ZP[0].a` | {"return_value":2.8,"status_code":"ok"} |
| `ZP[0].u` | {"return_value":1.25,"status_code":"ok"} |
| `ZR[0].n` | {"return_value":2000.0,"status_code":"ok"} |
| `ZP[0].Flanke.sigH` | {"return_value":973.7599073239661,"status_code":"ok"} |
| `ZS.Geo.alfn` | {"return_value":0.3490658503988659,"status_code":"ok"} |
| `ZS.Geo.mt` | {"return_value":0.2,"status_code":"ok"} |
| `ZP[0].Eps.aEffE` | {"return_value":1.2695316245992767,"status_code":"ok"} |

### Z016
- 状态: calculated
- 示例文件: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\03 Four Gears (ISO 6336).Z16`

| 变量 | 读取结果 (JSON) |
|------|-----------------|
| `ZR[0].x.nul` | {"return_value":0.45,"status_code":"ok"} |
| `ZS.Geo.beta` | {"return_value":0.0,"status_code":"ok"} |
| `ZS.Geo.mn` | {"return_value":1.5,"status_code":"ok"} |
| `ZR[0].da.E` | {"return_value":26.732,"status_code":"ok"} |
| `ZR[0].da.nul` | {"return_value":26.732,"status_code":"ok"} |
| `ZR[0].df.E` | {"return_value":20.000590650394454,"status_code":"ok"} |
| `ZR[0].df.nul` | {"return_value":20.1,"status_code":"ok"} |
| `ZP[0].Eps.b` | {"return_value":0.0,"status_code":"ok"} |
| `ZP[0].Eps.a` | {"return_value":1.3801058761393614,"status_code":"ok"} |
| `ZR[0].KM.MdK.nul` | {"return_value":28.78668220246326,"status_code":"ok"} |
| `ZR[0].KM.Wk.nul` | {"return_value":11.847344710934136,"status_code":"ok"} |
| `ZR[0].mat.typ` | {"return_value":2,"status_code":"ok"} |
| `ZR[0].mat.DBID` | {"return_value":10110,"status_code":"ok"} |
| `ZR[0].mat.bez` | {"return_value":"42 CrMo 4 (1)","status_code":"ok"} |
| `ZPP[0].Flanke.SH` | {"return_value":1.0512268780740859,"status_code":"ok"} |
| `ZPP[0].Fuss.SF` | {"return_value":12.77235696707857,"status_code":"ok"} |
| `ZPP[0].Fuss.SFnorm` | {"return_value":12.77235696707857,"status_code":"ok"} |
| `ZR[0].mat.E` | {"return_value":206000.0,"status_code":"ok"} |
| `ZPP[0].Fuss.sigF` | {"return_value":39.42344390095516,"status_code":"ok"} |
| `ZR[0].b` | {"return_value":10.0,"status_code":"ok"} |
| `ZR[0].z` | {"return_value":15.0,"status_code":"ok"} |
| `ZPP[0].Flanke.sigHP` | {"return_value":506.69191326887704,"status_code":"ok"} |
| `ZPP[0].Fuss.sigFP` | {"return_value":503.53029837459576,"status_code":"ok"} |
| `ZP[0].a` | {"return_value":34.5,"status_code":"ok"} |
| `ZP[0].u` | {"return_value":2.0,"status_code":"ok"} |
| `ZR[0].n` | {"return_value":2000.0,"status_code":"ok"} |
| `ZP[0].Flanke.sigH` | {"return_value":457.152855139953,"status_code":"ok"} |
| `ZS.Geo.alfn` | {"return_value":0.3490658503988659,"status_code":"ok"} |
| `ZS.Geo.mt` | {"return_value":1.5,"status_code":"ok"} |
| `ZP[0].Eps.aEffE` | {"return_value":1.387284038785344,"status_code":"ok"} |

## 4. Skript 函数调用统计

### 4.1 跨文件总调用频次 Top 50

| 函数 | 出现次数 | 出现文件 |
|------|----------|----------|
| `write` | 8 | S20_Generate_gearbox.skript, W10_Oil_level_to_mdrag_and_export.skript, Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_Comparison_ISO6336_edition_2006_2019.skript, Z12_Face_width_variation_and_export.skript, Z12_KHBeta_own_calculation.skript, Z12_Rule_example.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `Calculate` | 6 | S20_Generate_gearbox.skript, W10_Oil_level_to_mdrag_and_export.skript, Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_Comparison_ISO6336_edition_2006_2019.skript, Z12_Face_width_variation_and_export.skript, Z12_KHBeta_own_calculation.skript |
| `Temp_Dir` | 3 | W10_Oil_level_to_mdrag_and_export.skript, Z12_Face_width_variation_and_export.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `append_to_file` | 3 | W10_Oil_level_to_mdrag_and_export.skript, Z12_Face_width_variation_and_export.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `open_file` | 3 | W10_Oil_level_to_mdrag_and_export.skript, Z12_Face_width_variation_and_export.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `round` | 3 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_Comparison_ISO6336_edition_2006_2019.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `Execute` | 2 | W10_Oil_level_to_mdrag_and_export.skript, Z12_Face_width_variation_and_export.skript |
| `Line` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `NewGraphic` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `SetColor` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `ShowGraphic` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `Text` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `abs` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `close_file` | 2 | W10_Oil_level_to_mdrag_and_export.skript, Z12_Face_width_variation_and_export.skript |
| `coordinateSystem` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `graphic_to_x` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `max` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_KHBeta_own_calculation.skript |
| `to_string` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `x_to_graphic` | 2 | Z015_Z016_S020_3GearChain CalcSynchro.skript, Z12_to_Z16_Manufacturing_Deviation.skript |
| `CalculateStdCA` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |
| `Circle` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |
| `GenerateUIVar` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `GetConsistency` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `LoadFile` | 1 | Z12_Load_file.skript |
| `ModuleID` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `Pi` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `ShowDialog` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `addItem` | 1 | S20_Generate_gearbox.skript |
| `calculate` | 1 | Z12_Face_width_variation_and_export.skript |
| `defineBoundary` | 1 | S20_Generate_gearbox.skript |
| `defineGearPair` | 1 | S20_Generate_gearbox.skript |
| `degrees` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `floor` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `graphic_to_y` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |
| `min` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `pi` | 1 | Z015_Z016_S020_3GearChain CalcSynchro.skript |
| `roughSizingGearbox` | 1 | S20_Generate_gearbox.skript |
| `size` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |
| `sqrt` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |
| `square` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |
| `y_to_graphic` | 1 | Z12_to_Z16_Manufacturing_Deviation.skript |

### 4.2 按文件列出的函数调用

#### S20_Generate_gearbox.skript

- `addItem`
- `defineGearPair`
- `defineBoundary`
- `Calculate`
- `write`
- `roughSizingGearbox`

#### W10_Oil_level_to_mdrag_and_export.skript

- `Temp_Dir`
- `open_file`
- `append_to_file`
- `Calculate`
- `write`
- `close_file`
- `Execute`

#### Z015_Z016_S020_3GearChain CalcSynchro.skript

- `GetConsistency`
- `write`
- `Calculate`
- `ModuleID`
- `GenerateUIVar`
- `ShowDialog`
- `pi`
- `round`
- `degrees`
- `Pi`
- `floor`
- `abs`
- `min`
- `max`
- `x_to_graphic`
- `graphic_to_x`
- `coordinateSystem`
- `SetColor`
- `Line`
- `Text`
- `to_string`
- `NewGraphic`
- `ShowGraphic`

#### Z12_Comparison_ISO6336_edition_2006_2019.skript

- `Calculate`
- `round`
- `write`

#### Z12_Face_width_variation_and_export.skript

- `calculate`
- `Calculate`
- `Temp_Dir`
- `open_file`
- `append_to_file`
- `write`
- `close_file`
- `Execute`

#### Z12_KHBeta_own_calculation.skript

- `max`
- `write`
- `Calculate`

#### Z12_Load_file.skript

- `LoadFile`

#### Z12_Rule_example.skript

- `write`

#### Z12_to_Z16_Manufacturing_Deviation.skript

- `write`
- `size`
- `Temp_Dir`
- `open_file`
- `append_to_file`
- `round`
- `CalculateStdCA`
- `square`
- `sqrt`
- `x_to_graphic`
- `graphic_to_x`
- `y_to_graphic`
- `graphic_to_y`
- `coordinateSystem`
- `abs`
- `SetColor`
- `Line`
- `Text`
- `to_string`
- `NewGraphic`
- `Circle`
- `ShowGraphic`

## 5. 全部不重复函数调用清单

- `Calculate`
- `CalculateStdCA`
- `Circle`
- `Execute`
- `GenerateUIVar`
- `GetConsistency`
- `Line`
- `LoadFile`
- `ModuleID`
- `NewGraphic`
- `Pi`
- `SetColor`
- `ShowDialog`
- `ShowGraphic`
- `Temp_Dir`
- `Text`
- `abs`
- `addItem`
- `append_to_file`
- `calculate`
- `close_file`
- `coordinateSystem`
- `defineBoundary`
- `defineGearPair`
- `degrees`
- `floor`
- `graphic_to_x`
- `graphic_to_y`
- `max`
- `min`
- `open_file`
- `pi`
- `roughSizingGearbox`
- `round`
- `size`
- `sqrt`
- `square`
- `to_string`
- `write`
- `x_to_graphic`
- `y_to_graphic`
