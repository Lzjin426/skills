---
name: weekly-summary
description: 当用户要求"周总结""本周总结""上周总结""整理周报"等任务时使用。本技能从飞书云空间扫描每日 docx 文档，参考历史周报做交叉比对，生成新的周总结并写回飞书 weekly 文件夹。
---

# Weekly Summary

数据源为飞书云空间：日报在 `daily/`、周报在 `weekly/`、月报在 `monthly/`，均为 docx 文档。folder token 集中在 `../summary-shared/lark_folders.json`，禁止硬编码到其他地方。文件命名规则（日报 `M.D-YY`、周报 `M.DD～M.DD-YY`、月报 `M月-YY`、跨年匹配）已全部编码在两个脚本里，不要手动拼接文件名。

## 工作流

1. **定区间**

```bash
python scripts/week_window.py --which current   # 本周（周一~周日）
python scripts/week_window.py --which last      # 上周
python scripts/week_window.py --which explicit --start 2026-01-19 --end 2026-01-25
python scripts/week_window.py --which title --title '1.19～1.25-26'
```

2. **收集飞书文件清单**

```bash
python scripts/collect_lark_notes.py --start <YYYY-MM-DD> --end <YYYY-MM-DD>
```

返回本周命中的日报（`matched_daily_files`）、缺失日期（`missing_dates`）、目标周报文件名与是否已存在、历史上下文（最近 8 篇周报 + 2 篇月报）。

3. **读历史，重点是上一周**

- 用 `lark-cli docs +fetch --doc <url> --doc-format markdown` 读取，正文在返回 JSON 的 `data.document.content` 字段。
- 精读最近 1~2 篇周报，其余扫关键章节即可。目的不是学文风，而是找对比素材：上周「未闭合」的 checkbox 哪些动了哪些没动、精力方向的变化、反复出现的问题。
- **完整保留上一期周报的原文**，后面写作和批评环节都要用它做"重复检测"。

4. **读日报**

逐篇 fetch `matched_daily_files`。缺失日期只记录，不补写、不猜测、不从相邻日期推断。

5. **写作**

遵循 `references/writing-guide.md`。核心立场：**内容决定结构，事实只来自日报，写长了先删。**

6. **批评一遍再发**

把草稿、上一期周报原文、writing-guide 一起交给 subagent（Task 工具）挑刺：与上期结构和句式是否撞车、是否有日报里没有的事实、是否啰嗦。按批评意见改完才进入下一步。不要自我批评了事。

7. **写回飞书**

在临时目录生成 `<weekly_output_basename>.md`（`# 精力分布` 章节正文留空，画板后处理写入）：

```bash
WORKDIR=$(mktemp -d)
# 写 <basename>.md 和 pie.mmd（精力分布的 mermaid pie，3~5 个主题）到 $WORKDIR
```

- 若 `weekly_output_exists` 为 true，**未经用户允许不覆盖**，改用 `<basename>_v2` 并在最终回复里说明。

```bash
# 1) 导入为 docx，记下返回的 data.url 作为 DOC_URL
lark-cli drive +import --type docx \
  --file "$WORKDIR/<basename>.md" \
  --folder-token <weekly_folder_token> \
  --name <output_basename>

# 2) 在「# 精力分布」章节后插入空白画板，记下 data.board_tokens[0]
lark-cli docs +update \
  --doc <DOC_URL> \
  --mode insert_after \
  --selection-by-title "# 精力分布" \
  --markdown '<whiteboard type="blank"></whiteboard>'

# 3) 把 pie.mmd 写入画板
lark-cli whiteboard +update \
  --whiteboard-token <board_token> \
  --input_format mermaid \
  --source @"$WORKDIR/pie.mmd" \
  --idempotent-token "wb-pie-$(date +%s)" \
  --overwrite --yes --as user
```

- 若步骤 2 因标题定位失败，先 `docs +fetch --doc <DOC_URL>` 确认章节结构，再用 block id 定位重试。
- 若当周不用画板（见 writing-guide），跳过步骤 2、3。

8. **汇报**

返回周报 URL、纳入的日报日期范围、缺失日期、画板 token（若有）、是否发生了 `_v2` 规避。

## 其他

- 检索与写入保持在同一自然周内；跨年周脚本自动处理，无需特殊操作。
- 调用 `lark-cli` 前确保已登录；`permission denied` 时提示用户检查身份。

## 资源

- `scripts/week_window.py`：解析周区间。
- `scripts/collect_lark_notes.py`：扫描飞书文件夹，返回日报命中、目标文件名、历史上下文。
- `references/writing-guide.md`：写作指南（风格、结构、语言）。
- `lark-whiteboard` skill：画板写入路径。
- `../summary-shared/lark_folders.json`：共享 folder token 配置。
