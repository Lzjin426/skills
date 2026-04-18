---
name: slides
description: 使用 PptxGenJS 创建和编辑演示文稿幻灯片文件（`.pptx`），包含捆绑的布局辅助工具以及渲染/验证工具。适用于以下任务：构建新的 PowerPoint 演示文稿、根据截图/PDF/参考文稿重新创建幻灯片、修改幻灯片内容并保持输出可编辑、添加图表/图示/可视化元素，或诊断布局问题（如内容溢出、元素重叠和字体替换）。
---

# 幻灯片

## 概述

使用 PptxGenJS 进行幻灯片创作。除非任务仅涉及检查，否则不要使用 `python-pptx` 生成文稿；在 JavaScript 中保持输出可编辑，并同时交付 `.pptx` 文件和源代码 `.js`。

将工作保存在任务本地目录中。仅在渲染和验证通过后，将最终产物复制到请求的目标位置。

## 捆绑资源

- `assets/pptxgenjs_helpers/`：将此文件夹复制到文稿工作区，并本地导入，而不是重新实现辅助逻辑。
- `scripts/render_slides.py`：将 `.pptx` 或 `.pdf` 栅格化为每页 PNG 图片。
- `scripts/slides_test.py`：检测超出幻灯片画布的内容。
- `scripts/create_montage.py`：构建渲染幻灯片的联系表风格拼图。
- `scripts/detect_font.py`：报告 LibreOffice 解析时缺失或被替换的字体。
- `scripts/ensure_raster_image.py`：将 SVG/EMF/HEIC/PDF 类资源转换为 PNG 以便快速检查。
- `references/pptxgenjs-helpers.md`：仅在需要 API 详情或依赖说明时加载。

## 工作流程

1. 检查请求，确定是创建新文稿、重新创建现有文稿还是编辑现有文稿。
2. 预先设置幻灯片尺寸。除非源材料明确使用其他宽高比，否则默认使用 16:9（`LAYOUT_WIDE`）。
3. 将 `assets/pptxgenjs_helpers/` 复制到工作目录，并从该处导入辅助工具。
4. 使用 JavaScript 构建文稿，明确设置主题字体、稳定间距，并在可行时使用可编辑的 PowerPoint 原生元素。
5. 从本技能目录运行捆绑脚本，或将所需脚本复制到任务工作区。使用 `render_slides.py` 渲染结果，查看 PNG 图片，并在交付前修复布局问题。
6. 当幻灯片边缘紧凑或文稿内容密集时，运行 `slides_test.py` 进行溢出检查。
7. 交付 `.pptx` 文件、创作用的 `.js` 文件以及任何重新构建文稿所需的生成资源。

## 创作规则

- 明确设置主题字体。如果排版重要，不要依赖 PowerPoint 默认设置。
- 使用 `autoFontSize`、`calcTextBox` 及相关辅助工具来调整文本框大小；不要使用 PptxGenJS 的 `fit` 或 `autoFit`。
- 使用项目符号选项，而非字面字符 `•`。
- 使用 `imageSizingCrop` 或 `imageSizingContain`，而非 PptxGenJS 内置的图像尺寸调整。
- 使用 `latexToSvgDataUri()` 处理公式，使用 `codeToRuns()` 处理语法高亮的代码块。
- 对于简单的条形图/折线图/饼图/直方图等可视化内容，优先使用 PowerPoint 原生图表，以便审阅者后续编辑。
- 对于 PptxGenJS 无法良好表达的图表或图示，可在外部渲染 SVG 并将其放入幻灯片。
- 在提交的 JavaScript 代码中，每当生成或大幅编辑幻灯片时，都应包含 `warnIfSlideHasOverlaps(slide, pptx)` 和 `warnIfSlideElementsOutOfBounds(slide, pptx)`。
- 在交付前修复所有非预期的重叠和越界警告。如果重叠是故意的，请在相关元素附近添加简短代码注释。

## 重新创建或编辑现有幻灯片

- 首先渲染源文稿或参考 PDF，以便在视觉上比较幻灯片几何结构。
- 在重建布局前匹配原始宽高比。
- 尽可能保持可编辑性：文本应保持为文本，简单图表应保持为原生图表。
- 如果参考幻灯片使用栅格图像，在放置前使用 `ensure_raster_image.py` 从矢量或特殊图像格式生成调试用 PNG。

## 验证命令

以下示例假设已将所需脚本复制到工作目录。否则，请根据本技能文件夹的相对路径调用相同脚本。

```bash
# 将幻灯片渲染为 PNG 以供审阅
python3 scripts/render_slides.py deck.pptx --output_dir rendered

# 构建拼图以便快速浏览
python3 scripts/create_montage.py --input_dir rendered --output_file montage.png

# 检查是否超出原始幻灯片画布
python3 scripts/slides_test.py deck.pptx

# 检测缺失或被替换的字体
python3 scripts/detect_font.py deck.pptx --json
```

如需辅助工具 API 摘要或依赖详情，请加载 `references/pptxgenjs-helpers.md`。