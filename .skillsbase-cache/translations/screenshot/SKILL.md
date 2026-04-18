---
name: "screenshot"
description: "当用户明确要求截取桌面或系统截图（全屏、特定应用或窗口、或像素区域），或当工具特定的捕获功能不可用且需要操作系统级别的截图时使用。"
---

# 截图捕获

每次遵循以下保存位置规则：

1) 如果用户指定了路径，则保存到该路径。
2) 如果用户要求截图但未指定路径，则保存到操作系统默认的截图位置。
3) 如果 Codex 需要截图用于自身检查，则保存到临时目录。

## 工具优先级

- 优先使用工具特定的截图功能（例如：用于 Figma 文件的 Figma MCP/技能，或用于浏览器和 Electron 应用的 Playwright/agent-browser 工具）。
- 当明确要求、需要全系统桌面捕获，或当工具特定的捕获无法满足需求时，使用此技能。
- 否则，将此技能视为没有更好集成捕获工具的桌面应用的默认选择。

## macOS 权限预检（减少重复提示）

在 macOS 上，进行窗口/应用捕获前运行一次预检助手。它会检查
屏幕录制权限，解释为何需要该权限，并在一处请求权限。

助手将 Swift 的模块缓存路由到 `$TMPDIR/codex-swift-module-cache`
以避免额外的沙盒模块缓存提示。

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh
```

为避免多个沙盒批准提示，尽可能将预检和捕获合并到一个命令中：

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

对于 Codex 检查运行，将输出保留在临时目录：

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

使用捆绑的脚本以避免重新推导操作系统特定的命令。

## macOS 和 Linux（Python 助手）

从仓库根目录运行助手：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

常见模式：

- 默认位置（用户要求“截图”）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

- 临时位置（Codex 视觉检查）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp
```

- 明确位置（用户提供了路径或文件名）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png
```

- 按应用名称捕获应用/窗口（仅限 macOS；支持子字符串匹配；捕获所有匹配的窗口）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

- 应用内的特定窗口标题（仅限 macOS）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex" --window-name "Settings"
```

- 捕获前列出匹配的窗口 ID（仅限 macOS）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --list-windows --app "Codex"
```

- 像素区域（x,y,w,h）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600
```

- 聚焦/活动窗口（仅捕获最前端的窗口；使用 `--app` 捕获所有窗口）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window
```

- 特定窗口 ID（在 macOS 上使用 --list-windows 来发现 ID）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --window-id 12345
```

脚本为每次捕获打印一个路径。当多个窗口或显示器匹配时，它会打印多个路径（每行一个），并添加后缀如 `-w<windowId>` 或 `-d<display>`。按顺序使用图像查看器工具查看每个路径，仅在需要或要求时操作图像。

### 工作流示例

- “查看 <App> 并告诉我你看到了什么”：捕获到临时目录，然后按顺序查看每个打印的路径。

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

- “Figma 的设计与实现不匹配”：首先使用 Figma MCP/技能捕获设计，然后使用此技能捕获运行中的应用（通常到临时目录），并在任何操作之前比较原始截图。

### 多显示器行为

- 在 macOS 上，全屏截图在连接多个显示器时会为每个显示器保存一个文件。
- 在 Linux 和 Windows 上，全屏截图使用虚拟桌面（所有显示器在一个图像中）；需要时使用 `--region` 来隔离单个显示器。

### Linux 先决条件和选择逻辑

助手自动选择第一个可用的工具：

1) `scrot`
2) `gnome-screenshot`
3) ImageMagick `import`

如果都不可用，请用户安装其中之一并重试。

坐标区域需要 `scrot` 或 ImageMagick `import`。

`--app`、`--window-name` 和 `--list-windows` 仅限 macOS。在 Linux 上，使用
`--active-window` 或在可用时提供 `--window-id`。

## Windows（PowerShell 助手）

运行 PowerShell 助手：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

常见模式：

- 默认位置：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

- 临时位置（Codex 视觉检查）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp
```

- 明确路径：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Path "C:\Temp\screen.png"
```

- 像素区域（x,y,w,h）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -Region 100,200,800,600
```

- 活动窗口（请用户先聚焦它）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -ActiveWindow
```

- 特定窗口句柄（仅在提供时）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -WindowHandle 123456
```

## 直接操作系统命令（备用方案）

当无法运行助手时使用这些命令。

### macOS

- 全屏到特定路径：

```bash
screencapture -x output/screen.png
```

- 像素区域：

```bash
screencapture -x -R100,200,800,600 output/region.png
```

- 特定窗口 ID：

```bash
screencapture -x -l12345 output/window.png
```

- 交互式选择或窗口拾取：

```bash
screencapture -x -i output/interactive.png
```

### Linux

- 全屏：

```bash
scrot output/screen.png
```

```bash
gnome-screenshot -f output/screen.png
```

```bash
import -window root output/screen.png
```

- 像素区域：

```bash
scrot -a 100,200,800,600 output/region.png
```

```bash
import -window root -crop 800x600+100+200 output/region.png
```

- 活动窗口：

```bash
scrot -u output/window.png
```

```bash
gnome-screenshot -w -f output/window.png
```

## 错误处理

- 在 macOS 上，首先运行 `bash <path-to-skill>/scripts/ensure_macos_permissions.sh` 以在一处请求屏幕录制权限。
- 如果在沙盒运行中看到“屏幕捕获检查在沙盒中被阻止”、“无法从显示器创建图像”或 Swift `ModuleCache` 权限错误，请使用提升的权限重新运行命令。
- 如果 macOS 应用/窗口捕获没有匹配项，运行 `--list-windows --app "AppName"` 并使用 `--window-id` 重试，并确保应用在屏幕上可见。
- 如果 Linux 区域/窗口捕获失败，使用 `command -v scrot`、`command -v gnome-screenshot` 和 `command -v import` 检查工具可用性。
- 如果保存到操作系统默认位置因沙盒中的权限错误而失败，请使用提升的权限重新运行命令。
- 始终在响应中报告保存的文件路径。