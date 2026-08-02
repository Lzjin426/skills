# KISSsoft 2024 COM 接口完整参考文档

> 来源：KISSsoft COM 2024 类型库、运行时测试、变量清单与模块授权测试结果
> 环境：Windows（main-long），KISSsoft 2024 SP1，License #1113
> ProgID：`KISSsoftCOM2024.KISSsoft`
> 最后更新：2026-07-10

---

## 目录

1. [概述与连接方式](#1-概述与连接方式)
2. [核心工作流](#2-核心工作流)
3. [顶层方法列表](#3-顶层方法列表)
4. [模块映射与 License 可用性](#4-模块映射与-license-可用性)
5. [常用变量路径（Z011-Z016）](#5-常用变量路径z011-z016)
6. [CallJsonFunc 有效函数名](#6-calljsonfunc-有效函数名)
7. [接触分析](#7-接触分析)
8. [参数扫描示例](#8-参数扫描示例)
9. [报告生成](#9-报告生成)
10. [文件操作](#10-文件操作)
11. [配置与错误处理](#11-配置与错误处理)
12. [已知限制与未探明项](#12-已知限制与未探明项)
13. [快速参考代码](#13-快速参考代码)
14. [参考来源](#14-参考来源)

---

## 1. 概述与连接方式

### 1.1 ProgID

```text
KISSsoftCOM2024.KISSsoft
```

### 1.2 Python 连接示例

```python
import win32com.client

ks = win32com.client.Dispatch("KISSsoftCOM2024.KISSsoft")

# 基础信息
print(ks.GetKsoftVersion())         # 2024
print(ks.GetKsoftPatchLevel())      # -SP1
print(ks.GetKsoftVersionSettings()) # 2024
print(ks.GetLanguage())             # 0（默认）/ 1 / 2
print(ks.IsActiveInterface())       # False（未激活 GUI）
print(ks.isActive())                # False（未加载模块）
print(ks.IsModuleValid())           # False（未加载模块）
print(ks.LicenseNumber())           # 1113
print(ks.GetININame())              # C:\Program Files\KISSsoft AG\KISSsoft 2024\kiss.ini
```

### 1.3 常用约定

- 所有变量路径均按字符串传入/读取。
- `SetVar` 的 `value` 参数必须是字符串；数值也需要先转换为字符串。
- `GetVar` 返回字符串，`GetVarAsJson` 返回带 `status_code` 的 JSON 对象，推荐用于读数。
- Windows 路径包含空格，请使用原始字符串 `r"..."` 或双反斜杠。

---

## 2. 核心工作流

标准自动化脚本遵循以下顺序：

```python
import win32com.client

ks = win32com.client.Dispatch("KISSsoftCOM2024.KISSsoft")

# 1. 获取模块
ks.GetModule("Z012", False)
assert ks.IsModuleValid()

# 2. 加载文件
ks.LoadFile(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")

# 3. 读取/设置变量
ks.SetVar("ZR[0].b", "45")
value = ks.GetVarAsJson("ZPP[0].Fuss.SFnorm")

# 4. 计算
ks.Calculate()
# 或
ok = ks.CalculateRetVal()

# 5. 读取结果
result = ks.GetVarAsJson("ZPP[0].Flanke.SH")
```

### 2.1 工作流说明

| 步骤 | 方法 | 说明 |
|------|------|------|
| 1 | `GetModule(modul, interactive)` | 必须先加载模块。`interactive=False` 表示不弹 GUI。 |
| 2 | `LoadFile(fileName)` | 加载对应模块的 `*.Z*` 文件。建议用原始字符串处理 Windows 路径。 |
| 3 | `SetVar(name, value)` | 所有值均以字符串传入；修改后必须重新 `Calculate()` 才能反映到结果。 |
| 4 | `Calculate()` / `CalculateRetVal()` | `Calculate()` 返回 `None`；`CalculateRetVal()` 返回 `True/False`。 |
| 5 | `GetVarAsJson(name)` | 推荐读取方式，返回 `{"return_value": ..., "status_code": "ok"}`。 |

---

## 3. 顶层方法列表

下表列出 `IKISSsoft2024` 接口暴露的主要方法，签名来自类型库，返回值基于运行时测试。

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `GetModule` | `(modul, interactive)` | 无 | 加载指定模块，如 `"Z012"` |
| `GetModuleOEM` | `(modul, interactive, OEMcode)` | 无 | OEM 版模块加载 |
| `ReleaseModule` | `()` | 无 | 释放当前模块 |
| `IsModuleValid` | `()` | `bool` | 当前模块是否有效 |
| `LoadFile` | `(fileName)` | 无 | 加载 `*.Z*` 文件 |
| `LoadFileData` | `(data)` | 无 | 从字符串数据加载 |
| `SaveFile` | `(fileName)` | 无 | 保存文件 |
| `Calculate` | `()` | 无 | 执行主计算 |
| `CalculateRetVal` | `()` | `bool` | 计算并返回是否成功 |
| `GetResultCount` | `()` | `int` | 结果数量 |
| `GetNextResult` | `()` | `str` | 下一个结果 |
| `SetVar` | `(name, value)` | 无 | 设置变量（值以字符串传入） |
| `GetVar` | `(name)` | `str` | 读取变量，返回字符串 |
| `GetVarAsJson` | `(nameBstr)` | `JSON` | 读取变量，返回带状态码的 JSON（推荐） |
| `CallFunc` | `(name)` | 无 | 调用无参内部函数 |
| `CallFuncNParam` | `(paramArray)` | 无 | 调用带参内部函数 |
| `CallJsonFunc` | `(functionName, arrayOfJsonArgs)` | `JSON` | JSON 风格调用 |
| `Report` | `(show)` | 无 | 生成默认报告 |
| `ReportWithParameters` | `(infile, outfile, show, art)` | 无 | 按指定模板生成报告 |
| `ShowInterface` | `(wait)` | 无 | 显示/隐藏 GUI |
| `SetSilentMode` | `(silent)` | 无 | 静默模式 |
| `SetLanguage` | `(index)` | 无 | 设置界面语言 |
| `GetLanguage` | `()` | `int` | 当前语言 |
| `CheckLicense` | `(name)` | `bool` | 检查 license 是否包含指定模块 |
| `LoadLicenseFile` | `(name)` | `bool` | 加载 license 文件 |
| `GetModulFromFile` | `(fileName)` | `str` | 返回文件所属模块 ID |
| `GetVersionFromFile` | `(fileName)` | `str` | 返回文件版本，如 `"24.0"` |
| `GetKsoftVersionFromFile` | `(fileName)` | `str` | 返回文件保存时 KISSsoft 版本 |
| `GetKsoftVersion` | `()` | `str` | 当前 KISSsoft 版本 |
| `GetKsoftPatchLevel` | `()` | `str` | Patch 级别 |
| `GetKsoftVersionSettings` | `()` | `str` | 设置版本 |
| `GetDBName` | `(db_name, table, flag, ID, order)` | `str` | 数据库名称查询 |
| `GetDBValue` | `(db_name, table, ID, fieldname)` | `str` | 数据库值查询 |
| `SetDebugFile` | `(fileName)` | 无 | 设置调试日志 |
| `SetCallback` | `(name, callback)` | 无 | 设置回调 |
| `Message` | `(strings, types, numElem)` | 无 | 消息处理 |
| `isActive` | `()` | `bool` | 接口是否处于激活状态 |
| `IsActiveInterface` | `()` | `bool` | GUI 接口是否激活 |
| `LicenseNumber` | `()` | `int` | License 编号 |
| `GetININame` | `()` | `str` | INI 文件路径 |

---

## 4. 模块映射与 License 可用性

### 4.1 文件扩展名 ↔ 模块 ID

| 文件扩展名 | 模块 ID | 说明 | 示例文件 |
|------------|---------|------|----------|
| `.Z11` | `Z011` | 单齿轮（Single gear） | `01 Spur.Z11` |
| `.Z12` | `Z012` | 平行轴齿轮副（Cylindrical gear pair） | `01 Spur (ISO 6336).Z12` |
| `.Z13` | `Z013` | 齿条齿轮（Rack and pinion） | `01 Spur Rack and Pinion.Z13` |
| `.Z14` | `Z014` | 行星齿轮（Planetary） | `01 Spur Planetary (ISO 6336).Z14` |
| `.Z15` | `Z015` | 三齿轮传动 | `01 Three Gears (DIN 3990).Z15` |
| `.Z16` | `Z016` | 四齿轮传动 | `03 Four Gears (ISO 6336).Z16` |
| `.Z50` | `Z050` | 锥齿轮/Beveloid | `01 Spur Beveloid (Crowning).Z50` |
| `.Z60` | `Z060` | 面齿轮（Face gear） | `01 Face Gear.Z60` |
| `.Z70` | `Z070` | 锥齿轮/准双曲面齿轮（Bevel/Hypoid） | `01 Bevel (KN 3028 FH).z70` |
| `.Z80` | `Z080` | 蜗杆（Worm） | `01 Worm (DIN 3996 Example 1).Z80` |
| `.Z90` | `Z090` | V 带 | `01 V Belt.Z90` |
| `.Z91` | `Z091` | 同步带 | `01 Toothed Belt.Z91` |
| `.Z92` | `Z092` | 链传动 | `04 Chain Drive.Z92` |
| `.Z40` | `Z040` | 连续滚刀/刀具 | `01 Continuous rotation.Z40` |
| `.S20` | `S020` | 齿轮箱系统（KISSdesign） | `01 Cylindrical Gear Stage.S20` |
| `.W10` | `W010` | 轴系（Shaft） | `01 Shafts.W10` |
| `.W50` | `W050` | 深沟球轴承 | `01 Deep Groove.W50` |
| `.W51` | `W051` | 深沟球轴承（内部几何） | `03 Deep Groove (Inner Geometry).W51` |
| `.W70` | `W070` | 滑动轴承（ISO 7902） | `07 Plain Journal Bearing.W70` |
| `.W7C` | `W07C` | 推力滑动轴承（DIN 31653） | `13 Plain Thrust Bearing.W7C` |
| `.M10` | `M010` | 圆柱过盈配合 | `01 Cylindrical Interference Fit.M10` |
| `.M40` | `M040` | 螺栓（VDI 2230） | `01 Bolts (VDI 2230 Example 1).M40` |
| `.M50` | `M050` | 轴用挡圈 | `09 Shaft Ring.M50` |
| `.M60` | `M060` | Hirth 齿 | `11 Hirth (Voith).M60` |
| `.F10` | `F010` | 压缩弹簧 | `01 Compression Spring.F10` |
| `.F20` | `F020` | 拉伸弹簧 | `03 Tension Spring.F20` |
| `.F30` | `F030` | 板弹簧 | `04 Leg Spring.F30` |
| `.F40` | `F040` | 碟形弹簧 | `05 Disk Spring.F40` |
| `.F50` | `F050` | 扭杆弹簧 | `06 Torsion Bar Spring.F50` |
| `.A10` | `A010` | 齿轮同步器 | `01 Gear Synchroniser.A10` |
| `.A20` | `A020` | 联轴器 | `02 Coupling.A20` |
| `.K10` | `K010` | 公差计算 | `01 Tolerance Calculation.K10` |
| `.K12` | `K012` | FKM 应力分析 | `02 Stress Analysis (FKM 62).K12` |
| `.K14` | `K014` | 赫兹接触压力 | `04 Hertzian Pressure.K14` |
| `.K15` | `K015` | 线性驱动 | `07 Linear Drive.K15` |
| `.K17` | `K017` | 塑料管理器 | `09 Plastics Manager.K17` |
| `.K19` | `K019` | 载荷谱生成器 | `10 Load Spectrum Generator.K19` |

### 4.2 当前 License 可用模块

经 `GetModule(..., interactive=False)` 与 `IsModuleValid()` 实测：

| 模块 ID | 状态 | 说明 |
|---------|------|------|
| `Z011` | 可用 | 单齿轮 |
| `Z012` | 可用 | 平行轴齿轮副 |
| `Z013` | 可用 | 齿条齿轮 |
| `Z014` | 可用 | 行星齿轮 |
| `Z015` | 可用 | 三齿轮传动 |
| `Z016` | 可用 | 四齿轮传动 |
| `Z017` | 未授权 | 斜齿轮（Niemann） |
| `Z050` 及以后 | 未授权 | 锥齿轮、面齿轮、蜗杆、带、链等 |
| `W010`、`W050`、`W051`、`W070`、`W07C` | 未授权 | 轴、轴承 |
| `S020` | 未授权 | 齿轮箱系统 |
| `M010`、`M040`、`M050`、`M060` | 未授权 | 连接/紧固件 |
| `F010` ~ `F050` | 未授权 | 弹簧 |
| `A010`、`A020` | 未授权 | 同步器/联轴器 |
| `K010` ~ `K019` | 未授权 | 工具/辅助模块 |

---

## 5. 常用变量路径（Z011-Z016）

下表按模块列出已通过 `GetModule` → `LoadFile` → `Calculate` → `GetVarAsJson` 实测可用的常用变量。未特殊说明时，示例值来自默认示例文件。

### 5.1 Z011 — 单齿轮（Single gear）

- 示例文件：`01 Spur.Z11`
- 测试变量总数：74，可用：74，不可用：0

#### 常用输入变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `RechSt.GeometrieMeth` | `1` | 几何计算方法 |
| 2 | `RechSt.TolDIN3962` | `False` | 是否按 DIN 3962 公差 |
| 3 | `RechSt.TolISO1328v1995` | `False` | 是否按 ISO 1328:1995 公差 |
| 4 | `RechSt.TolMethode` | `0` | 公差方法 |
| 5 | `RechSt.TolWahl` | `0` | 公差选择 |
| 6 | `RechSt.ZahnZNachK` | `0` | 齿数计算选项 |
| 7 | `RechSt.asymmetric` | `False` | 非对称齿形 |
| 8 | `Setup.ReportLanguage` | `2` | 报告语言 |
| 9 | `ZR[0].CoreHV` | `0.0` | 核心硬度 HV |
| 10 | `ZR[0].HardnessHB` | `652.406` | 布氏硬度 HB |
| 11 | `ZR[0].Tool.Hob.isShortPitch` | `False` | 短节距滚刀 |
| 12 | `ZR[0].Tool.finishing` | `True` | 精加工 |
| 13 | `ZR[0].b` | `10.0` | 齿宽（mm） |
| 14 | `ZR[0].mat.DBID` | `10260` | 材料数据库 ID |
| 15 | `ZR[0].mat.E` | `206000.0` | 弹性模量（MPa） |
| 16 | `ZR[0].mat.Rm` | `1200.0` | 抗拉强度（MPa） |
| 17 | `ZR[0].mat.Rp` | `850.0` | 屈服强度（MPa） |
| 18 | `ZR[0].mat.bez` | `18CrNiMo7-6` | 材料名称 |
| 19 | `ZR[0].x.E` | `0.2258` | 弹性变形下变位系数 |
| 20 | `ZR[0].x.i` | `0.1846` | 初始变位系数 |
| 21 | `ZR[0].x.nul` | `0.3` | 无载荷变位系数 |
| 22 | `ZR[0].z` | `17.0` | 齿数 |
| 23 | `ZR[1].CoreHV` | `0.0` | 第二齿轮核心硬度 |
| 24 | `ZR[1].HardnessHB` | `0.0` | 第二齿轮硬度 |
| 25 | `ZR[1].b` | `0.0` | 第二齿轮齿宽 |
| 26 | `ZR[1].mat.DBID` | `10260` | 第二齿轮材料 ID |
| 27 | `ZR[1].mat.E` | `0.0` | 第二齿轮弹性模量 |
| 28 | `ZR[1].mat.bez` | `` | 第二齿轮材料名称 |
| 29 | `ZR[1].z` | `0.0` | 第二齿轮齿数 |
| 30 | `ZS.AnzRad` | `0` | 齿轮数量 |

#### 常用输出变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZP[0].u` | `0.0` | 传动比 |
| 2 | `ZR[0].AngleFaseb` | `45.0` | 倒角角度 |
| 3 | `ZR[0].BM` | `0.0` | 齿宽中点 |
| 4 | `ZR[0].Ca` | `-0.0` | 齿顶修缘 |
| 5 | `ZR[0].Cf` | `-0.0` | 齿根修缘 |
| 6 | `ZR[0].CoreHB` | `0.0` | 核心布氏硬度 |
| 7 | `ZR[0].Faseb` | `0.0` | 倒角宽度 |
| 8 | `ZR[0].Flanke.ZNT` | `0.0` | 接触寿命系数 |
| 9 | `ZR[0].Flanke.ZX` | `1.0` | 接触尺寸系数 |
| 10 | `ZR[0].Fuss.YB` | `1.0` | 弯曲粗糙度系数 |
| 11 | `ZR[0].Fuss.YCHD` | `1.0` | 弯曲喷丸系数 |
| 12 | `ZR[0].Fuss.YDS` | `0.0` | 弯曲尺寸系数 |
| 13 | `ZR[0].d` | `17.0` | 分度圆直径 |
| 14 | `ZR[0].dCaMesure` | `0.0` | 齿顶圆测量值 |
| 15 | `ZR[0].dNa.nul` | `0.0` | 无载荷齿顶圆 |
| 16 | `ZR[0].dNaMesure` | `0.0` | 齿顶圆测量值 |
| 17 | `ZR[0].dNf.nul` | `0.0` | 无载荷齿根圆 |
| 18 | `ZR[0].da.nul` | `19.6` | 无载荷齿顶圆直径 |
| 19 | `ZR[0].df.nul` | `15.1` | 无载荷齿根圆直径 |
| 20 | `ZR[0].diCalc` | `0.0` | 计算内径 |
| 21 | `ZR[0].zn` | `17.0` | 当量齿数 |
| 22 | `ZR[1].AngleFaseb` | `45.0` | 第二齿轮倒角 |
| 23 | `ZR[1].BM` | `0.0` | 第二齿轮齿宽中点 |
| 24 | `ZR[1].Ca` | `0.0` | 第二齿轮齿顶修缘 |
| 25 | `ZR[1].Cf` | `0.0` | 第二齿轮齿根修缘 |
| 26 | `ZR[1].CoreHB` | `0.0` | 第二齿轮核心硬度 |
| 27 | `ZR[1].Faseb` | `0.0` | 第二齿轮倒角宽度 |
| 28 | `ZR[1].d` | `0.0` | 第二齿轮分度圆 |
| 29 | `ZR[1].dCaMesure` | `0.0` | 第二齿轮齿顶测量 |
| 30 | `ZR[1].dNa.nul` | `0.0` | 第二齿轮无载荷齿顶圆 |

### 5.2 Z012 — 平行轴齿轮副（Cylindrical gear pair）

- 示例文件：`01 Spur (ISO 6336).Z12`
- 测试变量总数：106，可用：106，不可用：0

#### 常用输入变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `RechSt.CalculateP_Usage` | `False` | 是否计算功率损失 |
| 2 | `RechSt.Flankbreak` | `1` | 齿面断裂计算开关 |
| 3 | `RechSt.GeometrieMeth` | `1` | 几何计算方法 |
| 4 | `RechSt.Konfig` | `2` | 配置 ID |
| 5 | `RechSt.MicropittingStandard` | `1` | 微点蚀标准 |
| 6 | `RechSt.RechenMeth` | `0` | 计算方法 |
| 7 | `RechSt.RechenMethID` | `10029` | 计算方法 ID（如 ISO 6336 版本） |
| 8 | `RechSt.RechenMethSpez` | `0` | 计算方法特殊选项 |
| 9 | `RechSt.ScoringStandard` | `0` | 胶合标准 |
| 10 | `RechSt.TolDIN3962` | `False` | DIN 3962 公差 |
| 11 | `RechSt.TolISO1328v1995` | `False` | ISO 1328:1995 公差 |
| 12 | `RechSt.TolMethode` | `0` | 公差方法 |
| 13 | `RechSt.TolWahl` | `0` | 公差选择 |
| 14 | `RechSt.VDI2737Calc` | `0` | VDI 2737 计算 |
| 15 | `RechSt.ZahnZNachK` | `0` | 齿数选项 |
| 16 | `RechSt.asymmetric` | `False` | 非对称齿形 |
| 17 | `Setup.ReportLanguage` | `2` | 报告语言 |
| 18 | `ZR[0].CoreHV` | `342.0` | 小齿轮核心硬度 |
| 19 | `ZR[0].HardnessHB` | `652.406` | 小齿轮硬度 |
| 20 | `ZR[0].b` | `44.0` | 小齿轮齿宽（mm） |
| 21 | `ZR[0].mat.DBID` | `10260` | 小齿轮材料 ID |
| 22 | `ZR[0].mat.E` | `206000.0` | 小齿轮弹性模量 |
| 23 | `ZR[0].mat.bez` | `18CrNiMo7-6` | 小齿轮材料名称 |
| 24 | `ZR[0].x.E` | `0.2267` | 小齿轮弹性变位系数 |
| 25 | `ZR[0].x.nul` | `0.2485` | 小齿轮无载荷变位系数 |
| 26 | `ZR[0].z` | `25.0` | 小齿轮齿数 |
| 27 | `ZR[1].CoreHV` | `342.0` | 大齿轮核心硬度 |
| 28 | `ZR[1].HardnessHB` | `652.406` | 大齿轮硬度 |
| 29 | `ZR[1].b` | `44.0` | 大齿轮齿宽 |
| 30 | `ZR[1].mat.DBID` | `10260` | 大齿轮材料 ID |

#### 常用输出变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZPP[0].Fa` | `0.0` | 轴向力 |
| 2 | `ZPP[0].Flanke.SH` | `1.3328` | 小齿轮齿面接触安全系数 |
| 3 | `ZPP[0].Flanke.SHw` | `1.3416` | 小齿轮齿面接触安全系数（另一形式） |
| 4 | `ZPP[0].Flanke.ZL` | `1.0200` | 润滑油系数 |
| 5 | `ZPP[0].Flanke.ZR` | `0.9801` | 粗糙度系数 |
| 6 | `ZPP[0].Flanke.ZV` | `0.9742` | 速度系数 |
| 7 | `ZPP[0].Flanke.ZW` | `1.0` | 齿面工作硬化系数 |
| 8 | `ZPP[0].Flanke.sigHBD` | `1019.554` | 接触疲劳极限 |
| 9 | `ZPP[0].Flanke.sigHP` | `1358.905` | 接触许用应力 |
| 10 | `ZPP[0].Fnorm` | `23053.877` | 法向力 |
| 11 | `ZPP[0].Fr` | `7884.890` | 径向力 |
| 12 | `ZPP[0].Fuss.SF` | `2.5513` | 小齿轮齿根弯曲安全系数 |
| 13 | `ZPP[0].Fuss.SFnorm` | `2.5513` | 小齿轮齿根弯曲安全系数（归一化） |
| 14 | `ZPP[0].Fuss.YF` | `1.2462` | 齿形系数 |
| 15 | `ZPP[0].Fuss.YS` | `2.1101` | 应力修正系数 |
| 16 | `ZPP[0].Fuss.sigF` | `286.871` | 齿根应力 |
| 17 | `ZPP[0].Fuss.sigFP` | `731.906` | 齿根许用应力 |
| 18 | `ZPP[0].Kga` | `0.3051` | 齿顶修形量 |
| 19 | `ZPP[0].Kgf` | `-0.2186` | 齿根修形量 |
| 20 | `ZPP[0].c.E` | `1.8270` | 弹性变形中心距 |
| 21 | `ZPP[0].c.i` | `1.6626` | 初始中心距 |
| 22 | `ZPP[0].c.nul` | `1.5` | 无载荷中心距 |
| 23 | `ZPP[0].d_B.nul` | `149.664` | 无载荷基圆直径 |
| 24 | `ZPP[0].d_D.nul` | `154.008` | 无载荷直径 |
| 25 | `ZPP[0].dw` | `150.0` | 工作节圆直径 |
| 26 | `ZPP[0].eps.E` | `0.9727` | 弹性变形端面重合度 |
| 27 | `ZPP[0].eps.i` | `0.9660` | 初始端面重合度 |
| 28 | `ZPP[0].eps.nul` | `0.9720` | 无载荷端面重合度 |
| 29 | `ZPP[0].flankbreak.SFFB` | `1.2094` | 齿面断裂安全系数 |
| 30 | `ZPP[0].flankbreak.SFFBnom` | `1.2094` | 齿面断裂安全系数（归一化） |

### 5.3 Z013 — 齿条齿轮（Rack and pinion）

- 示例文件：`01 Spur Rack and Pinion.Z13`
- 测试变量总数：538，可用变量数：232

#### 常用输入变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZS.Geo.mn` | `1.5` | 法向模数（mm） |
| 2 | `ZS.Geo.beta` | `0.0` | 螺旋角（°） |
| 3 | `ZR[0].z` | `18.0` | 小齿轮齿数 |
| 4 | `ZR[1].z` | `-9000.0` | 齿条齿数（虚拟值） |
| 5 | `ZR[2].z` | `0.0` | 第三构件齿数 |
| 6 | `ZR[0].b` | `20.0` | 小齿轮齿宽（mm） |
| 7 | `ZR[1].b` | `18.0` | 齿条齿宽（mm） |
| 8 | `ZR[2].b` | `0.0` | 第三构件齿宽 |
| 9 | `ZR[0].x.nul` | `0.25` | 小齿轮无载荷变位系数 |
| 10 | `ZR[1].x.nul` | `0.0` | 齿条变位系数 |
| 11 | `ZR[2].x.nul` | `0.0` | 第三构件变位系数 |
| 12 | `ZR[0].da.nul` | `30.75` | 小齿轮无载荷齿顶圆直径 |
| 13 | `ZR[0].df.nul` | `24.0` | 小齿轮无载荷齿根圆直径 |
| 14 | `ZR[0].d.nul` | `27.0` | 小齿轮无载荷分度圆直径 |
| 15 | `ZR[1].da.nul` | `-13497.0` | 齿条无载荷齿顶圆 |
| 16 | `ZR[1].df.nul` | `-13503.75` | 齿条无载荷齿根圆 |
| 17 | `ZR[1].d.nul` | `-13500.0` | 齿条无载荷分度圆 |
| 18 | `ZR[2].da.nul` | `0.0` | 第三构件齿顶圆 |
| 19 | `ZR[2].df.nul` | `0.0` | 第三构件齿根圆 |
| 20 | `ZR[2].d.nul` | `0.0` | 第三构件分度圆 |
| 21 | `ZR[0].mat.bez` | `42 CrMo 4 (3)` | 小齿轮材料名称 |
| 22 | `ZR[1].mat.bez` | `C45 (1)` | 齿条材料名称 |
| 23 | `RechSt.RechenMethID` | `10080` | 计算方法 ID |
| 24 | `RechSt.RechenMeth` | `3` | 计算方法 |
| 25 | `RechSt.RechenMethSpez` | `0` | 计算方法特殊选项 |
| 26 | `RechSt.GeometrieMeth` | `1` | 几何计算方法 |
| 27 | `RechSt.Konfig` | `3` | 配置 ID |
| 28 | `RechSt.TolWahl` | `3` | 公差选择 |
| 29 | `Zst.KHbVariant` | `0` | KHβ 变体 |
| 30 | `ZR[2].mat.bez` | `` | 第三构件材料名称（JSON only） |

#### 常用输出变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZPP[0].Fuss.SF` | `3.1114` | 小齿轮齿根弯曲安全系数 |
| 2 | `ZPP[0].Fuss.SFnorm` | `3.1114` | 小齿轮齿根弯曲安全系数（归一化） |
| 3 | `ZPP[0].Flanke.SH` | `0.7060` | 小齿轮齿面接触安全系数 |
| 4 | `ZPP[1].Fuss.SF` | `1.5640` | 齿条齿根弯曲安全系数 |
| 5 | `ZPP[1].Fuss.SFnorm` | `1.5640` | 齿条齿根弯曲安全系数（归一化） |
| 6 | `ZPP[1].Flanke.SH` | `0.5067` | 齿条齿面接触安全系数 |
| 7 | `ZPP[2].Fuss.SF` | `0.0` | 第三构件弯曲安全系数 |
| 8 | `ZPP[2].Fuss.SFnorm` | `0.0` | 第三构件弯曲安全系数（归一化） |
| 9 | `ZPP[2].Flanke.SH` | `0.0` | 第三构件接触安全系数 |
| 10 | `ZPP[3].Fuss.SF` | `0.0` | 第四构件弯曲安全系数 |
| 11 | `ZPP[3].Fuss.SFnorm` | `0.0` | 第四构件弯曲安全系数（归一化） |
| 12 | `ZPP[3].Flanke.SH` | `0.0` | 第四构件接触安全系数 |
| 13 | `ZP[0].u` | `-500.0` | 传动比 |
| 14 | `ZP[1].u` | `0.0` | 第二对传动比 |
| 15 | `ZP[2].u` | `0.0` | 第三对传动比 |
| 16 | `ZP[0].KHb_nominal` | `1.3816` | 名义齿向载荷分布系数 |
| 17 | `ZP[1].KHb_nominal` | `0.0` | 第二对 KHβ |
| 18 | `ZP[2].KHb_nominal` | `1.0` | 第三对 KHβ |
| 19 | `ZPP[0].gamPC.A` | `0.3178` | 啮合刚度系数 A |
| 20 | `ZPP[0].gamPC.B` | `0.1545` | 啮合刚度系数 B |
| 21 | `ZPP[0].gamPC.C` | `0.1002` | 啮合刚度系数 C |
| 22 | `ZPP[1].gamPC.A` | `0.0003` | 齿条啮合刚度系数 A |
| 23 | `ZPP[1].gamPC.B` | `-4.01e-05` | 齿条啮合刚度系数 B |
| 24 | `ZPP[1].gamPC.C` | `-0.0001` | 齿条啮合刚度系数 C |
| 25 | `ZPP[2].gamPC.A` | `0.0` | 第三构件啮合刚度 A |
| 26 | `ZPP[2].gamPC.B` | `0.0` | 第三构件啮合刚度 B |
| 27 | `ZPP[2].gamPC.C` | `0.0` | 第三构件啮合刚度 C |
| 28 | `caResults.TransmissionError.delta` | `0.0` | 传动误差 |
| 29 | `caResults.MaxHertzianStress` | `0.0` | 最大赫兹应力 |
| 30 | `caResults.PowerLoss.average` | `0.0` | 平均功率损失 |

### 5.4 Z014 — 行星齿轮（Planetary gear）

- 示例文件：`01 Spur Planetary (ISO 6336).Z14`
- 测试变量总数：636，可用变量数：328

#### 常用输入变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZS.Geo.mn` | `1.3` | 法向模数（mm） |
| 2 | `ZS.Geo.beta` | `0.0` | 螺旋角（°） |
| 3 | `ZR[0].z` | `22.0` | 太阳轮齿数 |
| 4 | `ZR[1].z` | `27.0` | 行星轮齿数 |
| 5 | `ZR[2].z` | `-77.0` | 齿圈齿数 |
| 6 | `ZR[0].b` | `10.0` | 太阳轮齿宽 |
| 7 | `ZR[1].b` | `10.0` | 行星轮齿宽 |
| 8 | `ZR[2].b` | `10.0` | 齿圈齿宽 |
| 9 | `ZR[0].x.nul` | `0.3` | 太阳轮变位系数 |
| 10 | `ZR[1].x.nul` | `0.5890` | 行星轮变位系数 |
| 11 | `ZR[2].x.nul` | `-0.9021` | 齿圈变位系数 |
| 12 | `ZR[0].da.nul` | `31.748` | 太阳轮齿顶圆 |
| 13 | `ZR[0].df.nul` | `26.13` | 太阳轮齿根圆 |
| 14 | `ZR[0].d.nul` | `28.6` | 太阳轮分度圆 |
| 15 | `ZR[1].da.nul` | `38.999` | 行星轮齿顶圆 |
| 16 | `ZR[1].df.nul` | `33.381` | 行星轮齿根圆 |
| 17 | `ZR[1].d.nul` | `35.1` | 行星轮分度圆 |
| 18 | `ZR[2].da.nul` | `-99.845` | 齿圈齿顶圆 |
| 19 | `ZR[2].df.nul` | `-105.366` | 齿圈齿根圆 |
| 20 | `ZR[2].d.nul` | `-100.1` | 齿圈分度圆 |
| 21 | `ZR[0].mat.bez` | `18CrNiMo7-6` | 太阳轮材料 |
| 22 | `ZR[1].mat.bez` | `18CrNiMo7-6` | 行星轮材料 |
| 23 | `ZR[2].mat.bez` | `34 CrNiMo 6 (1)` | 齿圈材料 |
| 24 | `RechSt.RechenMethID` | `10029` | 计算方法 ID |
| 25 | `RechSt.RechenMeth` | `0` | 计算方法 |
| 26 | `RechSt.RechenMethSpez` | `0` | 计算方法特殊选项 |
| 27 | `RechSt.GeometrieMeth` | `1` | 几何计算方法 |
| 28 | `RechSt.Konfig` | `4` | 配置 ID |
| 29 | `RechSt.TolWahl` | `0` | 公差选择 |
| 30 | `Zst.KHbVariant` | `0` | KHβ 变体 |

#### 常用输出变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZPP[0].Fuss.SF` | `4.3135` | 太阳轮齿根弯曲安全系数 |
| 2 | `ZPP[0].Fuss.SFnorm` | `4.3135` | 太阳轮齿根弯曲安全系数（归一化） |
| 3 | `ZPP[0].Flanke.SH` | `1.3108` | 太阳轮齿面接触安全系数 |
| 4 | `ZPP[1].Fuss.SF` | `3.2473` | 行星轮齿根弯曲安全系数 |
| 5 | `ZPP[1].Fuss.SFnorm` | `3.2473` | 行星轮齿根弯曲安全系数（归一化） |
| 6 | `ZPP[1].Flanke.SH` | `1.4618` | 行星轮齿面接触安全系数 |
| 7 | `ZPP[2].Fuss.SF` | `3.4017` | 齿圈齿根弯曲安全系数 |
| 8 | `ZPP[2].Fuss.SFnorm` | `3.4017` | 齿圈齿根弯曲安全系数（归一化） |
| 9 | `ZPP[2].Flanke.SH` | `2.2775` | 齿圈齿面接触安全系数 |
| 10 | `ZPP[3].Fuss.SF` | `3.0418` | 第四构件齿根弯曲安全系数 |
| 11 | `ZPP[3].Fuss.SFnorm` | `3.0418` | 第四构件齿根弯曲安全系数（归一化） |
| 12 | `ZPP[3].Flanke.SH` | `1.1332` | 第四构件齿面接触安全系数 |
| 13 | `ZP[0].u` | `1.2273` | 第一对传动比 |
| 14 | `ZP[1].u` | `-2.8519` | 第二对传动比 |
| 15 | `ZP[2].u` | `0.0` | 第三对传动比 |
| 16 | `ZP[0].KHb_nominal` | `1.4279` | 第一对 KHβ |
| 17 | `ZP[1].KHb_nominal` | `1.4464` | 第二对 KHβ |
| 18 | `ZP[2].KHb_nominal` | `1.0` | 第三对 KHβ |
| 19 | `ZPP[0].gamPC.A` | `0.2593` | 啮合刚度 A |
| 20 | `ZPP[0].gamPC.B` | `0.2049` | 啮合刚度 B |
| 21 | `ZPP[0].gamPC.C` | `0.0681` | 啮合刚度 C |
| 22 | `ZPP[1].gamPC.A` | `3.0467` | 第二对啮合刚度 A |
| 23 | `ZPP[1].gamPC.B` | `3.0910` | 第二对啮合刚度 B |
| 24 | `ZPP[1].gamPC.C` | `3.2024` | 第二对啮合刚度 C |
| 25 | `ZPP[2].gamPC.A` | `-0.1540` | 第三对啮合刚度 A |
| 26 | `ZPP[2].gamPC.B` | `-0.0906` | 第三对啮合刚度 B |
| 27 | `ZPP[2].gamPC.C` | `-0.0695` | 第三对啮合刚度 C |
| 28 | `caResults.TransmissionError.delta` | `0.0` | 传动误差 |
| 29 | `caResults.MaxHertzianStress` | `0.0` | 最大赫兹应力 |
| 30 | `caResults.PowerLoss.average` | `0.0` | 平均功率损失 |

### 5.5 Z015 — 三齿轮传动

- 示例文件：`01 Three Gears (DIN 3990).Z15`
- 状态：模块有效、文件加载成功、计算成功

#### 常用输入/输出变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZR[0].x.nul` | `0.5` | 第一齿轮无载荷变位系数 |
| 2 | `ZS.Geo.beta` | `0.0` | 螺旋角（°） |
| 3 | `ZS.Geo.mn` | `0.2` | 法向模数（mm） |
| 4 | `ZR[0].da.E` | `2.976` | 第一齿轮弹性齿顶圆 |
| 5 | `ZR[0].da.nul` | `2.976` | 第一齿轮无载荷齿顶圆 |
| 6 | `ZR[0].df.E` | `2.056` | 第一齿轮弹性齿根圆 |
| 7 | `ZR[0].df.nul` | `2.1` | 第一齿轮无载荷齿根圆 |
| 8 | `ZP[0].Eps.b` | `0.0` | 轴向重合度 |
| 9 | `ZP[0].Eps.a` | `1.2494` | 端面重合度 |
| 10 | `ZR[0].KM.MdK.nul` | `3.3097` | 无载荷扭矩系数 |
| 11 | `ZR[0].KM.Wk.nul` | `1.5781` | 无载荷转速系数 |
| 12 | `ZR[0].mat.typ` | `2` | 材料类型 |
| 13 | `ZR[0].mat.DBID` | `10110` | 材料数据库 ID |
| 14 | `ZR[0].mat.bez` | `42 CrMo 4 (1)` | 材料名称 |
| 15 | `ZPP[0].Flanke.SH` | `0.4119` | 齿面接触安全系数 |
| 16 | `ZPP[0].Fuss.SF` | `4.8651` | 齿根弯曲安全系数 |
| 17 | `ZPP[0].Fuss.SFnorm` | `4.8651` | 齿根弯曲安全系数（归一化） |
| 18 | `ZR[0].mat.E` | `206000.0` | 弹性模量（MPa） |
| 19 | `ZPP[0].Fuss.sigF` | `109.770` | 齿根应力（MPa） |
| 20 | `ZR[0].b` | `2.0` | 齿宽（mm） |
| 21 | `ZR[0].z` | `12.0` | 齿数 |
| 22 | `ZPP[0].Flanke.sigHP` | `426.811` | 齿面许用应力（MPa） |
| 23 | `ZPP[0].Fuss.sigFP` | `534.040` | 齿根许用应力（MPa） |
| 24 | `ZP[0].a` | `2.8` | 中心距（mm） |
| 25 | `ZP[0].u` | `1.25` | 传动比 |
| 26 | `ZR[0].n` | `2000.0` | 转速（rpm） |
| 27 | `ZP[0].Flanke.sigH` | `973.760` | 齿面接触应力（MPa） |
| 28 | `ZS.Geo.alfn` | `0.3491` | 法向压力角（rad） |
| 29 | `ZS.Geo.mt` | `0.2` | 端面模数（mm） |
| 30 | `ZP[0].Eps.aEffE` | `1.2695` | 有效端面重合度 |

### 5.6 Z016 — 四齿轮传动

- 示例文件：`03 Four Gears (ISO 6336).Z16`
- 状态：模块有效、文件加载成功、计算成功

#### 常用输入/输出变量（30 个）

| 序号 | 变量路径 | 示例值 | 说明 |
|------|----------|--------|------|
| 1 | `ZR[0].x.nul` | `0.45` | 第一齿轮无载荷变位系数 |
| 2 | `ZS.Geo.beta` | `0.0` | 螺旋角（°） |
| 3 | `ZS.Geo.mn` | `1.5` | 法向模数（mm） |
| 4 | `ZR[0].da.E` | `26.732` | 第一齿轮弹性齿顶圆 |
| 5 | `ZR[0].da.nul` | `26.732` | 第一齿轮无载荷齿顶圆 |
| 6 | `ZR[0].df.E` | `20.0006` | 第一齿轮弹性齿根圆 |
| 7 | `ZR[0].df.nul` | `20.1` | 第一齿轮无载荷齿根圆 |
| 8 | `ZP[0].Eps.b` | `0.0` | 轴向重合度 |
| 9 | `ZP[0].Eps.a` | `1.3801` | 端面重合度 |
| 10 | `ZR[0].KM.MdK.nul` | `28.7867` | 无载荷扭矩系数 |
| 11 | `ZR[0].KM.Wk.nul` | `11.8473` | 无载荷转速系数 |
| 12 | `ZR[0].mat.typ` | `2` | 材料类型 |
| 13 | `ZR[0].mat.DBID` | `10110` | 材料数据库 ID |
| 14 | `ZR[0].mat.bez` | `42 CrMo 4 (1)` | 材料名称 |
| 15 | `ZPP[0].Flanke.SH` | `1.0512` | 齿面接触安全系数 |
| 16 | `ZPP[0].Fuss.SF` | `12.7724` | 齿根弯曲安全系数 |
| 17 | `ZPP[0].Fuss.SFnorm` | `12.7724` | 齿根弯曲安全系数（归一化） |
| 18 | `ZR[0].mat.E` | `206000.0` | 弹性模量（MPa） |
| 19 | `ZPP[0].Fuss.sigF` | `39.4234` | 齿根应力（MPa） |
| 20 | `ZR[0].b` | `10.0` | 齿宽（mm） |
| 21 | `ZR[0].z` | `15.0` | 齿数 |
| 22 | `ZPP[0].Flanke.sigHP` | `506.692` | 齿面许用应力（MPa） |
| 23 | `ZPP[0].Fuss.sigFP` | `503.530` | 齿根许用应力（MPa） |
| 24 | `ZP[0].a` | `34.5` | 中心距（mm） |
| 25 | `ZP[0].u` | `2.0` | 传动比 |
| 26 | `ZR[0].n` | `2000.0` | 转速（rpm） |
| 27 | `ZP[0].Flanke.sigH` | `457.153` | 齿面接触应力（MPa） |
| 28 | `ZS.Geo.alfn` | `0.3491` | 法向压力角（rad） |
| 29 | `ZS.Geo.mt` | `1.5` | 端面模数（mm） |
| 30 | `ZP[0].Eps.aEffE` | `1.3873` | 有效端面重合度 |

---

## 6. CallJsonFunc 有效函数名

`CallJsonFunc(functionName, arrayOfJsonArgs)` 在 249 个候选函数中，仅以下函数返回 `status_code: ok` 或实际值。其余函数大多返回 `not_implemented` / `bad_function_call`，或抛出异常。

### 6.1 已确认有效函数

| 函数名 | 推荐 JSON 参数 | 返回值/状态 | 说明 |
|--------|----------------|-------------|------|
| `GenerateReport` | `["<rpt路径>", "<out路径>"]` | `{"return_value": "C:/Windows/TEMP/KISS_4\\Z012.pprpt", "status_code": "ok"}` | 按模板生成报告，返回临时报告文件路径 |
| `GetConsistency` | `[]` 或 `{}` | `{"return_value": 0 或 1, "status_code": "ok"}` | 一致性检查，`1` 表示通过 |
| `ModuleID` | `[]` 或 `{}` | `{"return_value": "Z012", "status_code": "ok"}` | 返回当前模块 ID |
| `NewGraphic` | `[]` 或 `{}` | `{"return_value": null, "status_code": "ok"}` | 创建新图形对象 |
| `ShowGraphic` | `[]` 或 `{}` | `{"return_value": null, "status_code": "ok"}` | 显示图形 |
| `Temp_Dir` | `[]` 或 `{}` | `{"return_value": "C:/Windows/TEMP/KISS_4\\", "status_code": "ok"}` | 返回 KISSsoft 临时目录 |

### 6.2 在部分模块中返回成功但未稳定确认

| 函数名 | 观察到的返回值 | 说明 |
|--------|----------------|------|
| `Calculate` | `{"return_value": 1, "status_code": "ok"}` | 在 Z013/Z014 测试中出现，但与直接 `ks.Calculate()` 冲突，不推荐通过 `CallJsonFunc` 调用 |
| `CalculateStdCA` | `{"return_value": true, "status_code": "ok"}` | 标准接触分析计算 |
| `FineSizing` | `{"return_value": true, "status_code": "ok"}` | 仅在 Z014 中观察到返回 `true`；几何变量未实际变化 |

### 6.3 调用示例

```python
# 生成报告（CallJsonFunc 方式）
result = ks.CallJsonFunc("GenerateReport", [
    r"C:\Program Files\KISSsoft AG\KISSsoft 2024\rpt\Z012resc.rpt",
    r"C:\Users\Full stop\Desktop\report_from_json.rtf"
])
print(result)

# 获取当前模块 ID
print(ks.CallJsonFunc("ModuleID", []))

# 获取临时目录
print(ks.CallJsonFunc("Temp_Dir", []))
```

### 6.4 注意事项

- 直接 COM 方法（如 `Calculate`、`LoadFile`、`Message`、`Report`）不应通过 `CallJsonFunc` 调用，会触发异常或冲突。
- `CallFunc` 与 `CallFuncNParam` 对未知函数名也返回 `None`，但通常不做任何操作，不能作为成功依据。

---

## 7. 接触分析

### 7.1 调用方式

使用 `CallFuncNParam` 调用 `CalculatePathOfContactForPairKS`，需要传入控制文件路径和输出目录路径。

```python
control = r"C:\Program Files\KISSsoft AG\KISSsoft 2024\dat\Example_caControl.dat"
out_dir = r"C:\Users\Full stop\Desktop\kisssoft_ca_out"

ks.GetModule("Z012", False)
ks.LoadFile(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")
ks.Calculate()

ks.CallFuncNParam(['CalculatePathOfContactForPairKS', control, out_dir])
```

### 7.2 输出结果

- 输出文件：`C:\Users\Full stop\Desktop\kisssoft_ca_out\anglereport.txt`
- 文件内容示例：

```text
phi1	phi2	t1z	t2z	csalpha	csbeta	
0.1230181544	-3.14144863	1624.720196	4858.336054	959.1124557	943.4069355	
0.1203726027	-3.140578473	1624.71576	4858.563252	958.3384808	942.6923138	
0.117727051	-3.139708326	1624.677205	4858.710298	957.4567928	941.8759184	
```

### 7.3 注意事项

- `CallJsonFunc` 方式调用 `CalculatePathOfContactForPairKS` 会失败（`-2147352567` 异常）。
- 控制文件 `Example_caControl.dat` 路径和输出目录需要提前存在。
- 接触分析结果文件为制表符分隔文本，可直接用 pandas 或 Excel 读取。

---

## 8. 参数扫描示例

以下示例在 Z012 模块中保持其他输入不变，仅改变齿宽 `ZR[0].b`，每次 `Calculate()` 后读取安全系数的参数扫描。

```python
widths = [40, 42, 44, 46, 48, 50]
for b in widths:
    ks.SetVar("ZR[0].b", str(b))
    ks.Calculate()
    sf = ks.GetVarAsJson("ZPP[0].Fuss.SFnorm")
    sh = ks.GetVarAsJson("ZPP[0].Flanke.SH")
    print(b, sf, sh)
```

### 8.1 扫描结果

| ZR[0].b (mm) | ZPP[0].Fuss.SFnorm | ZPP[0].Flanke.SH | 消息数 |
|-------------|-------------------|------------------|--------|
| 40 | 2.330946773651080 | 1.274282980702781 | 0 |
| 42 | 2.441721023596828 | 1.303971176812722 | 0 |
| 44 | 2.551342605597647 | 1.332842267813122 | 0 |
| 46 | 2.667312724033903 | 1.332842267813122 | 0 |
| 48 | 2.783282842470160 | 1.332842267813122 | 0 |
| 50 | 2.899252960906416 | 1.332842267813122 | 0 |

### 8.2 输入修改对输出影响

| 修改的输入变量 | 输出变量 | 修改前 | 修改后 | 是否变化 |
|---------------|----------|--------|--------|----------|
| `ZR[0].b` | `ZPP[0].Fuss.SFnorm` | 2.551342605597647 | 2.441721023596828 | 是 |
| `ZR[0].b` | `ZPP[0].Flanke.SH` | 1.332842267813122 | 1.303971176812722 | 是 |
| `ZR[0].x.nul` | `ZPP[0].Fuss.SFnorm` | 2.551342605597647 | 2.567150379653703 | 是 |
| `ZR[0].x.nul` | `ZPP[0].Flanke.SH` | 1.332842267813122 | 1.334929010328463 | 是 |
| `ZR[0].x.nul` | `ZR[0].da.nul` | 164.982 | 166.200 | 是 |
| `ZS.Geo.mn` | `ZR[0].da.nul` | 164.982 | 137.659 | 是 |

---

## 9. 报告生成

### 9.1 ReportWithParameters

```python
ks.ReportWithParameters(
    infile=r"C:\Program Files\KISSsoft AG\KISSsoft 2024\rpt\Z012resc.rpt",
    outfile=r"C:\Users\Full stop\Desktop\report.rtf",
    show=0,
    art=0
)
```

### 9.2 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `infile` | `str` | 报告模板 `.rpt` 路径 |
| `outfile` | `str` | 输出文件路径 |
| `show` | `int` | 是否显示报告：`0` 不显示，`1` 显示 |
| `art` | `int` | 报告类型/内容变体：`0`、`1`、`2` 生成不同内容 |

### 9.3 常用报告模板与 art 变体

| 模板 | art | 输出大小（字节） | 说明 |
|------|-----|-----------------|------|
| `Z012resc.rpt` | 0 | 13129 | 紧凑型结果报告 |
| `Z012resc.rpt` | 1 | 14285 | 标准结果报告 |
| `Z012resc.rpt` | 2 | 17650 | 详细结果报告 |
| `Z012resa.rpt` | 0 | 12800 | 紧凑分析报告 |
| `Z012resa.rpt` | 1 | 13956 | 标准分析报告 |
| `Z012resa.rpt` | 2 | 18000 | 详细分析报告 |
| `Z012resi.rpt` | 0 | 12843 | 紧凑输入报告 |
| `Z012resi.rpt` | 1 | 13999 | 标准输入报告 |
| `Z012resi.rpt` | 2 | 18086 | 详细输入报告 |

### 9.4 默认报告方法

```python
ks.Report(0)  # 不显示，生成默认报告
ks.Report(1)  # 显示
```

### 9.5 注意事项

- 返回 `None` 表示生成成功（无异常即成功）。
- 输出文件为 **RTF 格式**，内部嵌有 PNG logo。
- 直接 RTF 转 PDF 可能出现乱码或 logo 问题，建议：
  - 用 Word 打开后另存为 PDF；或
  - 直接用 COM 读取变量，再用 Python 报告库（如 `reportlab`）生成 PDF。
- 通过 `CallJsonFunc("GenerateReport", ...)` 也可以生成报告，但返回的是临时 `.pprpt` 路径。

---

## 10. 文件操作

### 10.1 加载文件

```python
ks.LoadFile(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")
```

### 10.2 从字符串数据加载

```python
with open(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12", 'r') as f:
    data = f.read()
ks.LoadFileData(data)
```

> 注：`LoadFileData` 仅测试了前 2000 字符，返回 `None` 且无异常，具体格式要求未深入探明。

### 10.3 保存文件

```python
ks.SaveFile(r"C:\Users\Full stop\Desktop\test_save.Z12")
```

- 保存后文件大小示例：388846 字节。
- 保存后可用 `GetModulFromFile` / `GetVersionFromFile` / `GetKsoftVersionFromFile` 重新读取文件元数据。

### 10.4 文件元数据查询

```python
print(ks.GetModulFromFile(r"C:\...\01 Spur (ISO 6336).Z12"))      # 'Z012'
print(ks.GetVersionFromFile(r"C:\...\01 Spur (ISO 6336).Z12"))   # '24.0'
print(ks.GetKsoftVersionFromFile(r"C:\...\01 Spur (ISO 6336).Z12")) # '2024' 或 '2024 -SP1'
```

### 10.5 文件操作汇总

| 方法 | 参数 | 说明 |
|------|------|------|
| `LoadFile` | `fileName` | 从磁盘加载 `*.Z*` 文件 |
| `LoadFileData` | `data` | 从字符串/内存数据加载（格式未完全探明） |
| `SaveFile` | `fileName` | 保存当前模型到磁盘 |
| `GetModulFromFile` | `fileName` | 返回文件所属模块 ID |
| `GetVersionFromFile` | `fileName` | 返回文件版本，如 `24.0` |
| `GetKsoftVersionFromFile` | `fileName` | 返回文件保存时 KISSsoft 版本 |

---

## 11. 配置与错误处理

### 11.1 配置方法

```python
ks.SetSilentMode(1)    # 静默模式
ks.SetLanguage(2)      # 设置语言：0/1/2
print(ks.GetLanguage())
ks.SetDebugFile(r"C:\Users\Full stop\Desktop\kisssoft_debug.log")
ks.ShowInterface(0)    # 隐藏 GUI
ks.ShowInterface(1)    # 显示 GUI
```

### 11.2 错误处理示例

```python
# 无效模块
ks.GetModule("INVALID", False)
print(ks.IsModuleValid())  # True（注意：即使模块 ID 无效，IsModuleValid 仍可能为 True）

# 无效文件
ks.LoadFile(r"C:\nonexistent.Z12")  # 返回 None，不抛异常

# 无效变量
result = ks.GetVarAsJson("INVALID.VAR.NAME")
# {"status_code": "not_found", "status_msg": "Coult not find requested variable"}

result = ks.GetVarAsJson("")
# {"status_code": "not_found", "status_msg": "Coult not find requested variable"}
```

### 11.3 配置与错误处理汇总

| 方法 | 示例 | 说明 |
|------|------|------|
| `SetSilentMode(silent)` | `SetSilentMode(1)` | 开启静默模式，避免弹窗 |
| `SetLanguage(index)` | `SetLanguage(2)` | 设置界面/报告语言 |
| `GetLanguage()` | 返回 `0/1/2` | 当前语言 |
| `SetDebugFile(fileName)` | 设置日志路径 | 输出调试日志 |
| `ShowInterface(wait)` | `ShowInterface(0/1)` | 显示/隐藏 GUI，`wait` 含义未明确 |
| `CheckLicense(name)` | `CheckLicense('Z012')` | 返回 `True/False` |
| `GetVarAsJson` 错误 | `status_code: not_found` | 变量不存在或路径错误 |

### 11.4 回调限制

```python
ks.SetCallback('test', callback)
# TypeError: The Python instance can not be converted to a COM object
```

当前 COM 接口无法直接传入 Python 回调函数，如需事件处理，需通过其他机制（如轮询文件、日志）实现。

### 11.5 Message 方法

```python
result = ks.Message('Test message', 0, 1)
# 返回：(('Corrupt file!',), (3,), 1)
```

`Message` 的实际行为未完全探明，调用时传入的字符串可能被覆盖为系统内部消息。

---

## 12. 已知限制与未探明项

### 12.1 数据库方法返回空

`GetDBName` 与 `GetDBValue` 在多种参数组合下均返回空字符串：

```python
ks.GetDBName('mat', 'Material', 0, 1, 0)   # -> ''
ks.GetDBValue('mat', 'Material', 1, 'Name') # -> ''
ks.GetDBValue('mat', 'Material', 1, 'ID')   # -> ''
```

可能原因：参数含义未探明，或当前 license 未开放数据库接口。

### 12.2 CallFunc / CallFuncNParam / CallJsonFunc 限制

- `CallFunc('calculate')`、`CallFunc('Calculate')`、`CallFunc('roughSizing')` 均返回 `None`，未确认实际生效。
- `CallFuncNParam(['Calculate'])`、`CallFuncNParam(['roughSizing'])` 同样返回 `None`。
- `CallJsonFunc` 对未注册函数返回 `{"status_code":"not_implemented","status_msg":"The call function was not found"}`，或抛出异常。

### 12.3 非齿轮模块未授权

除 `Z011` ~ `Z016` 外，其余模块（`Z017`、`Z050`+、`W*`、`S020`、`M*`、`F*`、`A*`、`K*` 等）加载后 `IsModuleValid()` 为 `False`，`CalculateRetVal()` 为 `False`，无法实际计算。

### 12.4 变量读写限制

- `SetVar` 只能写入非只读变量；例如 `ZR[0].b` 可写，`ZR[0].x` 写入后读取仍为空。
- `GetVar` 返回字符串，数值末尾可能有大量浮点尾数；`GetVarAsJson` 更稳定。
- 某些变量在未执行 `Calculate()` 前可能为空或无效。

### 12.5 文件路径与编码

- Windows 路径含空格，需使用原始字符串或双反斜杠。
- 默认输出报告为 RTF，直接转 PDF 可能存在问题。

### 12.6 其他未确认项

- `ShowInterface(wait)` 参数 `wait` 的确切含义未明确。
- `GetModuleOEM` 的 `OEMcode` 用法未测试。
- `LoadFileData` 的完整字符串格式未测试。
- 接触分析控制文件 `caControl.dat` 的自定义参数未探明。
- 尺寸设计函数（`roughSizing`、`fineSizing`）未实际改变几何变量。

---

## 13. 快速参考代码

```python
import win32com.client

ks = win32com.client.Dispatch("KISSsoftCOM2024.KISSsoft")

ks.GetModule("Z012", False)
ks.LoadFile(r"C:\Program Files\KISSsoft AG\KISSsoft 2024\example\01 Spur (ISO 6336).Z12")

ks.SetVar("ZR[0].b", "45")
ks.Calculate()

print(ks.GetVarAsJson("ZPP[0].Fuss.SFnorm"))
print(ks.GetVarAsJson("ZPP[0].Flanke.SH"))
print(ks.GetVarAsJson("ZR[0].z"))
print(ks.GetVarAsJson("ZS.Geo.mn"))

ks.ReportWithParameters(
    r"C:\Program Files\KISSsoft AG\KISSsoft 2024\rpt\Z012resc.rpt",
    r"C:\Users\Full stop\Desktop\report.rtf",
    0, 0
)

ks.ReleaseModule()
```

---

## 14. 参考来源

- `kisssoft_com_reference.md` — 原始主参考文档
- `kisssoft_z01_scan.md` — Z011/Z012 变量扫描
- `kisssoft_z02_scan.md` — Z013/Z014 变量扫描
- `kisssoft_z03_scan.md` — Z015/Z016 变量 + Skript 函数扫描
- `kisssoft_functions_scan.md` — CallJsonFunc / CallFunc 函数扫描
- `kisssoft_advanced_scan.md` — 接触分析、参数扫描、多模块切换
- `kisssoft_io_config_scan.md` — 文件/报告/配置/错误处理
- `kisssoft_com_api_reference.md` — KISSsoftCOM2024 类型库方法清单
- `kisssoft_com_variables_inventory_v3.md` — 从 `.rpt` 模板提取的变量路径（约 1.5 万条）
- `kisssoft_com_variables_inventory_refined.md` — 精简变量与 `.skript` 函数清单
