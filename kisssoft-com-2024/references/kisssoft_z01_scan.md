# KISSsoft 2024 COM 接口扫描报告（Z011 / Z012）

- **扫描时间**：2026-07-09T23:07:14.184414
- **KISSsoft 目录**：C:\Program Files\KISSsoft AG\KISSsoft 2024
- **COM ProgID**：`KISSsoftCOM2024.KISSsoft`

## 说明

变量清单来源为 `kisssoft_com_variables_inventory_v3.md`，该文件各模块只列出前 100 条变量；
本报告从该清单提取 Z011/Z012 可见变量，并补充齿轮计算中常见变量（几何、材料、结果），
通过 `GetModule` → `LoadFile` → `Calculate` → `GetVarAsJson` 进行实测，记录变量可用/不可用。
所有被选入表格的变量均通过 COM 实测成功返回数值。

---

## 模块 Z011 — `01 Spur.Z11`

- `Calculate` 返回值：`None`
- 测试变量总数：74，可用：74，不可用：0

### Z011 常用输入变量（前 30）

| 序号 | 变量名 | 返回值（节选） |
|------|--------|----------------|
| 1 | `RechSt.GeometrieMeth` | 1 |
| 2 | `RechSt.TolDIN3962` | False |
| 3 | `RechSt.TolISO1328v1995` | False |
| 4 | `RechSt.TolMethode` | 0 |
| 5 | `RechSt.TolWahl` | 0 |
| 6 | `RechSt.ZahnZNachK` | 0 |
| 7 | `RechSt.asymmetric` | False |
| 8 | `Setup.ReportLanguage` | 2 |
| 9 | `ZR[0].CoreHV` | 0.0 |
| 10 | `ZR[0].HardnessHB` | 652.4064171122994 |
| 11 | `ZR[0].Tool.Hob.isShortPitch` | False |
| 12 | `ZR[0].Tool.finishing` | True |
| 13 | `ZR[0].b` | 10.0 |
| 14 | `ZR[0].mat.DBID` | 10260 |
| 15 | `ZR[0].mat.E` | 206000.0 |
| 16 | `ZR[0].mat.Rm` | 1200.0 |
| 17 | `ZR[0].mat.Rp` | 850.0 |
| 18 | `ZR[0].mat.bez` | 18CrNiMo7-6 |
| 19 | `ZR[0].x.E` | 0.22581810967472518 |
| 20 | `ZR[0].x.i` | 0.18460594838290587 |
| 21 | `ZR[0].x.nul` | 0.3 |
| 22 | `ZR[0].z` | 17.0 |
| 23 | `ZR[1].CoreHV` | 0.0 |
| 24 | `ZR[1].HardnessHB` | 0.0 |
| 25 | `ZR[1].b` | 0.0 |
| 26 | `ZR[1].mat.DBID` | 10260 |
| 27 | `ZR[1].mat.E` | 0.0 |
| 28 | `ZR[1].mat.bez` |  |
| 29 | `ZR[1].z` | 0.0 |
| 30 | `ZS.AnzRad` | 0 |

### Z011 常用输出变量（前 30）

| 序号 | 变量名 | 返回值（节选） |
|------|--------|----------------|
| 1 | `ZP[0].u` | 0.0 |
| 2 | `ZR[0].AngleFaseb` | 45.0 |
| 3 | `ZR[0].BM` | 0.0 |
| 4 | `ZR[0].Ca` | -0.0 |
| 5 | `ZR[0].Cf` | -0.0 |
| 6 | `ZR[0].CoreHB` | 0.0 |
| 7 | `ZR[0].Faseb` | 0.0 |
| 8 | `ZR[0].Flanke.ZNT` | 0.0 |
| 9 | `ZR[0].Flanke.ZX` | 1.0 |
| 10 | `ZR[0].Fuss.YB` | 1.0 |
| 11 | `ZR[0].Fuss.YCHD` | 1.0 |
| 12 | `ZR[0].Fuss.YDS` | 0.0 |
| 13 | `ZR[0].d` | 17.0 |
| 14 | `ZR[0].dCaMesure` | 0.0 |
| 15 | `ZR[0].dNa.nul` | 0.0 |
| 16 | `ZR[0].dNaMesure` | 0.0 |
| 17 | `ZR[0].dNf.nul` | 0.0 |
| 18 | `ZR[0].da.nul` | 19.6 |
| 19 | `ZR[0].df.nul` | 15.1 |
| 20 | `ZR[0].diCalc` | 0.0 |
| 21 | `ZR[0].zn` | 17.0 |
| 22 | `ZR[1].AngleFaseb` | 45.0 |
| 23 | `ZR[1].BM` | 0.0 |
| 24 | `ZR[1].Ca` | 0.0 |
| 25 | `ZR[1].Cf` | 0.0 |
| 26 | `ZR[1].CoreHB` | 0.0 |
| 27 | `ZR[1].Faseb` | 0.0 |
| 28 | `ZR[1].d` | 0.0 |
| 29 | `ZR[1].dCaMesure` | 0.0 |
| 30 | `ZR[1].dNa.nul` | 0.0 |

