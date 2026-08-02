# KISSsoft 2024 COM Optimization / DOE / Sizing Scan Report

**Host:** `main-long` (Windows)  
**User:** `full stop`  
**ProgID:** `KISSsoftCOM2024.KISSsoft`  
**Module loaded:** `Z012`  
**Example file:** `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12`  
**Date:** 2026-07-10

---

## 1. Executive Summary

- **No dedicated generic `Optimize` or `DOE` COM functions** were found in the 2024 COM API. Calling `Optimize` or `DOE` returns `not_implemented` / `The call function was not found`.
- **Sizing-related functions exist** and are callable through `CallFunc` / `CallJsonFunc`:
  - `calculateRoughSizing`
  - `CalculateFineSizing`
  - `calculateModificationProposal`
  - `calculateModificationFineSizing`
  - `calculateSizeCenterDistance`
  - `CalculateOptionsForX` (returns a numeric value, likely a recommended profile-shift value)
- In the `Z012` module, `calculateRoughSizing` and `CalculateFineSizing` return `ok` but do **not populate the expected result variables**. This strongly suggests they are designed for the `Z010` sizing UI context and require the corresponding `.kui` variables to be configured first.
- `CalculateOptionsForX` is the only sizing/optimization function that returns a meaningful number directly in `Z012` (≈ 0.2706 for the example file). Its arguments are ignored in the tests.
- **Manual parameter optimization is fully feasible** by looping over `SetVar(...)` → `Calculate()` → `GetVar(...)` externally. A sweep of `ZR[0].b` from 30–60 mm shows a monotonic increase of `ZPP[0].Fuss.SFnorm` from 1.77 to 3.39 in the tested range.

**Verdict:** KISSsoft 2024 COM does not expose a ready-to-use high-level optimization/DOE engine. However, automated parameter optimization is possible by driving the calculation loop from Python, and some sizing helpers (`CalculateOptionsForX`) can be invoked for quick recommendations.

---

## 2. Documents and Examples Found

A search of `C:\Program Files\KISSsoft AG\KISSsoft 2024` for keywords `Optimize`, `Optimization`, `DOE`, `Sizing`, `RoughSizing`, `FineSizing`, `Modification`, `Proposal` returned the following relevant items (excerpt):

### Tutorials / PDFs
- `tutorial\KISSsoft-Tutorial-009-Gearsizing-en.pdf`
- `tutorial\KISSsoft-Tutorial-012-Sizing_Of_Planetary_Gear_Set-en.pdf`
- `tutorial\KISSsoft-Tutorial-012-step2-rough-sizing.Z14`
- `tutorial\KISSsoft-Tutorial-012-step3_fine-sizing.Z14`
- `tutorial\KISSsoft-Tutorial-012-step4_modifications.Z14`

### UI definition files (`.kui`) containing sizing setups
- `kui\Z010_RoughSizing.kui` → `<setup>setupRoughSizing</setup>` / `<calculation>calculateRoughSizing</calculation>`
- `kui\Z010_FineSizing.kui` → `<setup>SetupFineSizing</setup>` / `<calculation>CalculateFineSizing</calculation>`
- `kui\Z000_ModificationRoughSizing.kui` → `<setup>setupModificationProposal</setup>` / `<calculation>calculateModificationProposal(currentTab)</calculation>`
- `kui\Z000_ModificationFineSizing.kui` → `<setup>setupModificationFineSizing</setup>` / `<calculation>calculateModificationFineSizing</calculation>`
- `kui\Z010_SizeCenterDistance.kui` → `<setup>setupSizeCenterDistance</setup>` / `<calculation>calculateSizeCenterDistance</calculation>`
- `kui\Z012_Z014_Z015_Z016_SizeProfileShift.kui` → `<setup>setupProfileShiftLimit</setup>`

### Report templates (`.rpt`) related to sizing / modifications
- `rpt\Z010ContactAnalysisModificationSizing*.rpt`
- `rpt\Z010Modifications*.rpt`
- `rpt\Z070ContactAnalysisModificationSizing*.rpt`
- `rpt\Z000ModificationsSummary*.rpt`
- `rpt\z010ModificationSizingLK*.rpt`

### Help / COM API reference
- `help\e\9748.htm` — "Server functionality": documents `GetModule`, `Calculate`, `SetVar`, `GetVar`, `CallFunc`, `CallFuncNParam`, `Report`, etc.
- `help\e\9749.htm` — Excel/VBA example using `GetModule("Z011", False)` and `SetVar`/`Calculate`/`GetVar`.
- `help\e\8634.htm` — "Center distance" describes the profile-shift sizing options accessible in the UI.

