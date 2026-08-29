---
name: apinebula-nanobanana
description: "通过 APINebula Nano Banana 图像接口使用 gemini-3.1-flash-image 生成图片。用户要求使用 Nano Banana、Gemini image、APINebula 文生图，或明确调用 $apinebula-nanobanana 时使用。"
---

# APINebula Nano Banana

使用 APINebula 的 Nano Banana 接口生成单张图片。固定模型为 `gemini-3.1-flash-image`，不切换到其他模型或其他生图服务。

## 调用

```bash
python3 /Users/fullstop/.agents/skills/apinebula-nanobanana/scripts/generate.py \
  --prompt "your image prompt" \
  --output /absolute/path/to/image.png \
  --aspect-ratio 16:9 \
  --image-size 2K
```

也可以用 `--prompt-file` 传入 UTF-8 提示词文件。脚本会调用：

`https://img-api.apinebula.ai/v1beta/models/gemini-3.1-flash-image:generateContent`

请求使用 Gemini 内容生成格式，`responseModalities` 固定为 `IMAGE`，返回的 inline Base64 图片会保存到 `--output`。

## 密钥

脚本优先读取环境变量 `APINEBULA_API_KEY`，未设置时读取本 skill 目录下的私有 `.api_key`。`.api_key` 必须保持 `600` 权限，不要打印、提交或写入提示词和输出清单。

## 参数

- `--prompt` 或 `--prompt-file`：二选一，必填。
- `--output`：输出图片路径，默认 `nanobanana-image.png`。
- `--aspect-ratio`：支持 `1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`3:2`、`2:3`、`21:9` 等常用比例。
- `--image-size`：`1K`、`2K` 或 `4K`。
- `--timeout`：单次请求超时秒数，默认 180。
- `--dry-run`：只打印不含密钥的 JSON 请求体，不调用服务。

生图提示词由调用方提供；本 skill 只负责 Nano Banana 请求、Base64 解码和文件保存。
