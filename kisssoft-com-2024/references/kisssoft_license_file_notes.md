# KISSsoft 2024 License File Notes

## License File Location

```
C:\Program Files\KISSsoft AG\KISSsoft 2024\license\License.lic
```

## Format

`License.lic` is a plain text file with fields:

```text
License Number: 1113
License Name: ForEveryOne
Version: 2024
License Type: 4
KISSsoft Users: 1
KISSsys Users: 1
License Code: 42BD0100BE1C1674
Modules: <hex-encoded module codes>
Checksum: BD3E474F3AA0F4AB20A2754EE80198D35C04E035
```

## Modules Field

The `Modules` field is a concatenated string of 4-character hex ASCII values, each representing a 2-byte module code. For example:

- `45393033` → ASCII `E903`
- `45413033` → ASCII `EA03`
- `45423033` → ASCII `EB03`

These are internal KISSsoft feature codes, not the user-facing module IDs like `Z011` or `Z012`.

## Why Some Modules Are Not Available in COM

If the **License Tool** (shown in the user's screenshot) has modules checked but `ks.CheckLicense(module_id)` returns `False`, the most likely cause is that the license tool changes have not been **applied/saved** to `License.lic`.

The license file is the source of truth for COM. Until the user clicks **应用 (Apply)** or **保存 (Save)** in the license tool, the COM API will continue to report the old set of modules.

## Do Not Edit Manually

Do not manually edit `License.lic`. The `Checksum` field is used to verify file integrity. Modifying the file without recalculating the checksum will likely invalidate the license.

## How to Enable More Modules

1. Open the KISSsoft license tool.
2. Check the desired modules.
3. Click **应用 (Apply)** or **保存 (Save)**.
4. Restart any running KISSsoft/COM processes.
5. Re-run `ks.CheckLicense(module_id)` to verify.

## Reference

- See `references/kisssoft_license_scan.md` for the current `CheckLicense` results.
- See `references/kisssoft_module_loadability.md` for which modules actually load and calculate.