---

## 3. COM API Method Inventory

From the `KISSsoftCOM2024.KISSsoft` type library:

| Method | Signature (from type info) | Purpose |
|---|---|---|
| `GetModule` | `(BSTR module, VARIANT_BOOL interactive)` | Load a module, e.g. `Z012` |
| `LoadFile` | `(BSTR filename)` | Load a `.Z12` calculation file |
| `Calculate` / `CalculateRetVal` | `()` | Run the main calculation |
| `SetVar` | `(BSTR name, BSTR value)` | Set a KISSsoft variable as text |
| `GetVar` | `(BSTR name) → BSTR` | Read a KISSsoft variable as text |
| `GetVarAsJson` | `(BSTR nameBstr) → BSTR` | Read a variable as JSON |
| `CallFunc` | `(BSTR name)` | Call a named special function |
| `CallFuncNParam` | `(VARIANT paramArray)` | Call a function with an argument array |
| `CallJsonFunc` | `(BSTR functionName, VARIANT arrayOfJsonArgs) → BSTR` | JSON-return version of `CallFunc` |
| `ReleaseModule` | `()` | Release the active module |
| `SetSilentMode` | `(VARIANT_BOOL silent)` | Suppress message boxes |

---

## 4. Function Call Results (Z012 module, `01 Spur (ISO 6336).Z12`)

All calls were made after `SetSilentMode(True)` and an initial `Calculate()`.

| Function | Mode | Args | Result / Return | Time | Notes |
|---|---|---|---|---|---|
| `calculateRoughSizing` | `CallJsonFunc` | `[]` | `{"return_value":null,"status_code":"ok"}` | 0.21 s | No result variables populated |
| `calculateRoughSizing` | `CallFunc` | none | `None` | 0.23 s | No result variables populated |
| `CalculateFineSizing` | `CallJsonFunc` | `[]` | `{"return_value":null,"status_code":"ok"}` | 0.09 s | `FineSizingResultsTable` / `FSx` remain empty |
| `CalculateFineSizing` | `CallFunc` | none | `None` | 0.09 s | Result variables empty |
| `calculateModificationProposal` | `CallJsonFunc` | `[]` | `{"return_value":null,"status_code":"ok"}` | 0.00 s | `MP_*` variables remain empty |
| `calculateModificationProposal` | `CallJsonFunc` | `["0"]` | `{"return_value":null,"status_code":"ok"}` | 0.00 s | `currentTab=0` accepted |
| `calculateModificationProposal` | `CallJsonFunc` | `["1"]` | `{"status_code":"bad_function_call"}` | 0.01 s | `currentTab=1` invalid |
| `calculateModificationProposal` | `CallFuncNParam` | `["calculateModificationProposal", 0]` | `None` | 0.00 s | Same as `CallFunc` with tab 0 |
| `calculateModificationProposal` | `CallFuncNParam` | `["calculateModificationProposal", 1]` | **Server error** | — | `currentTab=1` invalid |
| `calculateModificationProposal` | `CallFunc` | `"calculateModificationProposal(0)"` | `None` | 0.00 s | No visible effect |
| `calculateModificationFineSizing` | `CallJsonFunc` | `[]` | `{"status_code":"bad_function_call"}` | 0.00 s | Not available in this module |
| `calculateModificationFineSizing` | `CallFunc` | none | `None` | 0.00 s | No effect |
| `calculateSizeCenterDistance` | `CallJsonFunc` | `[]` | `{"status_code":"bad_function_call"}` | 0.00 s | Not available in this module |
| `calculateSizeCenterDistance` | `CallFunc` | none | `None` | 0.00 s | `CD_*` variables empty |
| `setupRoughSizing` | `CallJsonFunc` / `CallFunc` | `[]` / none | `ok` / `None` | 0.00 s | UI setup only, no data created in Z012 |
| `SetupFineSizing` | `CallJsonFunc` / `CallFunc` | `[]` / none | `ok` / `None` | 0.00 s | UI setup only |
| `setupModificationProposal` | `CallJsonFunc` / `CallFunc` | `[]` / none | `ok` / `None` | 0.00 s | UI setup only |
| `setupModificationFineSizing` | `CallJsonFunc` / `CallFunc` | `[]` / none | `ok` / `None` | 0.00 s | UI setup only |
| `setupSizeCenterDistance` | `CallJsonFunc` / `CallFunc` | `[]` / none | `ok` / `None` | 0.00 s | UI setup only |
| `setupProfileShiftLimit` | `CallJsonFunc` / `CallFunc` | `[]` / none | `ok` / `None` | 0.23 s | UI setup only |
| `Optimize` | `CallJsonFunc` / `CallFunc` | `[]` / none | `not_implemented` / `None` | 0.00 s | **Not implemented** |
| `DOE` | `CallJsonFunc` / `CallFunc` | `[]` / none | `not_implemented` / `None` | 0.00 s | **Not implemented** |
| `CalculateOptionsForX` | `CallJsonFunc` | `[]` | `return_value ≈ 0.2706453579` | 0.23 s | **Returns a numeric value**; ignores supplied args |
| `CalculateOptionsForX` | `CallJsonFunc` | `["x1"]`, `["x2"]`, `["sum"]` | same value | 0.23 s | Argument has no effect in tests |
| `CalculateOptionsForX` | `CallJsonFunc` | `['{"type":"x1"}']`, etc. | same value | 0.23 s | JSON argument ignored |

