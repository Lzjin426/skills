# PptxGenJS 辅助工具

## 何时阅读本文档

当你需要查看辅助 API 的详细信息、捆绑 Python 脚本的命令示例，或进行幻灯片生成任务时的依赖说明时，请阅读本文档。

## 辅助模块

- `autoFontSize(textOrRuns, fontFace, opts)`：为固定框选取合适的字体大小。
- `calcTextBox(fontSizePt, opts)`：根据字体大小和内容估算文本框的几何尺寸。
- `calcTextBoxHeightSimple(fontSizePt, numLines, leading?, padding?)`：快速估算文本高度。
- `imageSizingCrop(pathOrData, x, y, w, h)`：将图像居中裁剪至目标框内。
- `imageSizingContain(pathOrData, x, y, w, h)`：将图像完整适配到目标框内。
- `svgToDataUri(svgString)`：将 SVG 字符串转换为可嵌入的数据 URI。
- `latexToSvgDataUri(texString)`：将 LaTeX 渲染为 SVG，以获得清晰的公式。
- `getImageDimensions(pathOrData)`：读取图像的宽度、高度、类型和宽高比。
- `safeOuterShadow(...)`：为 PowerPoint 输出构建安全的外阴影配置。
- `codeToRuns(source, language)`：将源代码转换为富文本片段，供 `addText` 使用。
- `warnIfSlideHasOverlaps(slide, pptx)`：发出重叠警告，用于诊断。
- `warnIfSlideElementsOutOfBounds(slide, pptx)`：发出边界警告，用于诊断。
- `alignSlideElements(slide, indices, alignment)`：精确对齐选定的元素。
- `distributeSlideElements(slide, indices, direction)`：均匀分布选定的元素。

## 依赖说明

JavaScript 辅助工具在使用相应功能时需依赖以下包：

- 核心创作：`pptxgenjs`
- 文本测量：`skia-canvas`、`linebreak`、`fontkit`
- 语法高亮：`prismjs`
- LaTeX 渲染：`mathjax-full`

Python 脚本需依赖以下包：

- `Pillow`
- `pdf2image`
- `python-pptx`
- `numpy`

Python 脚本使用的系统工具：

- `soffice` / LibreOffice：用于 PPTX 到 PDF 的转换
- Poppler 工具：供 `pdf2image` 使用的 PDF 尺寸/光栅支持
- `fc-list`：用于字体检查
- 可选的光栅化工具（用于 `ensure_raster_image.py`）：Inkscape、ImageMagick、Ghostscript、`heif-convert`、`JxrDecApp`

## 脚本说明

- `render_slides.py`：将演示文稿转换为 PNG 图像。适用于视觉审查和差异对比。
- `slides_test.py`：在原始画布外添加灰色边框，渲染并检查是否有内容溢出到边框内。
- `create_montage.py`：将多个渲染的幻灯片图像合并为一张概览图。
- `detect_font.py`：区分完全缺失的字体与已安装但在渲染时被替换的字体。
- `ensure_raster_image.py`：从常见的矢量或特殊的光栅格式生成 PNG，以便轻松检查或放置资源。

## 实用规则

- 除非源材料另有说明，否则默认使用 `LAYOUT_WIDE`。
- 在测量文本之前，明确设置字体族。
- 对于可能扩展的内容框，使用 `valign: "top"`。
- 当图表简单且后续可能编辑时，优先使用原生 PowerPoint 图表而非渲染的图像。
- 尽可能使用 SVG 而非 PNG 来制作图表。