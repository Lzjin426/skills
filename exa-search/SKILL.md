---
name: exa-search
description: "用 Exa 语义搜索 API(neural search)做英文/技术/论文/代码相关检索。当 agent 需要查英文网页、技术文档、学术论文、GitHub 代码、竞品调研、语义相近内容,以及现有 anysearch 结果不够精准或需要全文提取时使用。执行方式: 运行全局 CLI python3 ~/.agents/tools/exa-search/exa_search.py。API key 已配置在 ~/.agents/tools/exa-search/.env。"
metadata:
  version: "0.1.0"
  docs: "https://exa.ai/docs"
---

# Exa Search CLI

用真实语义搜索(非关键词匹配)检索网页,对英文技术内容、论文、代码、找相似内容能力强。中文本土信息(工商/合规)弱,中文场景优先用 anysearch。

## 用法

```bash
# 基础搜索(默认 type=auto + 每结果带高亮摘要, 输出 Markdown)
python3 ~/.agents/tools/exa-search/exa_search.py "query"

# 指定结果数 / 搜索类型
python3 ~/.agents/tools/exa-search/exa_search.py "query" --max-results 5
python3 ~/.agents/tools/exa-search/exa_search.py "query" --type deep

# 完整 JSON(带元数据)
python3 ~/.agents/tools/exa-search/exa_search.py "query" --json

# 域名过滤 / 新鲜度
python3 ~/.agents/tools/exa-search/exa_search.py "query" --include-domains github.com,arxiv.org
python3 ~/.agents/tools/exa-search/exa_search.py "query" --max-age-hours 168
```

## 参数速查

| 参数 | 说明 |
|---|---|
| `--max-results` | 结果数,默认 API 默认 10 |
| `--type` | `auto`(默认)/`fast`/`instant`/`deep`/`deep-reasoning` |
| `--category` | `company`/`people`/`publication`/`news`(仅明确需要时用) |
| `--json` | 输出完整 JSON |

## 规范(来自官方 build-with-exa skill)

- 默认请求 = query + type:auto + contents.highlights:true,不添加多余参数
- 需要更加最新内容时,用 `startPublishedDate`/`endPublishedDate`,不要用 `maxAgeHours` 当发布时效过滤
- `findSimilar` 已废弃; 找相关页面用 `/search` 后跟 `/contents`
- 列表构建/富人流程走 Agent API,不是普通 search

## 错误处理

- key 未配置: 检查 ~/.agents/tools/exa-search/.env 或 export EXA_API_KEY
- 网络/429: 重试一次,仍失败告知用户配额或网络问题
