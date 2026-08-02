# KISSsoft 2024 COM 参数化函数与批量模式

**结论**：`CallJsonFunc` 支持带参数调用，`SetSilentMode` 有效，批量切换模块/文件安全，错误恢复能力强。

## 关键发现

### 模块加载

- KISSsoft 2024 中必须使用 `GetModule("Z012", 0)`（两个参数），单参数形式会触发 `DISP_E_NONAMEDARGS`。
- 切换模块前调用 `ReleaseModule()` 可保证干净状态。

### CallJsonFunc 签名

- 正确形式：`ks.CallJsonFunc(name, [arg1, arg2, ...])`，传入 Python 列表。
- 传入 JSON 字符串会报 `DISP_E_EXCEPTION`。

### 支持参数化的函数

- `CalculateOptionsForX`：`['0.5']`、`['0.0']`、`['-0.5']` 均返回 OK。
- `CalculateStdCA` / `CalculateCA`：用字符串 `['1']` / `['0']` 返回 OK；布尔值 `[True]` / `[False]` 会导致服务器异常。
- `SetCenterDistanceTolerances` / `SetToothThicknessTolerances`：OK。
- `GenerateReport`：OK，但即使传入不存在的模板路径也返回相同的默认临时报告路径。

### 报告函数

- `Report()` 无参数会报错；应使用 `Report(0)` 或 `Report(1)`。
- `ReportWithParameters(template, output, show, art)` 生成真实文件。

### 静默模式

- `SetSilentMode(1)` 有效。
- `Calculate` 和 `Report(1)` 在静默模式下均在 1 秒内完成，无弹窗阻塞。
- 用 `SetSilentMode(0)` 恢复。

### 批量处理

- 同一 COM 对象中通过 `ReleaseModule()` + `GetModule(module, 0)` 切换模块可行。
- 连续 `LoadFile` + `Calculate` + `GetVarAsJson` 无状态污染。
- 不同文件的变量路径和计算结果值不同，说明模块状态正确隔离。

### 错误恢复

- 加载不存在的文件、读取不存在的变量、或在未加载文件时计算，COM 对象都不会崩溃。
- 后续仍可正常加载有效文件并计算。
- `ReleaseModule + GetModule` 可重置到干净状态。

### 变量路径

- `GetVarAsJson` 顶层名称如 `SF` / `SH` 返回 `not_found`。
- Z012 模块需使用完整路径，如 `ZPP[0].Flanke.SH`、`ZPP[0].Fuss.SF`。

## 最佳实践

```python
import win32com.client
import json

ks = win32com.client.Dispatch("KISSsoftCOM2024.KISSsoft")
ks.SetSilentMode(1)
ks.GetModule("Z012", 0)
ks.LoadFile(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")
ks.Calculate()

r = json.loads(ks.GetVarAsJson("ZPP[0].Fuss.SFnorm"))
print(r)

ks.ReleaseModule()
```

## 参考

- `references/kisssoft_com_reference.md`：完整方法列表
- `references/kisssoft_functions_deep_scan.md`：内部函数枚举
