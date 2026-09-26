---
name: md-image-supplement
description: |
  当用户希望把 markdown 报告（如 KISSsoft 校核报告）补充完整，将配套 screenshots/图片目录中的内容 OCR 后合并到 markdown 中时，使用本 skill。
  适用场景包括：报告 markdown 中缺少图表/截图信息、需要把 images/ 目录里的内容追加到 full.md 后生成 full_complete.md、用户提到“补充 md”、“OCR 图片”、“图片里的内容没进 markdown”、“用 agent team 并行处理多个报告”等。
  即使原文件已经存在，只要用户想基于图片再补充一次，也应调用本 skill。
compatibility: |
  需要安装 mineru-open-api CLI（`mineru-open-api flash-extract` 可用）。
  依赖 Python 3 标准库（argparse、subprocess、concurrent.futures、pathlib）。
---

# md-image-supplement

把 markdown 报告及其同级 `images/` 目录中的截图合并，生成包含 OCR 结果的完整 markdown 文件。

## 何时使用

- 用户有一个或多个 markdown 文件（默认文件名 `full.md`），每个文件旁边都有 `images/` 目录。
- 用户指出 markdown 不够完整，图片里还有信息没包含进去。
- 用户要求“OCR 图片补充到 markdown”、“生成完整版报告”、“把截图内容合并进来”。
- 用户明确要求使用 agent team 并行处理多个报告。

## 输出产物

对每一个满足条件的报告目录：

- 保留原文件（例如 `full.md`）不变。
- 生成 `full_complete.md`，内容为原 markdown + “图片补充信息” 章节。
- 章节内按图片文件名分块列出 `mineru-open-api flash-extract` 的 OCR 结果。

## 执行流程

1. **确认输入目录**：如果用户没有给出目标目录，询问“请指定要处理的根目录”。
2. **发现报告目录**：在目标目录下递归查找所有名为 `full.md` 且同级存在 `images/` 目录的文件。
   - 如果用户给出过滤条件（如只处理某个功率等级、某个子目录），通过 `--filter` 传给脚本。
3. **使用 agent team 并行处理**：
   - 如果发现的报告目录数量 ≥ 2，使用 `Agent` 工具分派子代理。
   - 推荐分组方式：每个顶层子目录（如 `4.25/`、`6.25/`、`12.5/KA=1.1-ME/`）一个子代理；若顶层子目录内仍有多个报告级别，可进一步按 `md 文档/第X级` 拆分。
   - 每个子代理执行本 skill 的脚本：
     ```bash
     python3 <skill-path>/scripts/supplement_md_from_images.py <base-dir> [--filter <filter>]
     ```
   - 每个子代理只负责自己的那一部分目录，不要重复处理其他代理的范围。
   - 如果用户明确要求“不要 agent team”或只有一个报告目录，直接本地运行脚本。
4. **等待并汇总**：等所有子代理完成后，列出每个生成的 `full_complete.md` 路径、大小、补充的图片数量。
5. **复核**：检查是否有 `OCR 失败`、`OCR 超时`、`OCR 异常` 等标记。若有，向用户报告。

## 脚本参数说明

 bundled 脚本 `scripts/supplement_md_from_images.py` 支持：

```bash
python3 scripts/supplement_md_from_images.py <base_dir> [--md-name full.md] [--workers 2] [--filter 4.25] [--filter 6.25]
```

- `base_dir`：搜索根目录。
- `--md-name`：要补充的 markdown 文件名，默认 `full.md`。
- `--workers`：每个报告内部并发 OCR 的图片数，默认 2。
- `--filter`：可多次使用，只处理相对路径包含该字符串的报告。

## 边界与注意事项

- 本 skill **不修改原 markdown 文件**，只生成 `*_complete.md`。
- OCR 为纯文本追加，不保证与原文排版完全一致；如果图片 OCR 结果为空，则跳过该图片。
- 若 `mineru-open-api` 命令失败，脚本会在生成的 markdown 中写入错误标记，而不是中断整个流程。
- 使用 agent team 时，确保每个子代理的工作范围互不重叠。

## 示例

**用户输入：**
> “把 /Users/fullstop/reports 下的 KISSsoft 报告补充完整，用 agent team。”

**你的操作：**
1. 发现 `/Users/fullstop/reports` 下有 `4.25/md 文档/第一级/full.md` 等 3 个齿轮箱、共 10 个报告目录。
2. 启动 3 个子代理，分别处理 `4.25/`、`6.25/`、`12.5/KA=1.1-ME/`。
3. 每个子代理运行：
   ```bash
   python3 ~/.agents/skills/md-image-supplement/scripts/supplement_md_from_images.py \
     /Users/fullstop/reports --filter <对应目录>
   ```
4. 汇总生成 10 个 `full_complete.md` 并报告。
