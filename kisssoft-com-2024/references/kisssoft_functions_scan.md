# KISSsoft 2024 COM 接口函数扫描结果

- 扫描候选函数总数：**249**
- 任意调用返回有意义结果的函数数：**6**
- `CallJsonFunc` 返回 `status_code: ok` 的函数数：**6**
- 示例文件：`C:\Program Files\KISSsoft AG\KISSsoft 2024\example\Z012\01 Spur (ISO 6336).Z12`

## 最重要的有效函数名（Top 5）

1. `GenerateReport`
2. `GetConsistency`
3. `ModuleID`
4. `NewGraphic`
5. `ShowGraphic`

## `CallJsonFunc` 返回 `status_code: ok` 的函数名

- `GenerateReport`
- `GetConsistency`
- `ModuleID`
- `NewGraphic`
- `ShowGraphic`
- `Temp_Dir`

## 其他有意义返回的函数名


## 直接 COM 方法（dir(ks)）

- `CLSID`
- `Calculate`
- `CalculateRetVal`
- `CallFunc`
- `CallFuncNParam`
- `CallJsonFunc`
- `CheckLicense`
- `GetDBName`
- `GetDBValue`
- `GetININame`
- `GetKsoftPatchLevel`
- `GetKsoftVersion`
- `GetKsoftVersionFromFile`
- `GetKsoftVersionSettings`
- `GetLanguage`
- `GetModulFromFile`
- `GetModule`
- `GetModuleOEM`
- `GetNextResult`
- `GetResultCount`
- `GetVar`
- `GetVarAsJson`
- `GetVersionFromFile`
- `IsActiveInterface`
- `IsModuleValid`
- `LicenseNumber`
- `LoadFile`
- `LoadFileData`
- `LoadLicenseFile`
- `Message`
- `ReleaseModule`
- `Report`
- `ReportWithParameters`
- `SaveFile`
- `SetCallback`
- `SetDebugFile`
- `SetLanguage`
- `SetSilentMode`
- `SetVar`
- `ShowInterface`
- `coclass_clsid`
- `isActive`

## 详细调用结果

### `AmSOdon`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Bg`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Calculate`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=skipped, return=direct COM method
- **CallJsonFunc_arg**: status=skipped, return=direct COM method

### `CalculateStdCA`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":false}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":false}

### `Circle`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `ContactAnalysis`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Corr`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `DreiRad`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `DutyCycle`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Execute`
- **CallFunc**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallFuncNParam**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallJsonFunc_empty**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `Exiting`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Export`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ExportToothContact`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `FO`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `FineSizing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":false}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":false}

### `Flanke`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ForceExcitation`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Fuss`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Gears`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `GenerateReport`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"return_value":"C:/Windows/TEMP/KISS_4\\Z012.pprpt","status_code":"ok"}

### `GenerateUIVar`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `Geo`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `GetConsistency`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"return_value":0,"status_code":"ok"}
- **CallJsonFunc_arg**: status=ok, return={"return_value":0,"status_code":"ok"}

### `GetModuleInfo`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `GetVariables`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `GetVersionInfo`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Harm`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Hes`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `IN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `If`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Its`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `KHbVariant`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `KHb_nominal`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Kbln0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `L0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Line`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `LoadFile`
- **CallFunc**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallFuncNParam**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallJsonFunc_empty**: status=skipped, return=direct COM method
- **CallJsonFunc_arg**: status=skipped, return=direct COM method

### `LoadSpectrum`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Lu`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `MaxHertzianStress`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Mdrag`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Message`
- **CallFunc**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallFuncNParam**: status=error, return=com_error: (-2147417851, '服务器出现意外情况。', None, None)
- **CallJsonFunc_empty**: status=skipped, return=direct COM method
- **CallJsonFunc_arg**: status=skipped, return=direct COM method

### `Module`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ModuleID`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"return_value":"Z012","status_code":"ok"}
- **CallJsonFunc_arg**: status=ok, return={"return_value":"Z012","status_code":"ok"}

### `NN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `NPge`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `NS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `NWN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `NewGraphic`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"return_value":null,"status_code":"ok"}

