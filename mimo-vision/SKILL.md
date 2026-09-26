---
name: mimo-vision
description: "通过小米 MiMo V2.5 视觉模型让 DeepSeek 看懂图片。当用户发送图片、对话中出现图片文件/截图/URL、或模型自身无法查看图片内容需要描述时使用；支持多张图片并行调用、一次请求多图一起看，返回详细中文描述供 DeepSeek 使用。"
---

# MiMo Vision — 给 DeepSeek 的第三只眼

DeepSeek 自身无法直接查看图片。遇到任何图片（用户上传、本地路径、URL、截图、图表、界面、文档扫描件）时，用本 skill 调用小米 MiMo V2.5 视觉模型（`mimo-v2.5`）获取尽可能详细的图片描述，再基于描述继续回答。

## 调用方式

```bash
python3 /Users/fullstop/.agents/skills/mimo-vision/scripts/describe_images.py \
  <图片1> [图片2 ...] [选项]
```

图片参数可以是本地路径或 http(s) URL，数量不限。

### 并行调用（默认，推荐多图）

每张图一个独立请求、并发执行，各图独立获得详细描述，互不干扰：

```bash
python3 /Users/fullstop/.agents/skills/mimo-vision/scripts/describe_images.py \
  /path/a.png /path/b.png https://example.com/c.jpg \
  --concurrency 4
```

输出格式：`## 图片 N：<文件名>` + 详细描述。

### 多图一起看（together 模式）

所有图片放进同一个请求，MiMo 一次看完并对比多张图（指出异同、关联、顺序关系）：

```bash
python3 /Users/fullstop/.agents/skills/mimo-vision/scripts/describe_images.py \
  /path/a.png /path/b.png --mode together
```

适合对比、多图叙事、图组整体理解。

## 参数

- `--mode parallel|together`：默认 `parallel`。
- `--prompt "..."`：自定义描述指令。默认提示词要求尽可能详细：整体场景、主体、颜色光线、文字逐字转录、位置关系、氛围细节；截图/图表/界面/文档会完整转述文字与结构。
- `--max-tokens N`：单请求最大输出 token，默认 `4096`。MiMo V2.5 是推理模型，token 预算不足时 content 会为空（报"被截断"错误），遇到该错误就调大此值。
- `--thinking`：开启 MiMo 深度思考模式（更慢、更贵、分析更深）。**默认关闭**——MiMo V2.5 支持 `thinking: {"type": "disabled"}`，关闭后不走推理（`reasoning_tokens=0`），输出 token 减少 90%+、响应更快，日常识图完全够用。
- `--concurrency N`：parallel 模式并发数，默认 `4`。
- `--timeout N`：单请求超时秒数，默认 `180`。

## 使用规范

1. 用户发来图片（附件、路径或 URL）或要求"看/识别/描述这张图"时，直接运行本脚本，无需询问。
2. 多张图默认走 parallel；用户要求"一起看/对比/总结多图"时用 `--mode together`。
3. 把脚本输出的描述完整纳入回答依据；回答时把图片内容当作已"看到"的事实，不需要向用户说明"我调用了视觉模型"。
4. 单图失败不影响其他图（parallel 模式下错误会标注在对应条目上）。若某图报 token 截断错误，用更大的 `--max-tokens` 重试该图。
5. 中文描述默认即可；用户要求英文或其他语言时，用 `--prompt` 指定输出语言。

## 密钥

- 脚本优先读取环境变量 `MIMO_API_KEY`，未设置时读取本 skill 目录私有 `.api_key` 文件（已配置好）。
- 不要把密钥打印、写入输出或提交到任何仓库。`.api_key` 权限保持 `600`。

## API 要点（官方文档 https://mimo.mi.com/docs）

- 端点：`POST https://api.xiaomimimo.com/v1/chat/completions`（OpenAI 兼容，Bearer 或 `api-key` 头认证）。
- 图片理解仅支持 `mimo-v2.5` 模型；图片输入支持公开 URL 与 `data:image/{mime};base64,` 前缀的 Base64，单图 ≤ 50MB。
- 响应为推理模型：`content` 是最终描述，`reasoning_content` 是思考过程，只取 `content`。默认已通过 `thinking: {"type": "disabled"}` 关闭思考，此时响应无 `reasoning_content`。
- 价格（按量付费，2026 年官方定价）：`mimo-v2.5` 输入 ¥1.00/M（缓存命中 ¥0.02/M）、输出 ¥2.00/M。关闭思考后实际花费可降低约 90%（一次识图仅约 ¥0.005）。