---

## 5. Manual Parameter Optimization

A simple external loop was run in Python:

```python
for b in range(30, 61):
    ks.SetVar("ZR[0].b", str(b))
    ks.SetVar("ZR[1].b", str(b))
    ks.Calculate()
    sf = ks.GetVar("ZPP[0].Fuss.SFnorm")
```

Baseline values: `ZR[0].b = 44`, `ZR[1].b = 44`, `ZPP[0].Fuss.SFnorm = 2.5513`.

| b (mm) | SFnorm | b (mm) | SFnorm | b (mm) | SFnorm |
|--------|--------|--------|--------|--------|--------|
| 30 | 1.7661 | 41 | 2.3868 | 52 | 2.9700 |
| 31 | 1.8231 | 42 | 2.4419 | 53 | 3.0228 |
| 32 | 1.8800 | 43 | 2.4967 | 54 | 3.0754 |
| 33 | 1.9367 | 44 | 2.5513 | 55 | 3.1279 |
| 34 | 1.9934 | 45 | 2.6059 | 56 | 3.1802 |
| 35 | 2.0499 | 46 | 2.6500 | 57 | 3.2323 |
| 36 | 2.1064 | 47 | 2.7038 | 58 | 3.2843 |
| 37 | 2.1627 | 48 | 2.7573 | 59 | 3.3362 |
| 38 | 2.2189 | 49 | 2.8107 | 60 | 3.3878 |
| 39 | 2.2750 | 50 | 2.8640 | | |
| 40 | 2.3309 | 51 | 2.9171 | | |

**Result:** in the tested range, `SFnorm` increases monotonically with `b`; the maximum within the range is **3.3878 at b = 60 mm**. (A wider or constrained search would be needed for a true engineering optimum.)

---

## 6. Conclusions and Recommendations

1. **Built-in optimization / DOE:** There is no COM function named `Optimize` or `DOE` in KISSsoft 2024. They are not implemented.
2. **Sizing functions:** The functions `calculateRoughSizing`, `CalculateFineSizing`, `calculateModificationProposal`, `calculateModificationFineSizing`, `calculateSizeCenterDistance`, and `CalculateOptionsForX` are registered in the COM call table and can be invoked. However, only `CalculateOptionsForX` returns a direct numeric recommendation in the `Z012` context. The others behave like UI setup/calculation triggers and require the `Z010` sizing module/variables to produce visible results.
3. **Automation feasibility:** Real automated optimization can be built externally with the following pattern:
   ```python
   ks.SetSilentMode(True)
   ks.GetModule("Z012", False)
   ks.LoadFile(path)
   for value in design_variable_values:
       ks.SetVar("ZR[0].b", str(value))
       ks.Calculate()
       objective = float(ks.GetVar("ZPP[0].Fuss.SFnorm"))
       # choose best
   ks.ReleaseModule()
   ```
   Any external optimizer (grid search, scipy, Optuna, etc.) can be wrapped around this loop.
4. **Suggested next steps:** If the goal is to use KISSsoft's own rough/fine sizing, open the corresponding sizing UI via `setup*` functions and configure the required input variables, or load the calculation in the `Z010` module if available through COM. For pure automation, implement a Python optimizer around `SetVar`/`Calculate`/`GetVar`.

---

*Report generated by the KISSsoft 2024 COM deep-scan subagent.*
