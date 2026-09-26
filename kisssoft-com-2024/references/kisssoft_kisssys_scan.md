# KISSsys 自动化探索

**结论**：KISSsys 无法通过 `KISSsoftCOM2024.KISSsoft` COM 接口自动化，也没有独立的 KISSsys COM 接口。

## 关键发现

- `KISSsys.exe` 位于 `C:\Program Files\KISSsoft AG\KISSsoft 2024\bin\KISSsys.exe`，是基于 AWV ClassCAD 的独立 GUI 程序。
- KISSsys 文件扩展名为 `.ks`（ClassCAD 私有序列化格式）。
- `KISSsoftCOM2024.KISSsoft` 对 `.ks` 文件调用 `GetModulFromFile()` 返回空字符串，无法加载。
- `GetModule('SYS', False)`、`GetModule('KSE', False)`、`GetModule('KISSsys', False)` 均返回 `None`；`IsModuleValid()` 始终为 `False`。
- `CallJsonFunc` 中所有 `System`/`Train`/`Stage`/`KISSsys` 相关函数均返回 `"No calculation module is loaded"`。
- `KISSsys.*` / `KISSsys2024.*` ProgID 都未注册（`-2147221005`，无效类字符串）。
- 注册表仅 MSI 安装器特征项包含 `KISSsys` 字符串，无 COM 类注册。

## 如果必须自动化 KISSsys

唯一可行方案是 **UI 自动化**（如 pywinauto）或预生成 `.ks` 文件再启动 `KISSsys.exe`。

## 参考

- `references/kisssoft_com_reference.md`：主 COM 参考
- `references/kisssoft_module_loadability.md`：模块加载测试结果