### `Nl`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Nv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ON`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ORN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `OT`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `OT000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `OU_`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `OY`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `PSQN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Pi`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Pn0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Position`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `PowerLoss`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Q0R`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `RechenMethID`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `RechenMethID_default`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `RechenMethID_old`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `RoughSizing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":false}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":false}

### `S000o0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `S0n000000000k0o0Nl`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SF`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SFnorm`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SH`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SHIFT`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SKRIPTMODULE`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SKRIPTNAME`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Safety`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SaveReport`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SbDR`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `SetColor`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `ShowDialog`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `ShowGraphic`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"return_value":null,"status_code":"ok"}

### `Sizing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Spur`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Sv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `TE_Harmonics`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `TINv_`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `TRN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `TcR`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Temp_Dir`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"return_value":"C:/Windows/TEMP/KISS_4\\","status_code":"ok"}
- **CallJsonFunc_arg**: status=ok, return={"return_value":"C:/Windows/TEMP/KISS_4\\","status_code":"ok"}

### `Text`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"bad_function_call","status_msg":null}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"bad_function_call","status_msg":null}

### `Thb`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `The`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `This`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Tol`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ToothFormCalculation`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `TpN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `TransmissionError`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `UOb_r`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `U_`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Use`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Version`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Vqual`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Waelz`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `WhTONS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Wi`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `WnVpei`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Y000000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Y2`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `YS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yg0n0WnQ`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yg0n0m0X00`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yk0J0Q00`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yk0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yn0okS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yokv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `YtPfR0`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yv_`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Yzk0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `Z12`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ZP`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ZPP`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ZR`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ZS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `_fRw`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `_j`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `_jh`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `active`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `activeForVariant`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `addItem`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `alf12_23`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `alf23_34`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `apos`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `append_to_file`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `average`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `bN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `b_rOpe`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `bk0Y00iddRR`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `bv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `cRg`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `calc`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `calculate`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `cgq`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `close_file`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `constraints`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `contactAnalysis`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `coordinateSystem`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `coverages`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `csv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `cylindrical1`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `cylindrical2`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `defineBoundary`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `defineGearPair`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `degrees`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `delta`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `distances`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `dutyCycle`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `eb`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `export`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `exportToothContact`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `f0000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `f0000n0Vpe`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `factor1`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `factor2`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ff`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `file`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `fineSizing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `floor`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `frictionCalculationData`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `g0o0000000n0okHQQv_o0S`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `gS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `gamPC`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `gear`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `gear2`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `generateReport`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `getConsistency`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `getModuleInfo`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `getVariables`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `getVersionInfo`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `gn0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `graphic_to_x`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `graphic_to_y`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `gsO`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `h0`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `happens`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `helicalpair_calc`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `idd`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `j0rKag0K0K00R`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `k0J0Q00i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `k0Y00cHh`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `kk0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `kn06RP0s`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `linksflankedocument`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `loadSpectrum`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `mU0`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `mU0k00i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `meshing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `misWN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `mn`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ms`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `n00000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `n000000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `n0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `name`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `nci`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `nul`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `numOfTeeth`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `nv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `nxO`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `o00000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `oilLevel`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `open_file`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `p00`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `pe`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `qeQ0`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `rechts`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `roughSizing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `roughSizingGearbox`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `sD`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `saveReport`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `settingsEL`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `shaft1`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `shaft2`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `size`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `sizing`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `square`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `sv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `tWQv_`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `to_string`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `toothFormCalculation`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `tv`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `tvS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ty`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `type`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `tz`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `uN`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `ulQtShV`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `v6R`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `vCQ`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `vQ`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `vp`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `w0000peo0okCQwk0i`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `w050Results`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `w1_NS`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `write`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `xJR000`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `x_to_graphic`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `y_to_graphic`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `yrk`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}

### `zo0`
- **CallFunc**: status=ok, return=None
- **CallFuncNParam**: status=ok, return=None
- **CallJsonFunc_empty**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
- **CallJsonFunc_arg**: status=ok, return={"status_code":"not_implemented","status_msg":"The call function was not found"}