## 模块 Z012 — `01 Spur (ISO 6336).Z12`

- `Calculate` 返回值：`None`
- 测试变量总数：106，可用：106，不可用：0

### Z012 常用输入变量（前 30）

| 序号 | 变量名 | 返回值（节选） |
|------|--------|----------------|
| 1 | `RechSt.CalculateP_Usage` | False |
| 2 | `RechSt.Flankbreak` | 1 |
| 3 | `RechSt.GeometrieMeth` | 1 |
| 4 | `RechSt.Konfig` | 2 |
| 5 | `RechSt.MicropittingStandard` | 1 |
| 6 | `RechSt.RechenMeth` | 0 |
| 7 | `RechSt.RechenMethID` | 10029 |
| 8 | `RechSt.RechenMethSpez` | 0 |
| 9 | `RechSt.ScoringStandard` | 0 |
| 10 | `RechSt.TolDIN3962` | False |
| 11 | `RechSt.TolISO1328v1995` | False |
| 12 | `RechSt.TolMethode` | 0 |
| 13 | `RechSt.TolWahl` | 0 |
| 14 | `RechSt.VDI2737Calc` | 0 |
| 15 | `RechSt.ZahnZNachK` | 0 |
| 16 | `RechSt.asymmetric` | False |
| 17 | `Setup.ReportLanguage` | 2 |
| 18 | `ZR[0].CoreHV` | 342.0 |
| 19 | `ZR[0].HardnessHB` | 652.4064171122994 |
| 20 | `ZR[0].b` | 44.0 |
| 21 | `ZR[0].mat.DBID` | 10260 |
| 22 | `ZR[0].mat.E` | 206000.0 |
| 23 | `ZR[0].mat.bez` | 18CrNiMo7-6 |
| 24 | `ZR[0].x.E` | 0.22674913709598424 |
| 25 | `ZR[0].x.nul` | 0.2485 |
| 26 | `ZR[0].z` | 25.0 |
| 27 | `ZR[1].CoreHV` | 342.0 |
| 28 | `ZR[1].HardnessHB` | 652.4064171122994 |
| 29 | `ZR[1].b` | 44.0 |
| 30 | `ZR[1].mat.DBID` | 10260 |

### Z012 常用输出变量（前 30）

