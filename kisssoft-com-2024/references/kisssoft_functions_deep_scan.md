# KISSsoft 2024 COM 内部函数深度扫描报告

**生成时间**: 2026-07-10 11:04:02
**目标主机**: DESKTOP-US6VJ8U (main-long)
**COM ProgID**: KISSsoftCOM2024.KISSsoft
**测试模块**: Z012 (圆柱齿轮 ISO 6336)
**测试文件**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12`

## 摘要

- **候选函数总数**: 1001
- **可确认可用函数** (status_code=ok): 63
- **存在但需参数函数** (bad_function_call): 63
- **执行异常函数** (unknown_exception/exception): 6
- **未确认/不存在函数** (not_implemented): 869

## 测试方法

1. 在 `C:\Program Files\KISSsoft AG\KISSsoft 2024\` 目录下搜索所有 `*.skript` 文件和 `*.rpt` 文件。
2. 从 `*.skript` 文件中提取函数调用名；从 `kisscalc.dll` 导出符号（C++ 类方法名）中筛选候选函数名。
3. 使用 `GetModule("Z012", True)` 加载齿轮模块，并加载示例文件作为测试基准。
4. 对每个候选函数名，依次尝试以下调用方式：
   - `ks.CallJsonFunc(name, [])`
   - `ks.CallJsonFunc(name, [args])`（对部分函数提供示例参数）
   - `ks.CallFunc(name)`
   - `ks.CallFuncNParam([name, ...args])`（Python 绑定要求参数数组，首元素为函数名）
5. 记录返回状态：`ok`、`bad_function_call`、`not_implemented`、`unknown_exception`、`exception`。

## 调用方式行为说明

- **`CallJsonFunc(name, args)`**: 最可靠的调用方式。返回 JSON 字符串，包含 `status_code` 和 `return_value`。`ok` 表示函数存在且执行成功；`bad_function_call` 表示函数名存在但参数不匹配；`not_implemented` 表示函数名不存在/未暴露。
- **`CallFunc(name)`**: 对无参数函数返回 `None`，但对部分函数（如 `LoadFile`、`Execute`、`SaveFile`）会抛出服务器异常。无法区分函数是否存在。
- **`CallFuncNParam([name, ...args])`**: Python COM 绑定要求参数以数组形式传入（第一个元素为函数名）。对无参数函数返回 `None`；对带参数函数也返回 `None` 或抛出异常。可用性较低，不适合探测函数是否存在。

## 可确认可用函数 (status_code=ok)

以下函数通过 `CallJsonFunc` 调用成功返回 `ok`（含无参数或带参数调用）：

| 函数名 | 来源 | 返回值示例 | 备注 |
|--------|------|-------------|------|
| `CalcHobbingProcess` | kisscalc_methods | None | |
| `CalcSafetyTooth_MeasuredTorque` | kisscalc_methods | 0 | |
| `Calculate` | deep_test | 1 | |
| `CalculateAddendumHeight` | kisscalc_methods | None | |
| `CalculateCA` | deep_test | True | |
| `CalculateCenterDistanceAngle` | kisscalc_methods | None | |
| `CalculateDedendumHeight` | kisscalc_methods | None | |
| `CalculateFineSizing` | deep_test | None | |
| `CalculateGearPump` | kisscalc_methods | None | |
| `CalculateGridingDiameter` | kisscalc_methods | None | |
| `CalculateGrindingDistance` | kisscalc_methods | None | |
| `CalculateLeadAngle` | kisscalc_methods | None | |
| `CalculateLifeTime` | deep_test | None | |
| `CalculateMaximumRootRoundingInvolute` | kisscalc_methods | None | |
| `CalculateNormalModule` | kisscalc_methods | None | |
| `CalculateOB` | kisscalc_methods | None | |
| `CalculateOperatingBacklash` | deep_test | None | |
| `CalculateOptionsForX` | deep_test | 0.2706453579469703 | |
| `CalculatePower` | kisscalc_methods | None | |
| `CalculateProtuberanceAngle` | kisscalc_methods | None | |
| `CalculateProtuberanceHeight` | kisscalc_methods | None | |
| `CalculateStdCA` | deep_test | True | |
| `CalculateTipAlteration` | kisscalc_methods | None | |
| `CalculateToothThicknessCalculation` | kisscalc_methods | None | |
| `CalculateToothThicknessChange` | kisscalc_methods | None | |
| `CalculateWaterAbsorption` | kisscalc_methods | None | |
| `CalculatedNa` | kisscalc_methods | None | |
| `CalculatedNf` | kisscalc_methods | None | |
| `Execute` | deep_test | None | |
| `GenerateReport` | deep_test | C:/Windows/TEMP/KISS_9\Z012.pprpt | |
| `GetAsymmetricCount` | deep_test | 4 | |
| `GetConsistency` | deep_test | 1 | |
| `GetGearCount` | deep_test | 2 | |
| `GetHardnessCount` | deep_test | 4 | |
| `GetPairCount` | deep_test | 1 | |
| `GetReducerType` | deep_test | None | |
| `GetRefProfileType` | deep_test | 2 | |
| `GetZPPCount` | deep_test | 2 | |
| `LoadFile` | deep_test | None | |
| `ModuleID` | skript | Z012 | |
| `SetCenterDistanceTolerances` | deep_test | None | |
| `SetRefProfileDataForCurrentTool` | deep_test | None | |
| `SetToothThicknessTolerances` | deep_test | None | |
| `SetupCalculateZFTR06` | kisscalc_methods | None | |
| `SetupCalculationForAsymmetricGears` | kisscalc_methods | None | |
| `SetupCenterDistanceAngle` | kisscalc_methods | None | |
| `SetupConvertXeToQ` | kisscalc_methods | None | |
| `SetupFineSizing` | kisscalc_methods | None | |
| `SetupGrindingDistance` | kisscalc_methods | None | |
| `SetupImportManufacturingDeviations` | kisscalc_methods | None | |
| `SetupReferenceProfile` | kisscalc_methods | None | |
| `SetupToothDiameterAllowances` | kisscalc_methods | None | |
| `SetupToothThicknessAllowances` | kisscalc_methods | None | |
| `SetupToothThicknessCalculation` | kisscalc_methods | None | |
| `Temp_Dir` | deep_test | C:/Windows/TEMP/KISS_9\ | |
| `WriteSummary` | kisscalc_methods | True | |
| `calculateContactAnalysis` | kisscalc_methods | None | |
| `calculateContactAnalysisResults` | kisscalc_methods | None | |
| `calculateDeflection` | kisscalc_methods | None | |
| `calculateDeflectionStiffness` | kisscalc_methods | None | |
| `calculateModificationProposal` | kisscalc_methods | None | |
| `calculateRoughSizing` | kisscalc_methods | None | |
| `calculationMethodChanged` | kisscalc_methods | None | |

### 按类别细分

#### 计算类

| 函数名 | 返回值 |
|--------|--------|
| `CalcHobbingProcess` | None |
| `CalcSafetyTooth_MeasuredTorque` | 0 |
| `Calculate` | 1 |
| `CalculateAddendumHeight` | None |
| `CalculateCA` | True |
| `CalculateCenterDistanceAngle` | None |
| `CalculateDedendumHeight` | None |
| `CalculateFineSizing` | None |
| `CalculateGearPump` | None |
| `CalculateGridingDiameter` | None |
| `CalculateGrindingDistance` | None |
| `CalculateLeadAngle` | None |
| `CalculateLifeTime` | None |
| `CalculateMaximumRootRoundingInvolute` | None |
| `CalculateNormalModule` | None |
| `CalculateOB` | None |
| `CalculateOperatingBacklash` | None |
| `CalculateOptionsForX` | 0.2706453579469703 |
| `CalculatePower` | None |
| `CalculateProtuberanceAngle` | None |
| `CalculateProtuberanceHeight` | None |
| `CalculateStdCA` | True |
| `CalculateTipAlteration` | None |
| `CalculateToothThicknessCalculation` | None |
| `CalculateToothThicknessChange` | None |
| `CalculateWaterAbsorption` | None |
| `CalculatedNa` | None |
| `CalculatedNf` | None |
| `calculateContactAnalysis` | None |
| `calculateContactAnalysisResults` | None |
| `calculateDeflection` | None |
| `calculateDeflectionStiffness` | None |
| `calculateModificationProposal` | None |
| `calculateRoughSizing` | None |
| `calculationMethodChanged` | None |

#### 获取类

| 函数名 | 返回值 |
|--------|--------|
| `GetAsymmetricCount` | 4 |
| `GetConsistency` | 1 |
| `GetGearCount` | 2 |
| `GetHardnessCount` | 4 |
| `GetPairCount` | 1 |
| `GetReducerType` | None |
| `GetRefProfileType` | 2 |
| `GetZPPCount` | 2 |

#### 设置/Setup 类

| 函数名 | 返回值 |
|--------|--------|
| `SetCenterDistanceTolerances` | None |
| `SetRefProfileDataForCurrentTool` | None |
| `SetToothThicknessTolerances` | None |
| `SetupCalculateZFTR06` | None |
| `SetupCalculationForAsymmetricGears` | None |
| `SetupCenterDistanceAngle` | None |
| `SetupConvertXeToQ` | None |
| `SetupFineSizing` | None |
| `SetupGrindingDistance` | None |
| `SetupImportManufacturingDeviations` | None |
| `SetupReferenceProfile` | None |
| `SetupToothDiameterAllowances` | None |
| `SetupToothThicknessAllowances` | None |
| `SetupToothThicknessCalculation` | None |

#### 文件/系统类

| 函数名 | 返回值 |
|--------|--------|
| `Execute` | None |
| `LoadFile` | None |
| `Temp_Dir` | C:/Windows/TEMP/KISS_9\ |
| `WriteSummary` | True |

#### 报告/生成类

| 函数名 | 返回值 |
|--------|--------|
| `GenerateReport` | C:/Windows/TEMP/KISS_9\Z012.pprpt |

## 存在但需参数的函数 (bad_function_call)

以下函数名被 COM 识别，但无参数调用返回 `bad_function_call`。需要进一步提供正确参数才能执行：

| 函数名 | 来源 |
|--------|------|
| `CalcToothThicknessAllowances` | kisscalc_methods |
| `CalculateCAStep` | kisscalc_methods |
| `CalculateHerringboneGrooveWidth` | kisscalc_methods |
| `CalculateImportManufacturingDeviations` | kisscalc_methods |
| `CalculateKHbeta` | kisscalc_methods |
| `CalculateMaximumTipRounding` | kisscalc_methods |
| `CalculateTipFormHeight` | kisscalc_methods |
| `CalculateTipRounding` | kisscalc_methods |
| `CalculateTolerances` | kisscalc_methods |
| `CalculateToothForm` | deep_test |
| `CalculateZFTR06` | kisscalc_methods |
| `Circle` | deep_test |
| `CreateReportVar` | kisscalc_methods |
| `ExportGraphicAsDXF` | kisscalc_methods |
| `GenerateImage` | kisscalc_methods |
| `GenerateUIVar` | skript |
| `GetCrowning` | kisscalc_methods |
| `GetCyclesAutomatic` | kisscalc_methods |
| `GetCyclesInput` | kisscalc_methods |
| `GetCyclesPerRotation` | kisscalc_methods |
| `GetFactorCrowning` | kisscalc_methods |
| `GetFactorEccentricity` | kisscalc_methods |
| `GetHelixAngle` | kisscalc_methods |
| `GetWidthFactor` | kisscalc_methods |
| `Line` | deep_test |
| `NewGraphic` | deep_test |
| `ReadFineSizingTools` | kisscalc_methods |
| `SetAInput` | kisscalc_methods |
| `SetCenterDistanceBlock` | kisscalc_methods |
| `SetColor` | skript |
| `SetConsistency` | kisscalc_methods |
| `SetCrowning` | kisscalc_methods |
| `SetCyclesAutomatic` | kisscalc_methods |
| `SetCyclesInput` | kisscalc_methods |
| `SetCyclesPerRotation` | kisscalc_methods |
| `SetFactorCrowning` | kisscalc_methods |
| `SetFactorEccentricity` | kisscalc_methods |
| `SetGrindingBlockInputFactor` | kisscalc_methods |
| `SetGrindingBlockInputLength` | kisscalc_methods |
| `SetHelixAngle` | kisscalc_methods |
| `SetLanguage` | kisscalc_methods |
| `SetLzInput` | kisscalc_methods |
| `SetRadioXsizing` | kisscalc_methods |
| `SetTipAlteration` | kisscalc_methods |
| `SetTolAsnBlock` | kisscalc_methods |
| `SetToothThicknessReferenceHobFactorInput` | kisscalc_methods |
| `SetToothThicknessReferenceHobLengthInput` | kisscalc_methods |
| `SetTopCrowning` | kisscalc_methods |
| `SetWidthFactor` | kisscalc_methods |
| `SetXFactorHighPriority` | kisscalc_methods |
| `SetupConvertTipFormHeight` | kisscalc_methods |
| `SetupProfileFlanklineDiagram` | kisscalc_methods |
| `ShowDialog` | skript |
| `ShowGraphic` | deep_test |
| `Text` | deep_test |
| `WriteMeasurementGridReport` | kisscalc_methods |
| `calcGrindingDiameter` | kisscalc_methods |
| `calculateDrawingResults` | kisscalc_methods |
| `calculateMasterGear` | kisscalc_methods |
| `calculateMeasuringGrid` | kisscalc_methods |
| `calculateModificationFineSizing` | kisscalc_methods |
| `calculateScoringResults` | kisscalc_methods |
| `calculateSizeCenterDistance` | kisscalc_methods |

## 执行时抛出异常的函数

| 函数名 | 来源 | 状态 |
|--------|------|------|
| `CalculateMeasurementGridGDE` | kisscalc_methods | unknown_exception |
| `ExportToothForm` | kisscalc_methods | unknown_exception |
| `GetMittelPunkte` | kisscalc_methods | raw |
| `Message` | kisscalc_methods | raw |
| `SaveFile` | kisscalc_methods | raw |
| `calculateDeltaH` | kisscalc_methods | raw |

## 未确认/未暴露的函数 (not_implemented)

共有 **869** 个候选函数名返回 `not_implemented`（函数名不存在或未通过 COM 暴露）。
典型例子包括：

- 脚本语言数学/系统内置函数：`abs`, `sqrt`, `min`, `max`, `floor`, `round`, `degrees`, `pi`, `size`, `square`, `to_string` 等。
- UI/交互函数：`addItem`, `defineGearPair`, `defineBoundary`, `roughSizingGearbox`, `ShowDialog`, `Message`, `CoordinateSystem` 等。
- 图形绘制函数：`Circle`, `Line`, `Text`（无参数时）等。
- 报告函数：`ReportWithParameters` 等。

完整未确认列表见附录 A。

## 最有趣的发现

1. **`GetVar`/`SetVar` 不是内部函数**：通过 `CallJsonFunc` 调用 `GetVar`/`SetVar` 返回 `not_implemented`。它们是 COM 对象 `ks.GetVar(name)` / `ks.SetVar(name, value)` 的顶层方法。
2. **`GenerateReport` 需要报告模板路径**：无参数调用返回 `bad_function_call`；传入 `rpt\Z010Commente.rpt` 后成功生成临时报告文件，如 `C:/Windows/TEMP/KISS_9\Z012.pprpt`。
3. **`Calculate` 类函数最稳定**：`Calculate`、`CalculateStdCA`、`CalculateCA`、`CalculateFineSizing`、`CalculateLifeTime` 等多数无参数调用返回 `ok`。
4. **脚本语言函数与 COM 暴露函数差异大**：`.skript` 文件中大量函数（如数学函数、图形函数、UI 函数）在 COM 层不可用，只有 `Calculate`、`CalculateStdCA`、`GetConsistency`、`LoadFile`、`ModuleID`、`Temp_Dir`、`Execute` 等少数被确认。
5. **`CallFunc`/`CallFuncNParam` 可用性有限**：`CallFunc` 对无参数函数返回 `None`，对 `LoadFile`/`Execute`/`SaveFile` 抛出服务器异常；`CallFuncNParam` 需要 `[name, ...args]` 形式但只返回 `None`，无法通过返回值判断函数是否存在。
6. **参数化的内部函数**：`CalculateOptionsForX` 带参数 `0.5` 成功返回数值 `0.270645...`，说明内部函数可以接受参数并通过 `CallJsonFunc` 返回结果。

## 附录 A：完整候选函数测试结果

| 函数名 | 来源 | CallJsonFunc 状态 | 返回值 |
|--------|------|---------------------|--------|
| `BerechneKegelRadInSektion` | kisscalc_methods | not_implemented |  |
| `BerechnenOhneSetzen` | kisscalc_methods | not_implemented |  |
| `Berechnung` | kisscalc_methods | not_implemented |  |
| `Calc` | kisscalc_methods | not_implemented |  |
| `CalcAngleOrTorque` | kisscalc_methods | not_implemented |  |
| `CalcAnziehfaktor` | kisscalc_methods | not_implemented |  |
| `CalcChamferDimension` | kisscalc_methods | not_implemented |  |
| `CalcDiameterLength` | kisscalc_methods | not_implemented |  |
| `CalcDiameterTorqueAngle` | kisscalc_methods | not_implemented |  |
| `CalcFestigkeit` | kisscalc_methods | not_implemented |  |
| `CalcFestigkeitCore` | kisscalc_methods | not_implemented |  |
| `CalcGear` | kisscalc_methods | not_implemented |  |
| `CalcGeometrie1Stirn` | kisscalc_methods | not_implemented |  |
| `CalcGeometrie2Stirn` | kisscalc_methods | not_implemented |  |
| `CalcGeometrie3StirnINKLzahnform` | kisscalc_methods | not_implemented |  |
| `CalcGeometrie3StirnOHNEzahnform` | kisscalc_methods | not_implemented |  |
| `CalcHaerte` | kisscalc_methods | not_implemented |  |
| `CalcHerstellung` | kisscalc_methods | not_implemented |  |
| `CalcHobbingProcess` | kisscalc_methods | ok |  |
| `CalcKSB` | kisscalc_methods | not_implemented |  |
| `CalcKontrollmasseStirn` | kisscalc_methods | not_implemented |  |
| `CalcLengthOfEngagement` | kisscalc_methods | not_implemented |  |
| `CalcRollGeometrie` | kisscalc_methods | not_implemented |  |
| `CalcSafetyTooth_MeasuredTorque` | kisscalc_methods | ok | 0 |
| `CalcSizing` | kisscalc_methods | not_implemented |  |
| `CalcSpannrolle` | kisscalc_methods | not_implemented |  |
| `CalcToothForm` | kisscalc_methods | not_implemented |  |
| `CalcToothThicknessAllowances` | kisscalc_methods | bad_function_call |  |
| `CalcW050` | kisscalc_methods | not_implemented |  |
| `CalcW060` | kisscalc_methods | not_implemented |  |
| `CalcW100` | kisscalc_methods | not_implemented |  |
| `CalcWithSKFProgram` | kisscalc_methods | not_implemented |  |
| `CalcZahn` | kisscalc_methods | not_implemented |  |
| `Calc_dt_dr_from_dxdydzdata` | kisscalc_methods | not_implemented |  |
| `Calculate` | deep_test | ok | 1 |
| `Calculate2DGeometry` | kisscalc_methods | not_implemented |  |
| `CalculateAccordingToMethod` | kisscalc_methods | not_implemented |  |
| `CalculateAddendumDedendumAngle` | kisscalc_methods | not_implemented |  |
| `CalculateAddendumHeight` | kisscalc_methods | ok |  |
| `CalculateAndSize` | kisscalc_methods | not_implemented |  |
| `CalculateAuxilliaryAngles` | kisscalc_methods | not_implemented |  |
| `CalculateCA` | deep_test | ok | True |
| `CalculateCAStep` | kisscalc_methods | bad_function_call |  |
| `CalculateCenterDistanceAngle` | kisscalc_methods | ok |  |
| `CalculateConvertLeadAngle` | kisscalc_methods | not_implemented |  |
| `CalculateConvertReferenceProfile` | kisscalc_methods | not_implemented |  |
| `CalculateCutterRadius` | kisscalc_methods | not_implemented |  |
| `CalculateDedendumHeight` | kisscalc_methods | ok |  |
| `CalculateF060` | kisscalc_methods | not_implemented |  |
| `CalculateFineSizing` | deep_test | ok |  |
| `CalculateFlankBreaking` | kisscalc_methods | not_implemented |  |
| `CalculateFlankBreakingISO` | kisscalc_methods | not_implemented |  |
| `CalculateGear` | kisscalc_methods | not_implemented |  |
| `CalculateGearPump` | kisscalc_methods | ok |  |
| `CalculateGleasonConversion` | kisscalc_methods | not_implemented |  |
| `CalculateGleasonInput` | kisscalc_methods | not_implemented |  |
| `CalculateGridingDiameter` | kisscalc_methods | ok |  |
| `CalculateGrindingDistance` | kisscalc_methods | ok |  |
| `CalculateHerringboneGrooveWidth` | kisscalc_methods | bad_function_call |  |
| `CalculateHertzianPressure` | kisscalc_methods | not_implemented |  |
| `CalculateImportManufacturingDeviations` | kisscalc_methods | bad_function_call |  |
| `CalculateImportTopoDeviations` | kisscalc_methods | not_implemented |  |
| `CalculateInertia` | kisscalc_methods | not_implemented |  |
| `CalculateKHbeta` | kisscalc_methods | bad_function_call |  |
| `CalculateLager2HP` | kisscalc_methods | not_implemented |  |
| `CalculateLager2HPSystem` | kisscalc_methods | not_implemented |  |
| `CalculateLeadAngle` | kisscalc_methods | ok |  |
| `CalculateLeftAndRight` | kisscalc_methods | not_implemented |  |
| `CalculateLifeTime` | deep_test | ok |  |
| `CalculateLifeTimeKS` | kisscalc_methods | not_implemented |  |
| `CalculateMasterGear` | kisscalc_methods | not_implemented |  |
| `CalculateMaximumRootRoundingInvolute` | kisscalc_methods | ok |  |
| `CalculateMaximumTipRounding` | kisscalc_methods | bad_function_call |  |
| `CalculateMaximumTipRoundingAsymmetric` | kisscalc_methods | not_implemented |  |
| `CalculateMeasurementGridGDE` | kisscalc_methods | unknown_exception | An unknown exception occurred |
| `CalculateMfgDevModification` | kisscalc_methods | not_implemented |  |
| `CalculateMfgDevTemplateFactors` | kisscalc_methods | not_implemented |  |
| `CalculateModalAnalysis` | kisscalc_methods | not_implemented |  |
| `CalculateMultiplePressFit` | kisscalc_methods | not_implemented |  |
| `CalculateNormalModule` | kisscalc_methods | ok |  |
| `CalculateNumber` | kisscalc_methods | not_implemented |  |
| `CalculateNumberOfSlices` | kisscalc_methods | not_implemented |  |
| `CalculateOB` | kisscalc_methods | ok |  |
| `CalculateOperatingBacklash` | deep_test | ok |  |
| `CalculateOpt` | kisscalc_methods | not_implemented |  |
| `CalculateOptionsForX` | deep_test | ok | 0.2706453579469703 |
| `CalculatePower` | kisscalc_methods | ok |  |
| `CalculatePriority` | kisscalc_methods | not_implemented |  |
| `CalculateProtuberanceAngle` | kisscalc_methods | ok |  |
| `CalculateProtuberanceHeight` | kisscalc_methods | ok |  |
| `CalculateRetVal` | kisscalc_methods | not_implemented |  |
| `CalculateRoughSizing` | kisscalc_methods | not_implemented |  |
| `CalculateSectionParameters` | kisscalc_methods | not_implemented |  |
| `CalculateSectionsForContactAnalysis` | kisscalc_methods | not_implemented |  |
| `CalculateSectionsZF` | kisscalc_methods | not_implemented |  |
| `CalculateSectionsZFPerTooth` | kisscalc_methods | not_implemented |  |
| `CalculateServiceSpeed` | kisscalc_methods | not_implemented |  |
| `CalculateStdCA` | deep_test | ok | True |
| `CalculateSystemFrequencies` | kisscalc_methods | not_implemented |  |
| `CalculateSystemZFTR06` | kisscalc_methods | not_implemented |  |
| `CalculateTheoreticalInvolute` | kisscalc_methods | not_implemented |  |
| `CalculateThermalRating` | kisscalc_methods | not_implemented |  |
| `CalculateTipAlteration` | kisscalc_methods | ok |  |
| `CalculateTipFormHeight` | kisscalc_methods | bad_function_call |  |
| `CalculateTipRounding` | kisscalc_methods | bad_function_call |  |
| `CalculateTolerance` | kisscalc_methods | not_implemented |  |
| `CalculateTolerances` | kisscalc_methods | bad_function_call |  |
| `CalculateToothForm` | deep_test | bad_function_call |  |
| `CalculateToothThicknessCalculation` | kisscalc_methods | ok |  |
| `CalculateToothThicknessChange` | kisscalc_methods | ok |  |
| `CalculateTopologyModification` | kisscalc_methods | not_implemented |  |
| `CalculateTotalNumberOfSlices` | kisscalc_methods | not_implemented |  |
| `CalculateWaterAbsorption` | kisscalc_methods | ok |  |
| `CalculateZFLKimport` | kisscalc_methods | not_implemented |  |
| `CalculateZFSectionAtZpos` | kisscalc_methods | not_implemented |  |
| `CalculateZFTR06` | kisscalc_methods | bad_function_call |  |
| `CalculateZFTR06specialCalc` | kisscalc_methods | not_implemented |  |
| `Calculate_dFa` | kisscalc_methods | not_implemented |  |
| `CalculatedNa` | kisscalc_methods | ok |  |
| `CalculatedNf` | kisscalc_methods | ok |  |
| `CalculationNeedsSlices` | kisscalc_methods | not_implemented |  |
| `CallFunc` | kisscalc_methods | not_implemented |  |
| `Circle` | deep_test | bad_function_call |  |
| `Close` | kisscalc_methods | not_implemented |  |
| `CloseFile` | kisscalc_methods | not_implemented |  |
| `CreateReport` | kisscalc_methods | not_implemented |  |
| `CreateReportVar` | kisscalc_methods | bad_function_call |  |
| `DoCalculate` | kisscalc_methods | not_implemented |  |
| `DoCalculateOnlyGeometry` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AbwaelzenFraeser` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AbwaelzenStossrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AbwaelzenmitGegenrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ApplyConicity` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AutoKopfRundung` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AutoKopfkantenbruch` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AutomaticFirstStep` | kisscalc_methods | not_implemented |  |
| `DoCalculate_AutomaticModification` | kisscalc_methods | not_implemented |  |
| `DoCalculate_BPberechnen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Beloteinlesen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_CutTipDiameter` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Cycloide` | kisscalc_methods | not_implemented |  |
| `DoCalculate_EllipticTension` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ElliptischeFussmodifikation` | kisscalc_methods | not_implemented |  |
| `DoCalculate_FinalTreatment` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Fussradius` | kisscalc_methods | not_implemented |  |
| `DoCalculate_GeradlinigeFlanke` | kisscalc_methods | not_implemented |  |
| `DoCalculate_HirnProfilkorrektur` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Kopfkantenbruch` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Kopfrundung` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Korrekturen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Kreisbogen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Kronenrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_KronenradmitStossrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_LineareProfilkorrektur` | kisscalc_methods | not_implemented |  |
| `DoCalculate_LogarithmischeProfilkorrektur` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ModifikationErodieren` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ModifikationFormenbau` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ModifikationenStossrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_PreTreatment` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ProgressiveProfilkorrektur` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Punkteeinlesen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_RadDaten` | kisscalc_methods | not_implemented |  |
| `DoCalculate_RadialeVerschiebung` | kisscalc_methods | not_implemented |  |
| `DoCalculate_SchneckeAxialschnitteinlesen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_SchneckeErzeugen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Stirnradeinlesen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_StirnradmiteingelesenemAbwaelzfraeser` | kisscalc_methods | not_implemented |  |
| `DoCalculate_StirnradmiteingelesenemAbwaelzfraeser_NEW` | kisscalc_methods | not_implemented |  |
| `DoCalculate_StirnradmiteingelesenemStossrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_Stossradberechnen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_TheoretischeEvolvente` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ZahndickenModifikation` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ZahnstangeEinlesen` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ZahnstangemitStossrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_ZahnstangemiteingelesenemStossrad` | kisscalc_methods | not_implemented |  |
| `DoCalculate_alfan` | kisscalc_methods | not_implemented |  |
| `DoCalculate_beta` | kisscalc_methods | not_implemented |  |
| `DrawGrafik` | kisscalc_methods | not_implemented |  |
| `ExecFile` | kisscalc_methods | not_implemented |  |
| `Execute` | deep_test | ok |  |
| `Export` | kisscalc_methods | not_implemented |  |
| `Export3DGeometry` | kisscalc_methods | not_implemented |  |
| `ExportGear3D_` | kisscalc_methods | not_implemented |  |
| `ExportGraphic` | kisscalc_methods | not_implemented |  |
| `ExportGraphicAsDXF` | kisscalc_methods | bad_function_call |  |
| `ExportPair` | kisscalc_methods | not_implemented |  |
| `ExportSingleGear` | kisscalc_methods | not_implemented |  |
| `ExportToKISSsoftModule` | kisscalc_methods | not_implemented |  |
| `ExportToothForm` | kisscalc_methods | unknown_exception | An unknown exception occurred |
| `ExportZFLKdamageMatrix` | kisscalc_methods | not_implemented |  |
| `Find` | kisscalc_methods | not_implemented |  |
| `FindInnerContourElement` | kisscalc_methods | not_implemented |  |
| `FindMinMax` | kisscalc_methods | not_implemented |  |
| `FindOuterContourElement` | kisscalc_methods | not_implemented |  |
| `FindShoulder` | kisscalc_methods | not_implemented |  |
| `GenerateDrawingData` | kisscalc_methods | not_implemented |  |
| `GenerateGears3D` | kisscalc_methods | not_implemented |  |
| `GenerateHtmlOutput` | kisscalc_methods | not_implemented |  |
| `GenerateImage` | kisscalc_methods | bad_function_call |  |
| `GenerateReport` | deep_test | ok | C:/Windows/TEMP/KISS_9\Z012.pp |
| `GenerateResultReport` | kisscalc_methods | not_implemented |  |
| `GenerateUIVar` | skript | bad_function_call |  |
| `GenerateUserResultReport` | kisscalc_methods | not_implemented |  |
| `Get` | kisscalc_methods | not_implemented |  |
| `GetAAZABR07` | kisscalc_methods | not_implemented |  |
| `GetAdditionalSections` | kisscalc_methods | not_implemented |  |
| `GetAsymmetricCount` | deep_test | ok | 4 |
| `GetBasisDatenInSchnitt` | kisscalc_methods | not_implemented |  |
| `GetBetaConfiguration` | kisscalc_methods | not_implemented |  |
| `GetBetaGearIndex` | kisscalc_methods | not_implemented |  |
| `GetCalcCount` | kisscalc_methods | not_implemented |  |
| `GetCalcGeometrie` | kisscalc_methods | not_implemented |  |
| `GetCalculationContext` | kisscalc_methods | not_implemented |  |
| `GetCallerID` | kisscalc_methods | not_implemented |  |
| `GetCenterDistanceType` | kisscalc_methods | not_implemented |  |
| `GetComment` | kisscalc_methods | not_implemented |  |
| `GetConnectionCount` | kisscalc_methods | not_implemented |  |
| `GetConsistency` | deep_test | ok | 1 |
| `GetCrossSectionCount` | kisscalc_methods | not_implemented |  |
| `GetCrossSectionTypeName` | kisscalc_methods | not_implemented |  |
| `GetCrowning` | kisscalc_methods | bad_function_call |  |
| `GetCyclesAutomatic` | kisscalc_methods | bad_function_call |  |
| `GetCyclesInput` | kisscalc_methods | bad_function_call |  |
| `GetCyclesPerRotation` | kisscalc_methods | bad_function_call |  |
| `GetDiagramName` | kisscalc_methods | not_implemented |  |
| `GetDiameterAt` | kisscalc_methods | not_implemented |  |
| `GetDiameterOfDrillAt` | kisscalc_methods | not_implemented |  |
| `GetDiameters` | kisscalc_methods | not_implemented |  |
| `GetDisplacedGeneration_mn` | kisscalc_methods | not_implemented |  |
| `GetDocuPointCount` | kisscalc_methods | not_implemented |  |
| `GetFactorCrowning` | kisscalc_methods | bad_function_call |  |
| `GetFactorEccentricity` | kisscalc_methods | bad_function_call |  |
| `GetFileExtension` | kisscalc_methods | not_implemented |  |
| `GetFileName` | kisscalc_methods | not_implemented |  |
| `GetFileVersion` | kisscalc_methods | not_implemented |  |
| `GetFilletPoints` | kisscalc_methods | not_implemented |  |
| `GetFormula` | kisscalc_methods | not_implemented |  |
| `GetFullOutputFileName` | kisscalc_methods | not_implemented |  |
| `GetGearCount` | deep_test | ok | 2 |
| `GetGearNr` | kisscalc_methods | not_implemented |  |
| `GetGearNrFromName` | kisscalc_methods | not_implemented |  |
| `GetGenerationType` | kisscalc_methods | not_implemented |  |
| `GetGeometryFromDXF` | kisscalc_methods | not_implemented |  |
| `GetGlobalLubricant` | kisscalc_methods | not_implemented |  |
| `GetHVValue` | kisscalc_methods | not_implemented |  |
| `GetHandOfGear` | kisscalc_methods | not_implemented |  |
| `GetHardnessCount` | deep_test | ok | 4 |
| `GetHelixAngle` | kisscalc_methods | bad_function_call |  |
| `GetHelpId` | kisscalc_methods | not_implemented |  |
| `GetISOorDINCalc` | kisscalc_methods | not_implemented |  |
| `GetInfoOfCalc` | kisscalc_methods | not_implemented |  |
| `GetInfoOfCrossSection` | kisscalc_methods | not_implemented |  |
| `GetInfoOfDocuPoint` | kisscalc_methods | not_implemented |  |
| `GetInfoOfObject` | kisscalc_methods | not_implemented |  |
| `GetItemModel` | kisscalc_methods | not_implemented |  |
| `GetKegelAuslegung` | kisscalc_methods | not_implemented |  |
| `GetKegelModulUmrechnen` | kisscalc_methods | not_implemented |  |
| `GetKronenRadBasisRechnung` | kisscalc_methods | not_implemented |  |
| `GetLager2HPSystemData` | kisscalc_methods | not_implemented |  |
| `GetLehrzahnradNachDIN3970` | kisscalc_methods | not_implemented |  |
| `GetLifetime` | kisscalc_methods | not_implemented |  |
| `GetLocker` | kisscalc_methods | not_implemented |  |
| `GetMaterial` | kisscalc_methods | not_implemented |  |
| `GetMaxPressure` | kisscalc_methods | not_implemented |  |
| `GetMeasurementGridReport` | kisscalc_methods | not_implemented |  |
| `GetMeta` | kisscalc_methods | not_implemented |  |
| `GetMetaMap` | kisscalc_methods | not_implemented |  |
| `GetMetaNameOfCalc` | kisscalc_methods | not_implemented |  |
| `GetMittelPunkte` | kisscalc_methods | raw |  |
| `GetModuleId` | kisscalc_methods | not_implemented |  |
| `GetModuleIdaskString` | kisscalc_methods | not_implemented |  |
| `GetModuleShell` | kisscalc_methods | not_implemented |  |
| `GetNameOfCalc` | kisscalc_methods | not_implemented |  |
| `GetNofSteps` | kisscalc_methods | not_implemented |  |
| `GetPairCount` | deep_test | ok | 1 |
| `GetParam` | kisscalc_methods | not_implemented |  |
| `GetPoolId` | kisscalc_methods | not_implemented |  |
| `GetPositionOfStartingAngle` | kisscalc_methods | not_implemented |  |
| `GetProfileDiagramLmaxLmin` | kisscalc_methods | not_implemented |  |
| `GetRadKunstStoff` | kisscalc_methods | not_implemented |  |
| `GetReducerType` | deep_test | ok |  |
| `GetRefProfileType` | deep_test | ok | 2 |
| `GetRegisteredModules` | kisscalc_methods | not_implemented |  |
| `GetRelativeFileName` | kisscalc_methods | not_implemented |  |
| `GetReport` | kisscalc_methods | not_implemented |  |
| `GetReportName` | kisscalc_methods | not_implemented |  |
| `GetReportTitle` | kisscalc_methods | not_implemented |  |
| `GetResult` | kisscalc_methods | not_implemented |  |
| `GetResultName` | kisscalc_methods | not_implemented |  |
| `GetResultW030` | kisscalc_methods | not_implemented |  |
| `GetRzAtPosition` | kisscalc_methods | not_implemented |  |
| `GetSTIRNRADausZAHNST` | kisscalc_methods | not_implemented |  |
| `GetSeed` | kisscalc_methods | not_implemented |  |
| `GetSenseOfRotation` | kisscalc_methods | not_implemented |  |
| `GetShaftCount` | kisscalc_methods | not_implemented |  |
| `GetSharedInstance` | kisscalc_methods | not_implemented |  |
| `GetSingleGearGeometry` | kisscalc_methods | not_implemented |  |
| `GetStraightness` | kisscalc_methods | not_implemented |  |
| `GetSwitchMatrixFromFile` | kisscalc_methods | not_implemented |  |
| `GetTighteningTorqueFactorMethod` | kisscalc_methods | not_implemented |  |
| `GetTipRoundingOrChamfer` | kisscalc_methods | not_implemented |  |
| `GetTmpDir` | kisscalc_methods | not_implemented |  |
| `GetToolInputTypeFromName` | kisscalc_methods | not_implemented |  |
| `GetToolTypeFromName` | kisscalc_methods | not_implemented |  |
| `GetTotalWidth` | kisscalc_methods | not_implemented |  |
| `GetVar` | kisscalc_methods | not_implemented |  |
| `GetVariantsFromFile` | kisscalc_methods | not_implemented |  |
| `GetWidthFactor` | kisscalc_methods | bad_function_call |  |
| `GetXSize` | kisscalc_methods | not_implemented |  |
| `GetZAHNSTausSTIRNRAD` | kisscalc_methods | not_implemented |  |
| `GetZPPCount` | deep_test | ok | 2 |
| `GetZahnDicken` | kisscalc_methods | not_implemented |  |
| `Get_AddendumGear` | kisscalc_methods | not_implemented |  |
| `Get_GrindingFormHeightOnGear` | kisscalc_methods | not_implemented |  |
| `Get_GrindingTipRadius` | kisscalc_methods | not_implemented |  |
| `Get_GrindingToolTipFormHeight` | kisscalc_methods | not_implemented |  |
| `Get_GrindingToolTipHeight` | kisscalc_methods | not_implemented |  |
| `Get_NormalModuleTool` | kisscalc_methods | not_implemented |  |
| `Get_PressureAngleTool` | kisscalc_methods | not_implemented |  |
| `Get_ProtuberanceAngle` | kisscalc_methods | not_implemented |  |
| `Get_ProtuberanceHeight` | kisscalc_methods | not_implemented |  |
| `Get_RampAngle` | kisscalc_methods | not_implemented |  |
| `Get_RootFormHeight` | kisscalc_methods | not_implemented |  |
| `Get_RootHeight` | kisscalc_methods | not_implemented |  |
| `Get_RootRadius` | kisscalc_methods | not_implemented |  |
| `Get_TipChamferAngle` | kisscalc_methods | not_implemented |  |
| `Get_TipChamferLength` | kisscalc_methods | not_implemented |  |
| `Get_TipFormHeight` | kisscalc_methods | not_implemented |  |
| `Get_TipHeight` | kisscalc_methods | not_implemented |  |
| `Get_TipRadius` | kisscalc_methods | not_implemented |  |
| `Get_ToothThicknessReferenceHob` | kisscalc_methods | not_implemented |  |
| `Get_alf_prP` | kisscalc_methods | not_implemented |  |
| `Get_dFa` | kisscalc_methods | not_implemented |  |
| `Get_dFa0` | kisscalc_methods | not_implemented |  |
| `Get_dFf` | kisscalc_methods | not_implemented |  |
| `Get_dFf0` | kisscalc_methods | not_implemented |  |
| `Get_da` | kisscalc_methods | not_implemented |  |
| `Get_da0` | kisscalc_methods | not_implemented |  |
| `Get_delH` | kisscalc_methods | not_implemented |  |
| `Get_df` | kisscalc_methods | not_implemented |  |
| `Get_df0` | kisscalc_methods | not_implemented |  |
| `Get_haP` | kisscalc_methods | not_implemented |  |
| `Get_haP0` | kisscalc_methods | not_implemented |  |
| `Get_haP0_pinionCutter` | kisscalc_methods | not_implemented |  |
| `Get_haP_or_hfP` | kisscalc_methods | not_implemented |  |
| `Get_hfP` | kisscalc_methods | not_implemented |  |
| `Get_hfP0` | kisscalc_methods | not_implemented |  |
| `Get_hfP_InternalGears` | kisscalc_methods | not_implemented |  |
| `Get_hprP` | kisscalc_methods | not_implemented |  |
| `Get_m0` | kisscalc_methods | not_implemented |  |
| `Get_rhoaP_tool` | kisscalc_methods | not_implemented |  |
| `Get_xE` | kisscalc_methods | not_implemented |  |
| `Import` | kisscalc_methods | not_implemented |  |
| `InitGrafik` | kisscalc_methods | not_implemented |  |
| `InterpretGrafik` | kisscalc_methods | not_implemented |  |
| `Line` | deep_test | bad_function_call |  |
| `LoadFile` | deep_test | ok |  |
| `Message` | kisscalc_methods | raw |  |
| `Modify` | kisscalc_methods | not_implemented |  |
| `Module` | kisscalc_methods | not_implemented |  |
| `ModuleID` | skript | ok | Z012 |
| `New` | kisscalc_methods | not_implemented |  |
| `NewFile` | kisscalc_methods | not_implemented |  |
| `NewGraphic` | deep_test | bad_function_call |  |
| `OpenFile` | kisscalc_methods | not_implemented |  |
| `Pi` | kisscalc_methods | not_implemented |  |
| `Position` | kisscalc_methods | not_implemented |  |
| `PrintGraphic` | kisscalc_methods | not_implemented |  |
| `ReCalc` | kisscalc_methods | not_implemented |  |
| `ReCalculate` | kisscalc_methods | not_implemented |  |
| `Read` | kisscalc_methods | not_implemented |  |
| `ReadAchsabstandsToleranzen` | kisscalc_methods | not_implemented |  |
| `ReadAlleZugabeVorbearbeitung` | kisscalc_methods | not_implemented |  |
| `ReadAlleZugabeVorbearbeitungFeinauslegung` | kisscalc_methods | not_implemented |  |
| `ReadFineSizingTools` | kisscalc_methods | bad_function_call |  |
| `ReadFusskreisToleranzen` | kisscalc_methods | not_implemented |  |
| `ReadHiddenDBPosition` | kisscalc_methods | not_implemented |  |
| `ReadInTolFile` | kisscalc_methods | not_implemented |  |
| `ReadKettenData` | kisscalc_methods | not_implemented |  |
| `ReadKopfkreisToleranzen` | kisscalc_methods | not_implemented |  |
| `ReadMaterialData` | kisscalc_methods | not_implemented |  |
| `ReadMeasurementData` | kisscalc_methods | not_implemented |  |
| `ReadMfgDeviation` | kisscalc_methods | not_implemented |  |
| `ReadPositionsFile` | kisscalc_methods | not_implemented |  |
| `ReadRotCAD` | kisscalc_methods | not_implemented |  |
| `ReadToleranceData` | kisscalc_methods | not_implemented |  |
| `ReadTolerances` | kisscalc_methods | not_implemented |  |
| `ReadZahndickenToleranzen` | kisscalc_methods | not_implemented |  |
| `ReadZugabeVorbearbeitung` | kisscalc_methods | not_implemented |  |
| `ReleaseModule` | kisscalc_methods | not_implemented |  |
| `ReportWithParameters` | kisscalc_methods | not_implemented |  |
| `Run` | kisscalc_methods | not_implemented |  |
| `SHIFT` | kisscalc_methods | not_implemented |  |
| `Safety` | kisscalc_methods | not_implemented |  |
| `SaveAs` | kisscalc_methods | not_implemented |  |
| `SaveFile` | kisscalc_methods | raw |  |
| `Set` | kisscalc_methods | not_implemented |  |
| `SetAGMAData` | kisscalc_methods | not_implemented |  |
| `SetAInput` | kisscalc_methods | bad_function_call |  |
| `SetAktualisieren` | kisscalc_methods | not_implemented |  |
| `SetAlphaValue` | kisscalc_methods | not_implemented |  |
| `SetAsnFromMd2r` | kisscalc_methods | not_implemented |  |
| `SetAsnFromMdk` | kisscalc_methods | not_implemented |  |
| `SetAutoContents` | kisscalc_methods | not_implemented |  |
| `SetAutoReportTitle` | kisscalc_methods | not_implemented |  |
| `SetBetaConfiguration` | kisscalc_methods | not_implemented |  |
| `SetCallback` | kisscalc_methods | not_implemented |  |
| `SetCallerID` | kisscalc_methods | not_implemented |  |
| `SetCenterDistanceBlock` | kisscalc_methods | bad_function_call |  |
| `SetCenterDistanceTolerances` | deep_test | ok |  |
| `SetCenterDistanceType` | kisscalc_methods | not_implemented |  |
| `SetColor` | skript | bad_function_call |  |
| `SetConsistency` | kisscalc_methods | bad_function_call |  |
| `SetCorrFactorChurningLossesStatus` | kisscalc_methods | not_implemented |  |
| `SetCorrFactorSealLossesStatus` | kisscalc_methods | not_implemented |  |
| `SetCrowning` | kisscalc_methods | bad_function_call |  |
| `SetCyclesAutomatic` | kisscalc_methods | bad_function_call |  |
| `SetCyclesInput` | kisscalc_methods | bad_function_call |  |
| `SetCyclesPerRotation` | kisscalc_methods | bad_function_call |  |
| `SetDataForCurrentMethod` | kisscalc_methods | not_implemented |  |
| `SetDebugFile` | kisscalc_methods | not_implemented |  |
| `SetDefaultLengthOfEngagement` | kisscalc_methods | not_implemented |  |
| `SetEffectOfNotch` | kisscalc_methods | not_implemented |  |
| `SetFactorCrowning` | kisscalc_methods | bad_function_call |  |
| `SetFactorEccentricity` | kisscalc_methods | bad_function_call |  |
| `SetFileName` | kisscalc_methods | not_implemented |  |
| `SetFileNameStatus` | kisscalc_methods | not_implemented |  |
| `SetFlag` | kisscalc_methods | not_implemented |  |
| `SetGenerationType` | kisscalc_methods | not_implemented |  |
| `SetGrindingBlockInputFactor` | kisscalc_methods | bad_function_call |  |
| `SetGrindingBlockInputLength` | kisscalc_methods | bad_function_call |  |
| `SetGrooveDepth` | kisscalc_methods | not_implemented |  |
| `SetHandOfGear` | kisscalc_methods | not_implemented |  |
| `SetHasSpecial` | kisscalc_methods | not_implemented |  |
| `SetHelixAngle` | kisscalc_methods | bad_function_call |  |
| `SetISO23509TypII` | kisscalc_methods | not_implemented |  |
| `SetImProjekt` | kisscalc_methods | not_implemented |  |
| `SetInputAlpha1` | kisscalc_methods | not_implemented |  |
| `SetInputAlpha2` | kisscalc_methods | not_implemented |  |
| `SetInputConL0` | kisscalc_methods | not_implemented |  |
| `SetInputConL1` | kisscalc_methods | not_implemented |  |
| `SetInputConL2` | kisscalc_methods | not_implemented |  |
| `SetInputD` | kisscalc_methods | not_implemented |  |
| `SetInputD1` | kisscalc_methods | not_implemented |  |
| `SetInputD1e` | kisscalc_methods | not_implemented |  |
| `SetInputD1i` | kisscalc_methods | not_implemented |  |
| `SetInputD2` | kisscalc_methods | not_implemented |  |
| `SetInputD2e` | kisscalc_methods | not_implemented |  |
| `SetInputD2i` | kisscalc_methods | not_implemented |  |
| `SetInputDe` | kisscalc_methods | not_implemented |  |
| `SetInputDi` | kisscalc_methods | not_implemented |  |
| `SetInputF1` | kisscalc_methods | not_implemented |  |
| `SetInputF2` | kisscalc_methods | not_implemented |  |
| `SetInputFQ` | kisscalc_methods | not_implemented |  |
| `SetInputL0` | kisscalc_methods | not_implemented |  |
| `SetInputL1` | kisscalc_methods | not_implemented |  |
| `SetInputL2` | kisscalc_methods | not_implemented |  |
| `SetInputT1` | kisscalc_methods | not_implemented |  |
| `SetInputT2` | kisscalc_methods | not_implemented |  |
| `SetInputmges` | kisscalc_methods | not_implemented |  |
| `SetInputs1` | kisscalc_methods | not_implemented |  |
| `SetInputs2` | kisscalc_methods | not_implemented |  |
| `SetInputsQ` | kisscalc_methods | not_implemented |  |
| `SetInputvariTighteningTorque` | kisscalc_methods | not_implemented |  |
| `SetKonsistent` | kisscalc_methods | not_implemented |  |
| `SetLanguage` | kisscalc_methods | bad_function_call |  |
| `SetLocked` | kisscalc_methods | not_implemented |  |
| `SetLzInput` | kisscalc_methods | bad_function_call |  |
| `SetMainFolderStatus` | kisscalc_methods | not_implemented |  |
| `SetMaterialData` | kisscalc_methods | not_implemented |  |
| `SetMountingAngleStatus` | kisscalc_methods | not_implemented |  |
| `SetMultiplePressSit` | kisscalc_methods | not_implemented |  |
| `SetNamesOfGears` | kisscalc_methods | not_implemented |  |
| `SetNumTeethStatus` | kisscalc_methods | not_implemented |  |
| `SetOneRow` | kisscalc_methods | not_implemented |  |
| `SetParam` | kisscalc_methods | not_implemented |  |
| `SetPositionAccToCalc` | kisscalc_methods | not_implemented |  |
| `SetPositionAsInput` | kisscalc_methods | not_implemented |  |
| `SetPositionOfStartingAngle` | kisscalc_methods | not_implemented |  |
| `SetPowerGear` | kisscalc_methods | not_implemented |  |
| `SetRadioXsizing` | kisscalc_methods | bad_function_call |  |
| `SetRatio1Status` | kisscalc_methods | not_implemented |  |
| `SetRatio2Status` | kisscalc_methods | not_implemented |  |
| `SetRatio3Status` | kisscalc_methods | not_implemented |  |
| `SetRefProfile` | kisscalc_methods | not_implemented |  |
| `SetRefProfileDataForCurrentTool` | deep_test | ok |  |
| `SetReportTitle` | kisscalc_methods | not_implemented |  |
| `SetSenseOfRotation` | kisscalc_methods | not_implemented |  |
| `SetSilentMode` | kisscalc_methods | not_implemented |  |
| `SetSimpleReport` | kisscalc_methods | not_implemented |  |
| `SetSingleGearGeometry` | kisscalc_methods | not_implemented |  |
| `SetSpeedEfficiencyStatus` | kisscalc_methods | not_implemented |  |
| `SetSpeichern` | kisscalc_methods | not_implemented |  |
| `SetStressType` | kisscalc_methods | not_implemented |  |
| `SetTheReportTitle` | kisscalc_methods | not_implemented |  |
| `SetTipAlteration` | kisscalc_methods | bad_function_call |  |
| `SetTitle` | kisscalc_methods | not_implemented |  |
| `SetTolAsnBlock` | kisscalc_methods | bad_function_call |  |
| `SetToothThicknessReferenceHobFactorInput` | kisscalc_methods | bad_function_call |  |
| `SetToothThicknessReferenceHobLengthInput` | kisscalc_methods | bad_function_call |  |
| `SetToothThicknessTolerances` | deep_test | ok |  |
| `SetTopCrowning` | kisscalc_methods | bad_function_call |  |
| `SetTorqueSpeedWorkingFl_S20` | kisscalc_methods | not_implemented |  |
| `SetUnlockCode` | kisscalc_methods | not_implemented |  |
| `SetUnlocked` | kisscalc_methods | not_implemented |  |
| `SetVar` | kisscalc_methods | not_implemented |  |
| `SetVariable` | kisscalc_methods | not_implemented |  |
| `SetWidthFactor` | kisscalc_methods | bad_function_call |  |
| `SetXAxisFromDEFxAxis` | kisscalc_methods | not_implemented |  |
| `SetXFactorHighPriority` | kisscalc_methods | bad_function_call |  |
| `SetYAxisFromDEFyAxis` | kisscalc_methods | not_implemented |  |
| `Set_AddendumGear` | kisscalc_methods | not_implemented |  |
| `Set_GrindingFormHeightOnGear` | kisscalc_methods | not_implemented |  |
| `Set_GrindingTipRadius` | kisscalc_methods | not_implemented |  |
| `Set_GrindingToolTipFormHeight` | kisscalc_methods | not_implemented |  |
| `Set_GrindingToolTipHeight` | kisscalc_methods | not_implemented |  |
| `Set_NormalModuleTool` | kisscalc_methods | not_implemented |  |
| `Set_PressureAngleTool` | kisscalc_methods | not_implemented |  |
| `Set_ProtuberanceAngle` | kisscalc_methods | not_implemented |  |
| `Set_ProtuberanceHeight` | kisscalc_methods | not_implemented |  |
| `Set_RampAngle` | kisscalc_methods | not_implemented |  |
| `Set_RootFormHeight` | kisscalc_methods | not_implemented |  |
| `Set_RootHeight` | kisscalc_methods | not_implemented |  |
| `Set_RootRadius` | kisscalc_methods | not_implemented |  |
| `Set_TipChamferAngle` | kisscalc_methods | not_implemented |  |
| `Set_TipChamferLength` | kisscalc_methods | not_implemented |  |
| `Set_TipFormHeight` | kisscalc_methods | not_implemented |  |
| `Set_TipHeight` | kisscalc_methods | not_implemented |  |
| `Set_TipRadius` | kisscalc_methods | not_implemented |  |
| `Set_Tool_pr` | kisscalc_methods | not_implemented |  |
| `Set_ToothThicknessReferenceHob` | kisscalc_methods | not_implemented |  |
| `SetupCalculateZFTR06` | kisscalc_methods | ok |  |
| `SetupCalculationForAsymmetricGears` | kisscalc_methods | ok |  |
| `SetupCenterDistanceAngle` | kisscalc_methods | ok |  |
| `SetupConeAngles` | kisscalc_methods | not_implemented |  |
| `SetupConvertReferenceProfile` | kisscalc_methods | not_implemented |  |
| `SetupConvertRootAlteration` | kisscalc_methods | not_implemented |  |
| `SetupConvertTipAlteration` | kisscalc_methods | not_implemented |  |
| `SetupConvertTipFormHeight` | kisscalc_methods | bad_function_call |  |
| `SetupConvertXeToQ` | kisscalc_methods | ok |  |
| `SetupFineSizing` | kisscalc_methods | ok |  |
| `SetupFrequenciesCalculation` | kisscalc_methods | not_implemented |  |
| `SetupGleasonConversion` | kisscalc_methods | not_implemented |  |
| `SetupGrindingDistance` | kisscalc_methods | ok |  |
| `SetupImportManufacturingDeviations` | kisscalc_methods | ok |  |
| `SetupImportTopoDeviations` | kisscalc_methods | not_implemented |  |
| `SetupLengthOfEngagement` | kisscalc_methods | not_implemented |  |
| `SetupProfileFlanklineDiagram` | kisscalc_methods | bad_function_call |  |
| `SetupReferenceProfile` | kisscalc_methods | ok |  |
| `SetupReporting` | kisscalc_methods | not_implemented |  |
| `SetupRoughSizing` | kisscalc_methods | not_implemented |  |
| `SetupSClass` | kisscalc_methods | not_implemented |  |
| `SetupSizing` | kisscalc_methods | not_implemented |  |
| `SetupSizingDiameter` | kisscalc_methods | not_implemented |  |
| `SetupTighteningTorque` | kisscalc_methods | not_implemented |  |
| `SetupToothDiameterAllowances` | kisscalc_methods | ok |  |
| `SetupToothThicknessAllowances` | kisscalc_methods | ok |  |
| `SetupToothThicknessCalculation` | kisscalc_methods | ok |  |
| `SetupZFLKimport` | kisscalc_methods | not_implemented |  |
| `SetupZFexport` | kisscalc_methods | not_implemented |  |
| `Setup_ConvertXS` | kisscalc_methods | not_implemented |  |
| `ShowDialog` | skript | bad_function_call |  |
| `ShowGraphic` | deep_test | bad_function_call |  |
| `ShowInterface` | kisscalc_methods | not_implemented |  |
| `Spur` | kisscalc_methods | not_implemented |  |
| `Temp_Dir` | deep_test | ok | C:/Windows/TEMP/KISS_9\ |
| `Text` | deep_test | bad_function_call |  |
| `Update` | kisscalc_methods | not_implemented |  |
| `Write` | kisscalc_methods | not_implemented |  |
| `WriteGauge` | kisscalc_methods | not_implemented |  |
| `WriteMeasurementGridReport` | kisscalc_methods | bad_function_call |  |
| `WriteMfgDevTemplate` | kisscalc_methods | not_implemented |  |
| `WriteModuleVariables` | kisscalc_methods | not_implemented |  |
| `WriteSummary` | kisscalc_methods | ok | True |
| `abs` | kisscalc_methods | not_implemented |  |
| `addItem` | kisscalc_methods | not_implemented |  |
| `alf12_23` | kisscalc_methods | not_implemented |  |
| `alf23_34` | kisscalc_methods | not_implemented |  |
| `append_to_file` | kisscalc_methods | not_implemented |  |
| `calcExistsAlready` | kisscalc_methods | not_implemented |  |
| `calcGBodyDefFromMatrix` | kisscalc_methods | not_implemented |  |
| `calcGBodyStiffnessMatrix` | kisscalc_methods | not_implemented |  |
| `calcGrindingDiameter` | kisscalc_methods | bad_function_call |  |
| `calcMethodChanged` | kisscalc_methods | not_implemented |  |
| `calcModule` | kisscalc_methods | not_implemented |  |
| `calcName` | kisscalc_methods | not_implemented |  |
| `calcPermissiblePressure` | kisscalc_methods | not_implemented |  |
| `calcPowerflow` | kisscalc_methods | not_implemented |  |
| `calcRRelation` | kisscalc_methods | not_implemented |  |
| `calcSafetyFactor` | kisscalc_methods | not_implemented |  |
| `calcStats` | kisscalc_methods | not_implemented |  |
| `calcStatus` | kisscalc_methods | not_implemented |  |
| `calcStressesAndRelation` | kisscalc_methods | not_implemented |  |
| `calcTime` | kisscalc_methods | not_implemented |  |
| `calcTipClearance` | kisscalc_methods | not_implemented |  |
| `calcToothFlankArea` | kisscalc_methods | not_implemented |  |
| `calcToothHeightInner` | kisscalc_methods | not_implemented |  |
| `calcToothHeightInnerTheoretical` | kisscalc_methods | not_implemented |  |
| `calcToothHeightMiddle` | kisscalc_methods | not_implemented |  |
| `calcToothHeightMiddleTheoretical` | kisscalc_methods | not_implemented |  |
| `calcToothHeightOuter` | kisscalc_methods | not_implemented |  |
| `calcToothHeightOuterTheoretical` | kisscalc_methods | not_implemented |  |
| `calcToothTipWidth` | kisscalc_methods | not_implemented |  |
| `calcType` | kisscalc_methods | not_implemented |  |
| `calcUndercutAndMinTopland` | kisscalc_methods | not_implemented |  |
| `calcWithInnerRingModif` | kisscalc_methods | not_implemented |  |
| `calcWm` | kisscalc_methods | not_implemented |  |
| `calculate` | kisscalc_methods | not_implemented |  |
| `calculateAmplitudeSpectrum` | kisscalc_methods | not_implemented |  |
| `calculateAmplitudeSpectrumFromEntryPosition` | kisscalc_methods | not_implemented |  |
| `calculateAuxillaryResults` | kisscalc_methods | not_implemented |  |
| `calculateAverageValues` | kisscalc_methods | not_implemented |  |
| `calculateCases` | kisscalc_methods | not_implemented |  |
| `calculateCasingDeformationCore` | kisscalc_methods | not_implemented |  |
| `calculateCenterDistanceForSections` | kisscalc_methods | not_implemented |  |
| `calculateConicalBroadeningOfRim` | kisscalc_methods | not_implemented |  |
| `calculateContactAnalysis` | kisscalc_methods | ok |  |
| `calculateContactAnalysisAccuracy` | kisscalc_methods | not_implemented |  |
| `calculateContactAnalysisResults` | kisscalc_methods | ok |  |
| `calculateContactRatio` | kisscalc_methods | not_implemented |  |
| `calculateContactShift` | kisscalc_methods | not_implemented |  |
| `calculateCoordinates` | kisscalc_methods | not_implemented |  |
| `calculateCycles_VDI2736` | kisscalc_methods | not_implemented |  |
| `calculateCycles_Weibull` | kisscalc_methods | not_implemented |  |
| `calculateCycles_normalDistribution` | kisscalc_methods | not_implemented |  |
| `calculateDeflection` | kisscalc_methods | ok |  |
| `calculateDeflectionStiffness` | kisscalc_methods | ok |  |
| `calculateDeltaH` | kisscalc_methods | raw |  |
| `calculateDifferential` | kisscalc_methods | not_implemented |  |
| `calculateDrawingResults` | kisscalc_methods | bad_function_call |  |
| `calculateEmodulus` | kisscalc_methods | not_implemented |  |
| `calculateFlankLineDeflection` | kisscalc_methods | not_implemented |  |
| `calculateGearBodies` | kisscalc_methods | not_implemented |  |
| `calculateGearBody` | kisscalc_methods | not_implemented |  |
| `calculateGearBodyDeformation` | kisscalc_methods | not_implemented |  |
| `calculateGearBodyFromStiffnessMatrix` | kisscalc_methods | not_implemented |  |
| `calculateGearWithPowerSkivingTool` | kisscalc_methods | not_implemented |  |
| `calculateKHBeta` | kisscalc_methods | not_implemented |  |
| `calculateMasterGear` | kisscalc_methods | bad_function_call |  |
| `calculateMeasuringGrid` | kisscalc_methods | bad_function_call |  |
| `calculateMinMaxBacklash` | kisscalc_methods | not_implemented |  |
| `calculateMinMaxMedBacklashchange` | kisscalc_methods | not_implemented |  |
| `calculateModificationFineSizing` | kisscalc_methods | bad_function_call |  |
| `calculateModificationProposal` | kisscalc_methods | ok |  |
| `calculateNoBacklashCenterDistance` | kisscalc_methods | not_implemented |  |
| `calculateOilCoolerDissipation` | kisscalc_methods | not_implemented |  |
| `calculateOnlyKinematics` | kisscalc_methods | not_implemented |  |
| `calculateOperatingPitchDiameter` | kisscalc_methods | not_implemented |  |
| `calculatePathOfContact` | kisscalc_methods | not_implemented |  |
| `calculatePathOfContactForPair` | kisscalc_methods | not_implemented |  |
| `calculatePathOfContactForPlanet` | kisscalc_methods | not_implemented |  |
| `calculatePathOfContactWithProfileModifications` | kisscalc_methods | not_implemented |  |
| `calculatePinDeltaXZ` | kisscalc_methods | not_implemented |  |
| `calculateReactionAndStiffness` | kisscalc_methods | not_implemented |  |
| `calculateRegionOfContact` | kisscalc_methods | not_implemented |  |
| `calculateRootFormDiameter` | kisscalc_methods | not_implemented |  |
| `calculateRoughSizing` | kisscalc_methods | ok |  |
| `calculateScoringResults` | kisscalc_methods | bad_function_call |  |
| `calculateSealLosses` | kisscalc_methods | not_implemented |  |
| `calculateSizeCenterDistance` | kisscalc_methods | bad_function_call |  |
| `calculateStiffnessMatrix` | kisscalc_methods | not_implemented |  |
| `calculateSubModule` | kisscalc_methods | not_implemented |  |
| `calculateSystemBacklash` | kisscalc_methods | not_implemented |  |
| `calculateSystemInertia` | kisscalc_methods | not_implemented |  |
| `calculateSystemMassAndKineticEnergy` | kisscalc_methods | not_implemented |  |
| `calculateSystemTorsion` | kisscalc_methods | not_implemented |  |
| `calculateTopologyTemplateFactors` | kisscalc_methods | not_implemented |  |
| `calculateTorsion` | kisscalc_methods | not_implemented |  |
| `calculateTorsionAndModifications` | kisscalc_methods | not_implemented |  |
| `calculateTransmissionError` | kisscalc_methods | not_implemented |  |
| `calculateWear` | kisscalc_methods | not_implemented |  |
| `calculateWearFactor` | kisscalc_methods | not_implemented |  |
| `calculateWornToothform` | kisscalc_methods | not_implemented |  |
| `calculateXeFromTolerance` | kisscalc_methods | not_implemented |  |
| `calculate_dFa_dFf_fromToothForm` | kisscalc_methods | not_implemented |  |
| `calculate_hFfP_xe_from_hFaP0` | kisscalc_methods | not_implemented |  |
| `calculationMethodChanged` | kisscalc_methods | ok |  |
| `calculationNeedsFurtherIteration` | kisscalc_methods | not_implemented |  |
| `calculationTimeSec` | kisscalc_methods | not_implemented |  |
| `close_file` | kisscalc_methods | not_implemented |  |
| `coordinateSystem` | kisscalc_methods | not_implemented |  |
| `defineBoundary` | kisscalc_methods | not_implemented |  |
| `defineGearPair` | kisscalc_methods | not_implemented |  |
| `degrees` | kisscalc_methods | not_implemented |  |
| `distances` | kisscalc_methods | not_implemented |  |
| `execute` | kisscalc_methods | not_implemented |  |
| `exportAllCalculations` | kisscalc_methods | not_implemented |  |
| `exportCalculation` | kisscalc_methods | not_implemented |  |
| `exportData` | kisscalc_methods | not_implemented |  |
| `exportGDE` | kisscalc_methods | not_implemented |  |
| `exportGDEFunction` | kisscalc_methods | not_implemented |  |
| `exportGDEf` | kisscalc_methods | not_implemented |  |
| `exportMatingData` | kisscalc_methods | not_implemented |  |
| `exportModifications` | kisscalc_methods | not_implemented |  |
| `exportRexs` | kisscalc_methods | not_implemented |  |
| `exportRexs_cutter_wheel_tool` | kisscalc_methods | not_implemented |  |
| `exportRexs_cylindrical_gear` | kisscalc_methods | not_implemented |  |
| `exportRexs_cylindrical_gear_flank` | kisscalc_methods | not_implemented |  |
| `exportRexs_cylindrical_gear_manufacturing_settings` | kisscalc_methods | not_implemented |  |
| `exportRexs_cylindrical_stage` | kisscalc_methods | not_implemented |  |
| `exportRexs_cylindrical_stage_gear_data` | kisscalc_methods | not_implemented |  |
| `exportRexs_rack_shaped_tool` | kisscalc_methods | not_implemented |  |
| `exportSingleGearGDE` | kisscalc_methods | not_implemented |  |
| `exportSingleGearGDEf` | kisscalc_methods | not_implemented |  |
| `exportSpecialZF` | kisscalc_methods | not_implemented |  |
| `exportZFdamageMatrix` | kisscalc_methods | not_implemented |  |
| `exportZFstiffnessMatrix` | kisscalc_methods | not_implemented |  |
| `findAppropriateContact` | kisscalc_methods | not_implemented |  |
| `findCalculation` | kisscalc_methods | not_implemented |  |
| `findCombinations` | kisscalc_methods | not_implemented |  |
| `findDynamicGraphic` | kisscalc_methods | not_implemented |  |
| `findIntersectingFrequencies` | kisscalc_methods | not_implemented |  |
| `findObject` | kisscalc_methods | not_implemented |  |
| `findOrder` | kisscalc_methods | not_implemented |  |
| `findSectionFromPosition` | kisscalc_methods | not_implemented |  |
| `findShiftingAngleForTEforHelical` | kisscalc_methods | not_implemented |  |
| `findSimilarFrequencies` | kisscalc_methods | not_implemented |  |
| `findSystemZeroPoint` | kisscalc_methods | not_implemented |  |
| `floor` | kisscalc_methods | not_implemented |  |
| `gear` | kisscalc_methods | not_implemented |  |
| `gear2` | kisscalc_methods | not_implemented |  |
| `generateReport` | kisscalc_methods | not_implemented |  |
| `getAdditionalTorquesOf` | kisscalc_methods | not_implemented |  |
| `getAllConnectionCalcObjs` | kisscalc_methods | not_implemented |  |
| `getAllGearCalcObjs` | kisscalc_methods | not_implemented |  |
| `getAllGearNames` | kisscalc_methods | not_implemented |  |
| `getAllRotCadElements` | kisscalc_methods | not_implemented |  |
| `getAllRotCadElementsOfType` | kisscalc_methods | not_implemented |  |
| `getAllSwitchableObjs` | kisscalc_methods | not_implemented |  |
| `getAllTransmissionObjs` | kisscalc_methods | not_implemented |  |
| `getAllTransverseObjs` | kisscalc_methods | not_implemented |  |
| `getAlphaPos` | kisscalc_methods | not_implemented |  |
| `getAnglePhi` | kisscalc_methods | not_implemented |  |
| `getAnnotationWidgetInfo` | kisscalc_methods | not_implemented |  |
| `getAttributesOfComponentId` | kisscalc_methods | not_implemented |  |
| `getAussereEinwirkung` | kisscalc_methods | not_implemented |  |
| `getAxialModule` | kisscalc_methods | not_implemented |  |
| `getAxialOffsetCopy` | kisscalc_methods | not_implemented |  |
| `getAxis` | kisscalc_methods | not_implemented |  |
| `getAxisId` | kisscalc_methods | not_implemented |  |
| `getAxisRotationCopy` | kisscalc_methods | not_implemented |  |
| `getAxisRotationReference` | kisscalc_methods | not_implemented |  |
| `getAxisRotationThetaX` | kisscalc_methods | not_implemented |  |
| `getAxisRotationThetaXCopy` | kisscalc_methods | not_implemented |  |
| `getAxisRotationThetaY` | kisscalc_methods | not_implemented |  |
| `getAxisRotationThetaYCopy` | kisscalc_methods | not_implemented |  |
| `getAxisRotationThetaZ` | kisscalc_methods | not_implemented |  |
| `getAxisRotationThetaZCopy` | kisscalc_methods | not_implemented |  |
| `getAxisType` | kisscalc_methods | not_implemented |  |
| `getBCName` | kisscalc_methods | not_implemented |  |
| `getBCPowerStatus` | kisscalc_methods | not_implemented |  |
| `getBCSpeedStatus` | kisscalc_methods | not_implemented |  |
| `getBCTorqueStatus` | kisscalc_methods | not_implemented |  |
| `getBelowReferenceConst` | kisscalc_methods | not_implemented |  |
| `getBelowReferenceForPos` | kisscalc_methods | not_implemented |  |
| `getBinNumber` | kisscalc_methods | not_implemented |  |
| `getBoundaries` | kisscalc_methods | not_implemented |  |
| `getBoxHeight` | kisscalc_methods | not_implemented |  |
| `getBoxLength` | kisscalc_methods | not_implemented |  |
| `getBoxWidth` | kisscalc_methods | not_implemented |  |
| `getCACenterDistance` | kisscalc_methods | not_implemented |  |
| `getCACenterDistanceTolerance` | kisscalc_methods | not_implemented |  |
| `getCalc` | kisscalc_methods | not_implemented |  |
| `getCalcAndBrgCounterFromRow` | kisscalc_methods | not_implemented |  |
| `getCalcFileName` | kisscalc_methods | not_implemented |  |
| `getCalcOfElement` | kisscalc_methods | not_implemented |  |
| `getCalcsWhereGearWasPaired` | kisscalc_methods | not_implemented |  |
| `getCalculation` | kisscalc_methods | not_implemented |  |
| `getCalculationMethod` | kisscalc_methods | not_implemented |  |
| `getCalculationModule` | kisscalc_methods | not_implemented |  |
| `getCalculationWithoutSave` | kisscalc_methods | not_implemented |  |
| `getCenterDistance` | kisscalc_methods | not_implemented |  |
| `getCenterDistanceCopy` | kisscalc_methods | not_implemented |  |
| `getCenterDistanceForPos` | kisscalc_methods | not_implemented |  |
| `getCenterDistanceReference` | kisscalc_methods | not_implemented |  |
| `getChildrenAndPos` | kisscalc_methods | not_implemented |  |
| `getCombinedInterpolatedEffect` | kisscalc_methods | not_implemented |  |
| `getComment` | kisscalc_methods | not_implemented |  |
| `getCompAttribute` | kisscalc_methods | not_implemented |  |
| `getCompAttributes` | kisscalc_methods | not_implemented |  |
| `getComplementaryPosition` | kisscalc_methods | not_implemented |  |
| `getConeAngle` | kisscalc_methods | not_implemented |  |
| `getConnectionCalcTypes` | kisscalc_methods | not_implemented |  |
| `getConnectionData` | kisscalc_methods | not_implemented |  |
| `getConnectionTypes` | kisscalc_methods | not_implemented |  |
| `getConstForPositionId` | kisscalc_methods | not_implemented |  |
| `getContactWidth` | kisscalc_methods | not_implemented |  |
| `getContour` | kisscalc_methods | not_implemented |  |
| `getConusAngle` | kisscalc_methods | not_implemented |  |
| `getCoordSystemCopy` | kisscalc_methods | not_implemented |  |
| `getCoordinateSystem` | kisscalc_methods | not_implemented |  |
| `getCoordinateSystem2D` | kisscalc_methods | not_implemented |  |
| `getCoordinateSystemOrigin` | kisscalc_methods | not_implemented |  |
| `getCoordinatesInput` | kisscalc_methods | not_implemented |  |
| `getCopyNumber` | kisscalc_methods | not_implemented |  |
| `getCorrectionDelta` | kisscalc_methods | not_implemented |  |
| `getCorrectionFactor` | kisscalc_methods | not_implemented |  |
| `getCorrectionSum` | kisscalc_methods | not_implemented |  |
| `getCorrectiontypeAsKWString` | kisscalc_methods | not_implemented |  |
| `getCurrentBCPosition` | kisscalc_methods | not_implemented |  |
| `getCurrentOperatingMode` | kisscalc_methods | not_implemented |  |
| `getCurrentPlanet` | kisscalc_methods | not_implemented |  |
| `getCurrentSwitchPosition` | kisscalc_methods | not_implemented |  |
| `getCurrentValue` | kisscalc_methods | not_implemented |  |
| `getCurrentVariant` | kisscalc_methods | not_implemented |  |
| `getCwd` | kisscalc_methods | not_implemented |  |
| `getCylIndexOfPosition` | kisscalc_methods | not_implemented |  |
| `getCylinderDefaultLength` | kisscalc_methods | not_implemented |  |
| `getCylinderDiameter` | kisscalc_methods | not_implemented |  |
| `getCylinderIdsOfDot` | kisscalc_methods | not_implemented |  |
| `getCylinderIdsOfElement` | kisscalc_methods | not_implemented |  |
| `getCylinderLength` | kisscalc_methods | not_implemented |  |
| `getCylinderLengthDirection` | kisscalc_methods | not_implemented |  |
| `getCylinderPosition` | kisscalc_methods | not_implemented |  |
| `getDAtPosition` | kisscalc_methods | not_implemented |  |
| `getDBIDfromRexsType` | kisscalc_methods | not_implemented |  |
| `getDBId` | kisscalc_methods | not_implemented |  |
| `getDa` | kisscalc_methods | not_implemented |  |
| `getDaAtIndex` | kisscalc_methods | not_implemented |  |
| `getDaAtPosition` | kisscalc_methods | not_implemented |  |
| `getDatFilePairs` | kisscalc_methods | not_implemented |  |
| `getData` | kisscalc_methods | not_implemented |  |
| `getDataFromGearModule` | kisscalc_methods | not_implemented |  |
| `getDataFromPathOfContact` | kisscalc_methods | not_implemented |  |
| `getDataFromRotCad` | kisscalc_methods | not_implemented |  |
| `getDataIdSelected` | kisscalc_methods | not_implemented |  |
| `getDataToRexs` | kisscalc_methods | not_implemented |  |
| `getDef` | kisscalc_methods | not_implemented |  |
| `getDefaultDa` | kisscalc_methods | not_implemented |  |
| `getDefaultDi` | kisscalc_methods | not_implemented |  |
| `getDefaultValue` | kisscalc_methods | not_implemented |  |
| `getDefinition` | kisscalc_methods | not_implemented |  |
| `getDefinitionName` | kisscalc_methods | not_implemented |  |
| `getDelta` | kisscalc_methods | not_implemented |  |
| `getDependenciesWhenRemovingItem` | kisscalc_methods | not_implemented |  |
| `getDeviations` | kisscalc_methods | not_implemented |  |
| `getDi` | kisscalc_methods | not_implemented |  |
| `getDiAtIndex` | kisscalc_methods | not_implemented |  |
| `getDiAtPosition` | kisscalc_methods | not_implemented |  |
| `getDiameter` | kisscalc_methods | not_implemented |  |
| `getDiameterAtIndex` | kisscalc_methods | not_implemented |  |
| `getDistance` | kisscalc_methods | not_implemented |  |
| `getDocPoints` | kisscalc_methods | not_implemented |  |
| `getDotId` | kisscalc_methods | not_implemented |  |
| `getDotIds` | kisscalc_methods | not_implemented |  |
| `getDotOfItem` | kisscalc_methods | not_implemented |  |
| `getDotRotation` | kisscalc_methods | not_implemented |  |
| `getDots` | kisscalc_methods | not_implemented |  |
| `getDotsAroundPosition` | kisscalc_methods | not_implemented |  |
| `getDriven1` | kisscalc_methods | not_implemented |  |
| `getDriven2` | kisscalc_methods | not_implemented |  |
| `getDynamicResultsForGraphics` | kisscalc_methods | not_implemented |  |
| `getEfficiency` | kisscalc_methods | not_implemented |  |
| `getElasticConditionType` | kisscalc_methods | not_implemented |  |
| `getElement` | kisscalc_methods | not_implemented |  |
| `getElement1Id` | kisscalc_methods | not_implemented |  |
| `getElement2Id` | kisscalc_methods | not_implemented |  |
| `getElementAttributes` | kisscalc_methods | not_implemented |  |
| `getElementConnectionData` | kisscalc_methods | not_implemented |  |
| `getElementId` | kisscalc_methods | not_implemented |  |
| `getElementIds` | kisscalc_methods | not_implemented |  |
| `getElementName` | kisscalc_methods | not_implemented |  |
| `getElementOfLoss` | kisscalc_methods | not_implemented |  |
| `getElementRatiosToRef` | kisscalc_methods | not_implemented |  |
| `getElementTerm` | kisscalc_methods | not_implemented |  |
| `getElementType` | kisscalc_methods | not_implemented |  |
| `getElementsForKISSsoftRecurDynInterface` | kisscalc_methods | not_implemented |  |
| `getEmodulus` | kisscalc_methods | not_implemented |  |
| `getEmptyDots` | kisscalc_methods | not_implemented |  |
| `getEmptyPositions` | kisscalc_methods | not_implemented |  |
| `getEngagedGear` | kisscalc_methods | not_implemented |  |
| `getEntryContact` | kisscalc_methods | not_implemented |  |
| `getEntryContacts` | kisscalc_methods | not_implemented |  |
| `getEntryPosition` | kisscalc_methods | not_implemented |  |
| `getEntryPositions` | kisscalc_methods | not_implemented |  |
| `getErr` | kisscalc_methods | not_implemented |  |
| `getEvaluatedEntryContact` | kisscalc_methods | not_implemented |  |
| `getExtDir` | kisscalc_methods | not_implemented |  |
| `getExtrapolationStart` | kisscalc_methods | not_implemented |  |
| `getFEUtilities` | kisscalc_methods | not_implemented |  |
| `getFM` | kisscalc_methods | not_implemented |  |
| `getFalse` | kisscalc_methods | not_implemented |  |
| `getFileName` | kisscalc_methods | not_implemented |  |
| `getFineSizingUnit` | kisscalc_methods | not_implemented |  |
| `getFlag` | kisscalc_methods | not_implemented |  |
| `getFlankGLData` | kisscalc_methods | not_implemented |  |
| `getFrequenciesFromSubCalcs` | kisscalc_methods | not_implemented |  |
| `getFrictionCalculationDataRef` | kisscalc_methods | not_implemented |  |
| `getFrictionCoefficient` | kisscalc_methods | not_implemented |  |
| `getFromToleranceField` | kisscalc_methods | not_implemented |  |
| `getGear` | kisscalc_methods | not_implemented |  |
| `getGear1Id` | kisscalc_methods | not_implemented |  |
| `getGear2Id` | kisscalc_methods | not_implemented |  |
| `getGearBodyMaterial` | kisscalc_methods | not_implemented |  |
| `getGearBodyPoints` | kisscalc_methods | not_implemented |  |
| `getGearBodyStiffnessMatrices` | kisscalc_methods | not_implemented |  |
| `getGearCalcTypes` | kisscalc_methods | not_implemented |  |
| `getGearData` | kisscalc_methods | not_implemented |  |
| `getGearMountingAngle` | kisscalc_methods | not_implemented |  |
| `getGearName` | kisscalc_methods | not_implemented |  |
| `getGearNames` | kisscalc_methods | not_implemented |  |
| `getGearNumberOfTeeth` | kisscalc_methods | not_implemented |  |
| `getGearPointer` | kisscalc_methods | not_implemented |  |
| `getGearPositionAndDiameter` | kisscalc_methods | not_implemented |  |
| `getGearPressureAngle` | kisscalc_methods | not_implemented |  |
| `getGearTeethAngle` | kisscalc_methods | not_implemented |  |
| `getGearTeethValue` | kisscalc_methods | not_implemented |  |
| `getGearTypes` | kisscalc_methods | not_implemented |  |
| `getGearWidth` | kisscalc_methods | not_implemented |  |
| `getGearboxInOutput` | kisscalc_methods | not_implemented |  |
| `getGeneralCalculationType` | kisscalc_methods | not_implemented |  |
| `getGeometryForSelection` | kisscalc_methods | not_implemented |  |
| `getGlobalCoordinates` | kisscalc_methods | not_implemented |  |
| `getGlobalPosition` | kisscalc_methods | not_implemented |  |
| `getHGridRatio` | kisscalc_methods | not_implemented |  |
| `getHandOfGear` | kisscalc_methods | not_implemented |  |
| `getHeight` | kisscalc_methods | not_implemented |  |
| `getHeightInsideGearbody` | kisscalc_methods | not_implemented |  |
| `getHelixAngle` | kisscalc_methods | not_implemented |  |
| `getId` | kisscalc_methods | not_implemented |  |
| `getIdentifier` | kisscalc_methods | not_implemented |  |
| `getIds` | kisscalc_methods | not_implemented |  |
| `getIncreasedCounter` | kisscalc_methods | not_implemented |  |
| `getIndex` | kisscalc_methods | not_implemented |  |
| `getInitialUnits` | kisscalc_methods | not_implemented |  |
| `getInnerContour` | kisscalc_methods | not_implemented |  |
| `getInnerDiameter` | kisscalc_methods | not_implemented |  |
| `getInnerGeometry` | kisscalc_methods | not_implemented |  |
| `getInput` | kisscalc_methods | not_implemented |  |
| `getInputs` | kisscalc_methods | not_implemented |  |
| `getIsCoupConnectionWithPosition` | kisscalc_methods | not_implemented |  |
| `getIsPositioned` | kisscalc_methods | not_implemented |  |
| `getIsSwitching` | kisscalc_methods | not_implemented |  |
| `getItem` | kisscalc_methods | not_implemented |  |
| `getItemIdsOfType` | kisscalc_methods | not_implemented |  |
| `getItemIdsOfTypes` | kisscalc_methods | not_implemented |  |
| `getItemOfDotId` | kisscalc_methods | not_implemented |  |
| `getItemType` | kisscalc_methods | not_implemented |  |
| `getKDataType` | kisscalc_methods | not_implemented |  |
| `getKHbeta` | kisscalc_methods | not_implemented |  |
| `getKHbetaGap` | kisscalc_methods | not_implemented |  |
| `getKObjOfKDataId` | kisscalc_methods | not_implemented |  |
| `getLSElement` | kisscalc_methods | not_implemented |  |
| `getLSInput` | kisscalc_methods | not_implemented |  |
| `getLeadAngle` | kisscalc_methods | not_implemented |  |
| `getLength` | kisscalc_methods | not_implemented |  |
| `getLengthAtIndex` | kisscalc_methods | not_implemented |  |
| `getLengthAtPosition` | kisscalc_methods | not_implemented |  |
| `getLifetimeFrequencySpectrum` | kisscalc_methods | not_implemented |  |
| `getLifetimeTotal` | kisscalc_methods | not_implemented |  |
| `getLocalCoordinates` | kisscalc_methods | not_implemented |  |
| `getLogic` | kisscalc_methods | not_implemented |  |
| `getLoopAngle` | kisscalc_methods | not_implemented |  |
| `getLossId` | kisscalc_methods | not_implemented |  |
| `getLossInput` | kisscalc_methods | not_implemented |  |
| `getLossRatio` | kisscalc_methods | not_implemented |  |
| `getLubElement` | kisscalc_methods | not_implemented |  |
| `getLubInput` | kisscalc_methods | not_implemented |  |
| `getMatElement` | kisscalc_methods | not_implemented |  |
| `getMaxDimensionsOfGearbox` | kisscalc_methods | not_implemented |  |
| `getMaxDistanceXaxisGlobal` | kisscalc_methods | not_implemented |  |
| `getMaxNbOfModificationsDefined` | kisscalc_methods | not_implemented |  |
| `getMaxNumberOfIterations` | kisscalc_methods | not_implemented |  |
| `getMeanNormalModule` | kisscalc_methods | not_implemented |  |
| `getMeanSpiralAngle` | kisscalc_methods | not_implemented |  |
| `getMinMaxFrom4DimVectorCurves` | kisscalc_methods | not_implemented |  |
| `getMinMaxTERatio` | kisscalc_methods | not_implemented |  |
| `getModelId` | kisscalc_methods | not_implemented |  |
| `getModelId2Xml` | kisscalc_methods | not_implemented |  |
| `getModificationString` | kisscalc_methods | not_implemented |  |
| `getModule` | kisscalc_methods | not_implemented |  |
| `getModuleGearData` | kisscalc_methods | not_implemented |  |
| `getModuleSpecificSettings` | kisscalc_methods | not_implemented |  |
| `getMountingAngleIsGiven` | kisscalc_methods | not_implemented |  |
| `getName` | kisscalc_methods | not_implemented |  |
| `getNameOfId` | kisscalc_methods | not_implemented |  |
| `getNameOfIdPair` | kisscalc_methods | not_implemented |  |
| `getNbOfModificationCases` | kisscalc_methods | not_implemented |  |
| `getNewCylinderDiameters` | kisscalc_methods | not_implemented |  |
| `getNextDot` | kisscalc_methods | not_implemented |  |
| `getNextOccupied` | kisscalc_methods | not_implemented |  |
| `getNodeIds` | kisscalc_methods | not_implemented |  |
| `getNodeXCoords` | kisscalc_methods | not_implemented |  |
| `getNodeYCoords` | kisscalc_methods | not_implemented |  |
| `getNodeZCoords` | kisscalc_methods | not_implemented |  |
| `graphic_to_x` | kisscalc_methods | not_implemented |  |
| `graphic_to_y` | kisscalc_methods | not_implemented |  |
| `happens` | kisscalc_methods | not_implemented |  |
| `max` | kisscalc_methods | not_implemented |  |
| `meshing` | kisscalc_methods | not_implemented |  |
| `min` | kisscalc_methods | not_implemented |  |
| `open_file` | kisscalc_methods | not_implemented |  |
| `pi` | kisscalc_methods | not_implemented |  |
| `roughSizingGearbox` | kisscalc_methods | not_implemented |  |
| `round` | kisscalc_methods | not_implemented |  |
| `size` | kisscalc_methods | not_implemented |  |
| `sqrt` | kisscalc_methods | not_implemented |  |
| `square` | kisscalc_methods | not_implemented |  |
| `to_string` | kisscalc_methods | not_implemented |  |
| `x_to_graphic` | kisscalc_methods | not_implemented |  |
| `y_to_graphic` | kisscalc_methods | not_implemented |  |
