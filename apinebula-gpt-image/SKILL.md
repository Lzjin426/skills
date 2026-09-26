---
name: apinebula-gpt-image
description: "通过 APINebula 的 gpt-image-2 异步任务接口生成或批量并发生成图片，并下载到本地。用户要求用 APINebula、gpt-image-2、异步图片任务、一次生成多张图片、并发出图或下载出图结果时使用。"
---

# APINebula GPT Image

使用 APINebula 异步图片任务接口生成 `gpt-image-2` 图片。接口每个任务只返回一张；用脚本并发提交多个任务实现批量出图。

## 生成图片

1. 优先读取当前进程环境的 `APINEBULA_API_KEY`；未设置时读取技能目录的私有 `.api_key` 文件。不得把密钥写进脚本、命令历史、`SKILL.md` 或输出清单。
2. 先确认用户的提示词、张数和质量；每个任务都可能产生费用。未明确张数时默认生成 1 张。
3. 运行脚本。推荐把输出目录设为用户指定的项目目录：

```bash
python3 /Users/fullstop/.agents/skills/apinebula-gpt-image/scripts/generate_images.py \
  --prompt "一只猫坐在赛博朋克风格的窗边" \
  --count 4 \
  --concurrency 4 \
  --quality high \
  --output-dir /absolute/path/to/output
```

脚本会并发执行以下流程：

- `POST https://apinebula.ai/v1/image-tasks/generations`，每张图提交一个 `gpt-image-2` 异步任务；
- 轮询 `GET /v1/image-tasks/{task_id}?detail=true`，直到任务完成、失败、取消或超时；
- 从 `detail.data[].download_url` 下载完成图片，并在输出目录写入不含密钥的 `manifest.json`。

## 参数

- `--count`：生成张数，默认 `1`。
- `--concurrency`：同时提交、查询和下载的最大数量，默认 `3`，不得大于 `--count`。
- `--quality`：`low`、`medium`、`high` 或 `auto`，默认 `medium`。
- `--timeout`：从提交后等待所有任务完成的总秒数，默认 `600`。
- `--poll-interval`：轮询间隔秒数，默认 `3`。
- `--output-dir`：下载目录；未传入时创建当前目录下的带时间戳 `apinebula-images-*` 文件夹。

`n` 不是此接口的批量参数，保持每个任务单图。任务最终失败或取消时，服务商文档说明会退回预扣额度；脚本会保留成功图片并以非零状态退出。

## 编辑图片

该脚本目前只支持文生图。用户需要参考图编辑时，使用同一异步体系的 `POST /v1/image-tasks/edits`，并在实现前核对文档的 JSON 请求格式与图片输入字段；不要把同步 `/v1/images/edits` 接口混用进来。