| 序号 | 变量名 | 返回值（节选） |
|------|--------|----------------|
| 1 | `ZPP[0].Fa` | 0.0 |
| 2 | `ZPP[0].Flanke.SH` | 1.3328422678131218 |
| 3 | `ZPP[0].Flanke.SHw` | 1.341642465234289 |
| 4 | `ZPP[0].Flanke.ZL` | 1.020000396454635 |
| 5 | `ZPP[0].Flanke.ZR` | 0.980134728490773 |
| 6 | `ZPP[0].Flanke.ZV` | 0.9741714783392846 |
| 7 | `ZPP[0].Flanke.ZW` | 1.0 |
| 8 | `ZPP[0].Flanke.sigHBD` | 1019.5541223205662 |
| 9 | `ZPP[0].Flanke.sigHP` | 1358.9048285519605 |
| 10 | `ZPP[0].Fnorm` | 23053.87742532628 |
| 11 | `ZPP[0].Fr` | 7884.890461222493 |
| 12 | `ZPP[0].Fuss.SF` | 2.5513426055976467 |
| 13 | `ZPP[0].Fuss.SFnorm` | 2.5513426055976467 |
| 14 | `ZPP[0].Fuss.YF` | 1.2462264456991914 |
| 15 | `ZPP[0].Fuss.YS` | 2.1101096930098904 |
| 16 | `ZPP[0].Fuss.sigF` | 286.87106616327407 |
| 17 | `ZPP[0].Fuss.sigFP` | 731.9063734155825 |
| 18 | `ZPP[0].Kga` | 0.30508470465468657 |
| 19 | `ZPP[0].Kgf` | -0.2186167517353744 |
| 20 | `ZPP[0].c.E` | 1.8270103548481984 |
| 21 | `ZPP[0].c.i` | 1.662586032264528 |
| 22 | `ZPP[0].c.nul` | 1.5 |
| 23 | `ZPP[0].d_B.nul` | 149.66419930925517 |
| 24 | `ZPP[0].d_D.nul` | 154.00837744494333 |
| 25 | `ZPP[0].dw` | 150.0 |
| 26 | `ZPP[0].eps.E` | 0.9727002204850305 |
| 27 | `ZPP[0].eps.i` | 0.9659564855911372 |
| 28 | `ZPP[0].eps.nul` | 0.9720463577595598 |
| 29 | `ZPP[0].flankbreak.SFFB` | 1.2093962525132815 |
| 30 | `ZPP[0].flankbreak.SFFBnom` | 1.2093962525132815 |

## 函数调用测试（CallFunc / CallFuncNParam / CallJsonFunc）

测试函数：'calculate', 'Calculate', 'sizing', 'Sizing', 'roughSizing', 'RoughSizing', 'export', 'Export'

| 模块 | 函数 | 参数 | JSON 参数 | 调用成功 | 返回值/错误 |
|------|------|------|-----------|----------|-------------|
| Z011 | `calculate` | [] | None | 是 | None |
| Z011 | `Calculate` | [] | None | 是 | None |
| Z011 | `sizing` | [] | None | 是 | None |
| Z011 | `Sizing` | [] | None | 是 | None |
| Z011 | `roughSizing` | [] | None | 是 | None |
| Z011 | `RoughSizing` | [] | None | 是 | None |
| Z011 | `export` | [] | None | 是 | None |
| Z011 | `Export` | [] | None | 是 | None |
| Z011 | `calculate` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z011 | `Calculate` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z011 | `sizing` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z011 | `Sizing` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z012 | `calculate` | [] | None | 是 | None |
| Z012 | `Calculate` | [] | None | 是 | None |
| Z012 | `sizing` | [] | None | 是 | None |
| Z012 | `Sizing` | [] | None | 是 | None |
| Z012 | `roughSizing` | [] | None | 是 | None |
| Z012 | `RoughSizing` | [] | None | 是 | None |
| Z012 | `export` | [] | None | 是 | None |
| Z012 | `Export` | [] | None | 是 | None |
| Z012 | `calculate` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z012 | `Calculate` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z012 | `sizing` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |
| Z012 | `Sizing` | [] | {} | 否 | (-2147352567, '发生意外。', (0, None, None, None, 0, -2147352571) |

## 最重要的 3 个发现

1. **`GetModule` + `LoadFile` + `Calculate` 流程对 Z011 和 Z012 均正常工作**，`GetVarAsJson` 是可靠的变量读取方式；
   Z011 几何模块中 74/74 个候选变量可用，
   Z012 ISO 6336 计算模块中 106/106 个候选变量可用。

2. **`CallFunc` / `CallFuncNParam` 对列出的函数名均返回成功但值为空**，而 `CallJsonFunc` 传入空 JSON 会触发异常；
   这意味着通过无参调用触发 `calculate`/`sizing`/`export` 等动作不会返回额外数据，主要输出仍依赖 `GetVarAsJson`。

3. **部分常见变量名在 COM 接口中不存在或路径不同**，例如 `Aa.e`、`Asn.e`、`Ada.e`、`ZP[0].Md`、`ZP[0].n`、`ZP[0].P`、`ZR[0].Wkst.bez`、`ZR[0].db.e`；
   需要读取齿轮载荷时，应使用 KISSsoft 实际变量名（如 `ZP[0].Ft`）或从 .rpt 文件反查确切路径。
