# KISSsoft 2024 Module Loadability Report

Generated: 2026-07-10T09:21:12.747131

## Summary

- Fully available (valid + load + calculate): 24
- Module invalid (IsModuleValid False): 0
- Load failed (valid but LoadFile failed): 1
- Calculate failed (valid + loaded but CalculateRetVal failed): 1

## Fully Available Modules

- **Z011**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur.Z11` | result: ZPP[0].Fuss.SFnorm={"return_value":0.0,"status_code":"ok"}
- **Z012**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12` | result: ZPP[0].Fuss.SFnorm={"return_value":2.5513426055976467,"status_code":"ok"}
- **Z013**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Rack and Pinion.Z13` | result: ZPP[0].Fuss.SFnorm={"return_value":3.1114299644092527,"status_code":"ok"}
- **Z014**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Planetary (ISO 6336).Z14` | result: ZPP[0].Fuss.SFnorm={"return_value":4.31351958261616,"status_code":"ok"}
- **Z015**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Three Gears (DIN 3990).Z15` | result: ZPP[0].Fuss.SFnorm={"return_value":4.865082122429253,"status_code":"ok"}
- **Z016**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\03 Four Gears (ISO 6336).Z16` | result: ZPP[0].Fuss.SFnorm={"return_value":12.77235696707857,"status_code":"ok"}
- **Z050**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Beveloid (Crowning).Z50` | result: ZPP[0].Fuss.SFnorm={"return_value":3.474447539044542,"status_code":"ok"}
- **Z060**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Face Gear.Z60` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **Z070**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Bevel (KN 3028 FH).z70` | result: ZPP[0].Fuss.SFnorm={"return_value":1.7055555405661906,"status_code":"ok"}
- **Z080**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Worm (DIN 3996 Example 1).Z80` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **Z090**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 V Belt.Z90` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **W010**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Shafts.W10` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **M010**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Cylindrical Interference Fit.M10` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **M040**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Bolts (VDI 2230 Example 1).M40` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **M050**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\09 Shaft Ring.M50` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **M060**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\11 Hirth (Voith).M60` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **F010**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Compression Spring.F10` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **F020**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\03 Tension Spring.F20` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **F030**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\04 Leg Spring.F30` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **F040**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\05 Disk Spring.F40` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **F050**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\06 Torsion Bar Spring.F50` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **A010**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Gear Synchroniser.A10` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **A020**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\02 Coupling.A20` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}
- **K010**: `C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Tolerance Calculation.K10` | result: ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"}

## Module Invalid

_None_

## Load Failed

- **S020**: file=`C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Cylindrical Gear Stage.S20` | error=LoadFile error: (-2147417851, '服务器出现意外情况。', None, None)

## Calculate Failed

- **K019**: file=`C:\Program Files\KISSsoft AG\KISSsoft 2024\example\10 Load Spectrum Generator (Time Series to LDD).K19` | error=CalculateRetVal returned False

## Detailed Results

| Module | CheckLicense | IsModuleValid | Example File | LoadFile | CalculateRetVal | Result Var | Error |
|--------|--------------|---------------|--------------|----------|-----------------|------------|-------|
| Z011 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur.Z11 | True | True | ZPP[0].Fuss.SFnorm={"return_value":0.0,"status_code":"ok"} | N/A |
| Z012 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12 | True | True | ZPP[0].Fuss.SFnorm={"return_value":2.5513426055976467,"status_code":"ok"} | N/A |
| Z013 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Rack and Pinion.Z13 | True | True | ZPP[0].Fuss.SFnorm={"return_value":3.1114299644092527,"status_code":"ok"} | N/A |
| Z014 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Planetary (ISO 6336).Z14 | True | True | ZPP[0].Fuss.SFnorm={"return_value":4.31351958261616,"status_code":"ok"} | N/A |
| Z015 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Three Gears (DIN 3990).Z15 | True | True | ZPP[0].Fuss.SFnorm={"return_value":4.865082122429253,"status_code":"ok"} | N/A |
| Z016 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\03 Four Gears (ISO 6336).Z16 | True | True | ZPP[0].Fuss.SFnorm={"return_value":12.77235696707857,"status_code":"ok"} | N/A |
| Z050 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur Beveloid (Crowning).Z50 | True | True | ZPP[0].Fuss.SFnorm={"return_value":3.474447539044542,"status_code":"ok"} | N/A |
| Z060 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Face Gear.Z60 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| Z070 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Bevel (KN 3028 FH).z70 | True | True | ZPP[0].Fuss.SFnorm={"return_value":1.7055555405661906,"status_code":"ok"} | N/A |
| Z080 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Worm (DIN 3996 Example 1).Z80 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| Z090 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 V Belt.Z90 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| W010 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Shafts.W10 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| S020 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Cylindrical Gear Stage.S20 | False | False | N/A | LoadFile error: (-2147417851, '服务器出现意外情况。', None, None) |
| M010 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Cylindrical Interference Fit.M10 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| M040 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Bolts (VDI 2230 Example 1).M40 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| M050 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\09 Shaft Ring.M50 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| M060 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\11 Hirth (Voith).M60 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| F010 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Compression Spring.F10 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| F020 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\03 Tension Spring.F20 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| F030 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\04 Leg Spring.F30 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| F040 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\05 Disk Spring.F40 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| F050 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\06 Torsion Bar Spring.F50 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| A010 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Gear Synchroniser.A10 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| A020 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\02 Coupling.A20 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| K010 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Tolerance Calculation.K10 | True | True | ZPP[0].Fuss.SFnorm={"status_code":"not_found","status_msg":"Coult not find requested variable"} | N/A |
| K019 | True | True | C:\Program Files\KISSsoft AG\KISSsoft 2024\example\10 Load Spectrum Generator (Time Series to LDD).K19 | True | False | N/A | CalculateRetVal returned False |
