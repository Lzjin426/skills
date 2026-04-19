---
name: "doc"
description: "当任务涉及读取、创建或编辑 `.docx` 文档，尤其是对格式或版式保真度有要求时使用；推荐优先使用 `python-docx` 配合内置的 `scripts/render_docx.py` 进行视觉检查。"
---

# DOCX 技能

## 使用时机
- 读取或审阅 DOCX 内容，且版式很重要（表格、图表、分页）。
- 创建或编辑具有专业格式的 DOCX 文件。
- 在交付前验证视觉版式。

## 工作流程
1. 优先进行视觉审阅（版式、表格、图表）。
   - 如果 `soffice` 和 `pdftoppm` 可用，将 DOCX -> PDF -> PNG 转换。
   - 或使用 `scripts/render_docx.py`（需要 `pdf2image` 和 Poppler）。
   - 如果缺少这些工具，请安装它们或请用户本地审阅渲染后的页面。
2. 使用 `python-docx` 进行编辑和结构化创建（标题、样式、表格、列表）。
3. 每次有意义的更改后，重新渲染并检查页面。
4. 如果无法进行视觉审阅，则使用 `python-docx` 提取文本作为备选方案，并指出版式风险。
5. 保持中间输出有序，并在最终确认后清理。

## 临时文件与输出约定
- 使用 `tmp/docs/` 存放中间文件；完成后删除。
- 在本仓库中工作时，将最终成果写入 `output/doc/` 目录下。
- 保持文件名稳定且具有描述性。

## 依赖项（缺失时安装）
推荐使用 `uv` 进行依赖管理。

Python 包：
```
uv pip install python-docx pdf2image
```
如果 `uv` 不可用：
```
python3 -m pip install python-docx pdf2image
```
系统工具（用于渲染）：
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

如果无法在当前环境中安装，请告知用户缺少哪个依赖项以及如何在本地安装。

## 环境
无需环境变量。

## 渲染命令
DOCX -> PDF：
```
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX
```

PDF -> PNG：
```
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
```

内置辅助脚本：
```
python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

## 质量要求
- 交付客户就绪的文档：一致的排版、间距、边距和清晰的层级结构。
- 避免格式缺陷：文本被裁剪/重叠、表格损坏、字符不可读或默认模板样式。
- 图表、表格和视觉元素在渲染页面中必须清晰可读且对齐正确。
- 仅使用 ASCII 连字符。避免 U+2011（不间断连字符）和其他 Unicode 破折号。
- 引用和参考文献必须人类可读；切勿保留工具标记或占位符字符串。

## 最终检查
- 在最终交付前，重新渲染并以 100% 缩放比例检查每一页。
- 修复任何间距、对齐或分页问题，并重复渲染循环。
- 确认没有残留文件（临时文件、重复渲染），除非用户要求保留。