# KISSsoft COM IO / 配置 / 错误处理扫描结果

Connected
Loaded Z012 example


## LoadFileData tests

LoadFileData (first 2000 chars): result=None, time=0.01s, err=None


## SaveFile tests

SaveFile('C:\Users\Full stop\Desktop\test_save.Z12'): result=None, time=0.01s, err=None
Saved file exists: True, size: 388846


## File metadata tests

GetModulFromFile('C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12'): 'Z012', time=0.00s, err=None
GetVersionFromFile('C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12'): '24.0', time=0.00s, err=None
GetKsoftVersionFromFile('C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12'): '2024', time=0.01s, err=None
GetModulFromFile('C:\Users\Full stop\Desktop\test_save.Z12'): 'Z012', time=0.00s, err=None
GetVersionFromFile('C:\Users\Full stop\Desktop\test_save.Z12'): '24.0', time=0.00s, err=None
GetKsoftVersionFromFile('C:\Users\Full stop\Desktop\test_save.Z12'): '2024 -SP1', time=0.01s, err=None


## Report tests

Report(0): result=None, time=0.74s, err=None
Report(1): result=None, time=0.71s, err=None
ReportWithParameters(Z012resc.rpt, art=0): result=None, time=0.01s, err=None, output=True/13129
ReportWithParameters(Z012resc.rpt, art=1): result=None, time=0.01s, err=None, output=True/14285
ReportWithParameters(Z012resc.rpt, art=2): result=None, time=0.01s, err=None, output=True/17650
ReportWithParameters(Z012resa.rpt, art=0): result=None, time=0.01s, err=None, output=True/12800
ReportWithParameters(Z012resa.rpt, art=1): result=None, time=0.01s, err=None, output=True/13956
ReportWithParameters(Z012resa.rpt, art=2): result=None, time=0.01s, err=None, output=True/18000
ReportWithParameters(Z012resi.rpt, art=0): result=None, time=0.01s, err=None, output=True/12843
ReportWithParameters(Z012resi.rpt, art=1): result=None, time=0.01s, err=None, output=True/13999
ReportWithParameters(Z012resi.rpt, art=2): result=None, time=0.01s, err=None, output=True/18086


## DB tests

GetDBName('KMAT', 'Material', 0, 1, 0): '', time=0.00s, err=None
GetDBName('Z000', 'Material', 0, 1, 0): '', time=0.00s, err=None
GetDBName('M000', 'Material', 0, 1, 0): '', time=0.00s, err=None
GetDBName('W000', 'Material', 0, 1, 0): '', time=0.05s, err=None
GetDBName('KMAT', 'MATERIAL', 0, 1, 0): '', time=0.00s, err=None
GetDBName('KMAT', 'Material', 1, 1, 0): '', time=0.00s, err=None
GetDBName('KMAT', 'Material', 0, 0, 0): '', time=0.00s, err=None


## Configuration tests

SetSilentMode(0): result=None, time=0.00s, err=None
SetSilentMode(1): result=None, time=0.00s, err=None
SetLanguage(0): result=None, time=0.05s, err=None
SetLanguage(1): result=None, time=0.09s, err=None
SetLanguage(2): result=None, time=0.05s, err=None
GetLanguage after: 2
SetDebugFile('C:\Users\Full stop\Desktop\kisssoft_debug.log'): result=None, time=0.00s, err=None
ShowInterface(0): result=None, time=0.00s, err=None
ShowInterface(1): result=None, time=0.00s, err=None


## Callback test

SetCallback('test', callback): result=None, time=0.00s, err=TypeError: The Python instance can not be converted to a COM object


## Message test

Message('Test message', 0, 1): result=(('Corrupt file!',), (3,), 1), time=0.00s, err=None


## Error handling tests

GetModule('INVALID', False): result=None, time=0.00s, err=None
IsModuleValid after invalid: True
LoadFile(nonexistent): result=None, time=0.00s, err=None
GetVarAsJson('INVALID.VAR.NAME'): result={"status_code":"not_found","status_msg":"Coult not find requested variable"}, time=0.00s, err=None
GetVarAsJson(''): result={"status_code":"not_found","status_msg":"Coult not find requested variable"}, time=0.00s, err=None


## License check

CheckLicense('Z012'): True, time=0.00s, err=None
CheckLicense('Z011'): True, time=0.00s, err=None
CheckLicense('Z015'): True, time=0.00s, err=None
CheckLicense('W010'): True, time=0.00s, err=None
CheckLicense('S020'): True, time=0.00s, err=None
CheckLicense('INVALID'): False, time=0.00s, err=None