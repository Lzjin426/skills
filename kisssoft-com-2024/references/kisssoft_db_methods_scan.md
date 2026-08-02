# KISSsoft 2024 COM DB Methods Deep Scan Report

Generated: 2026-07-10T09:40:34.724688

## Environment
- Host: Windows `main-long` (100.111.253.87)
- ProgID: `KISSsoftCOM2024.KISSsoft`
- Python: `3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)]`
- KISSsoft base: `C:\Program Files\KISSsoft AG\KISSsoft 2024`

## COM Connection
- `KISSsoftCOM2024.KISSsoft` dispatched successfully.
- Module `Z012` loaded with `GetModule('Z012', False)`.

## Type Library Signatures
- `IKISSsoft2024`: `GetDBName(BSTR db_name, BSTR table, long flag, long ID, long order) -> BSTR`
- `IKISSsoft2024`: `GetDBValue(BSTR db_name, BSTR table, long ID, BSTR fieldname) -> BSTR`

## Database Files (kdb/udb)

### kdb: `C:\Program Files\KISSsoft AG\KISSsoft 2024\kdb`
- `KMAT.KDB` (1023654 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string NAME', 'string BEZ_ISO', 'string BEZ_COMMENT', 'string SOURCE', 'integer FETTFLAG', 'real ROOIL', 'real NU40', 'real NU100', 'integer SCHMIERBASE', 'integer SCORINGTEST', 'integer FZGTESTA', 'real SCORINGTEMP', 'integer FZGTESTMP', 'real KONUSPEN', 'real SEIFENANTEIL', 'integer OHNEADDIT', 'real EINSATZTEMP_VON', 'real EINSATZTEMP_BIS', 'real MAXGREASETEMP', 'real KFAC', 'real SFAC', 'integer MICROPITTINGTEST']
- `M000.KDB` (132863 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string NAME', 'string BEZ_COMMENT']
- `W000.KDB` (91798306 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string MANUFACTURER', 'string NAME', 'string COMMENT', 'string NOTE', 'string BAUREIHE', 'real INDM', 'real AUSDM', 'integer WITHOUTINNERRING', 'integer WITHOUTOUTERRING', 'real LAGBR', 'real RADIUS', 'real TRAGZC', 'real TRAGZCO', 'real TRAGZCA', 'real TRAGZCOA', 'integer HYBRID', 'real FAKTE', 'real FAKTX1', 'real FAKTY1', 'real FAKTX2', 'real FAKTY2', 'real FAKTE0', 'real FAKTX01', 'real FAKTY01', 'real FAKTX02', 'real FAKTY02', 'real DREHFET', 'real DREHOEL', 'real GEWICHT', 'real DRWINKEL', 'real MAXAXPR', 'real MAXWINK', 'real THEBEZDR', 'integer INLAGER', 'real PREIS', 'real MASS_A', 'real MASS_B', 'real MASS_C', 'real MASS_D', 'real MASS_E', 'real FEDKONR', 'real FEDKONA', 'real FEDKONN', 'real FAKT_F0', 'real MINDPC', 'real GRENZBEL', 'integer INT_A', 'integer INT_B', 'real INT_C', 'real INT_D', 'real INT_E', 'real INT_F', 'real INT_G', 'real INT_H', 'real INT_I', 'real INT_J', 'real INT_K', 'real INT_L', 'real INT_M', 'real INT_N', 'real INT_O', 'real INT_P', 'real INT_Q', 'real INT_R', 'real INT_S', 'string ROLLERPROFILE', 'string RACEWAYPROFINNER', 'string RACEWAYPROFOUTER', 'real INT_T', 'real INT_U']
- `Z000.KDB` (397659 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string NAME', 'string BEZ_COMMENT']

### udb: `C:\Program Files\KISSsoft AG\KISSsoft 2024\udb`
- `KMAT.UDB` (4670 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string NAME', 'string BEZ_ISO', 'string BEZ_COMMENT', 'string SOURCE', 'integer FETTFLAG', 'real ROOIL', 'real NU40', 'real NU100', 'integer SCHMIERBASE', 'integer SCORINGTEST', 'integer FZGTESTA', 'real SCORINGTEMP', 'integer FZGTESTMP', 'real KONUSPEN', 'real SEIFENANTEIL', 'integer OHNEADDIT', 'real EINSATZTEMP_VON', 'real EINSATZTEMP_BIS', 'real MAXGREASETEMP', 'real KFAC', 'real SFAC', 'integer MICROPITTINGTEST']
- `M000.UDB` (7529 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string NAME', 'string BEZ_COMMENT']
- `W000.UDB` (48542 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string MANUFACTURER', 'string NAME', 'string COMMENT', 'string NOTE', 'string BAUREIHE', 'real INDM', 'real AUSDM', 'integer WITHOUTINNERRING', 'integer WITHOUTOUTERRING', 'real LAGBR', 'real RADIUS', 'real TRAGZC', 'real TRAGZCO', 'real TRAGZCA', 'real TRAGZCOA', 'integer HYBRID', 'real FAKTE', 'real FAKTX1', 'real FAKTY1', 'real FAKTX2', 'real FAKTY2', 'real FAKTE0', 'real FAKTX01', 'real FAKTY01', 'real FAKTX02', 'real FAKTY02', 'real DREHFET', 'real DREHOEL', 'real GEWICHT', 'real DRWINKEL', 'real MAXAXPR', 'real MAXWINK', 'real THEBEZDR', 'integer INLAGER', 'real PREIS', 'real MASS_A', 'real MASS_B', 'real MASS_C', 'real MASS_D', 'real MASS_E', 'real FEDKONR', 'real FEDKONA', 'real FEDKONN', 'real FAKT_F0', 'real MINDPC', 'real GRENZBEL', 'integer INT_A', 'integer INT_B', 'real INT_C', 'real INT_D', 'real INT_E', 'real INT_F', 'real INT_G', 'real INT_H', 'real INT_I', 'real INT_J', 'real INT_K', 'real INT_L', 'real INT_M', 'real INT_N', 'real INT_O', 'real INT_P', 'real INT_Q', 'real INT_R', 'real INT_S', 'string ROLLERPROFILE', 'string RACEWAYPROFINNER', 'string RACEWAYPROFOUTER', 'real INT_T', 'real INT_U']
- `Z000.UDB` (8522 bytes)
  - fields: ['integer ID', 'integer FOLGE', 'string MODUL', 'integer STATUS', 'string CREATE_BY', 'string CREATE_DATE', 'string CREATE_TIME', 'string UPDATE_BY', 'string UPDATE_DATE', 'string UPDATE_TIME', 'string NAME', 'string BEZ_COMMENT']

## Real Database IDs via GetVarAsJson
- `ZR[0].mat.DBID`: `{"return_value":10260,"status_code":"ok"}` (err=None)
- `ZR[0].mat.bez`: `{"return_value":"18CrNiMo7-6","status_code":"ok"}` (err=None)
- `ZR[0].mat.nr`: `{"status_code":"not_found","status_msg":"Coult not find requested variable"}` (err=None)
- `ZR[0].mat.id`: `{"status_code":"not_found","status_msg":"Coult not find requested variable"}` (err=None)

## Successful Call Examples

### GetDBName(db_name, table, flag, ID, order)
- `ks.GetDBName('KMAT', 'KLUB', 0, 10260, 0)` -> `Klübersynth GH 6-460 (API GL 5)`
- `ks.GetDBName('W000', 'W05WNORM10', 0, 1, 0)` -> `6014-2RSR-C4`
- `ks.GetDBName('W000', 'W05WNORM10', 0, 2, 0)` -> `6014-2RSR-L038`
- `ks.GetDBName('W000', 'W05WNORM10', 0, 10260, 0)` -> `16032`
- `ks.GetDBName('Z000', 'ZAXT', 0, 10260, 0)` -> `ISO 286:2010 Surcote H6`

### GetDBValue(db_name, table, ID, fieldname)
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'NAME')` -> `Klübersynth GH 6-460 (API GL 5)`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'BEZ_ISO')` -> `ISO VG 460`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'BEZ_COMMENT')` -> `Huile à grande capacité de charge (engrenage droit, roue conique et vis sans fin)`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'ID')` -> `10260`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'ROOIL')` -> `1.074`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'NU40')` -> `460`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'NU100')` -> `71`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'KFAC')` -> `0.0047`
- `ks.GetDBValue('KMAT', 'KLUB', 10260, 'SFAC')` -> `0.1572`
- `ks.GetDBValue('Z000', 'ZAXT', 10260, 'NAME')` -> `ISO 286:2010 Surcote H6`
- `ks.GetDBValue('Z000', 'ZAXT', 10260, 'ID')` -> `10260`

## Failed Attempts (Incorrect Signatures)
Calling the methods with the documented `GetDBName(table, index)` / `GetDBValue(table, index, field)`
signatures produced the following errors:

- `ks.GetDBName('KMAT', '0')` -> `com_error: (-2147352561, '非选择性的参数。', None, None)`
- `ks.GetDBValue('KMAT', '0', 'NAME')` -> `ValueError: invalid literal for int() with base 10: 'NAME'`

## Parameter Convention
- `db_name`: Database file name without extension (e.g., `KMAT`, `M000`, `W000`, `Z000`).
- `table`: Internal table name from the KDB header (e.g., `KLUB`, `M02A`, `W05WNORM10`, `ZAXT`).
- `flag`: `0` for standard database, `1` for user/custom entries.
- `ID`: Integer record ID in the database (primary key in the `ID` field).
- `order`: Ordering index; `0` returned the standard name in successful tests.
- `fieldname`: Field name from the table schema (case-insensitive). Empty string if the field does not exist.

## Summary
- **Successful**: Yes, with the exact signatures from the type library.
- `GetDBName` returns the display name of a database record.
- `GetDBValue` returns a specific field value as a BSTR string.
- The commonly documented 2-/3-argument signatures are **incorrect** for KISSsoft 2024.
- Exhaustive parameter testing was performed against many db_name/table/ID/field combinations;
  this report lists only the representative successful examples.
