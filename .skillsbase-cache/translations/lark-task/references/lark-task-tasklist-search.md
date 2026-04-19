# task +tasklist-search

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。
>
> **⚠️ 注意：** 此快捷指令使用任务清单搜索，然后通过任务清单详情查询来渲染最终输出。

通过关键词和可选过滤器搜索任务清单。

## 推荐命令

```bash
# 通过关键词搜索
lark-cli task +tasklist-search --query "测试"

# 搜索特定用户创建的任务清单
lark-cli task +tasklist-search --creator "ou_xxx,ou_yyy"

# 按创建时间范围搜索
lark-cli task +tasklist-search --query "Q2" --create-time "-30d,+0d"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--query <string>` | 否 | 搜索关键词。如果省略，则必须提供至少一个过滤器。 |
| `--creator <ids>` | 否 | 创建者的 open_id，以逗号分隔。 |
| `--create-time <range>` | 否 | 创建时间范围，格式为 `起始,结束`。每侧支持 ISO/日期/相对时间/毫秒输入。 |
| `--page-token <string>` | 否 | 用于分页的页面令牌。 |
| `--page-all` | 否 | 自动遍历所有页面（最多 40 页）。 |
| `--page-limit <int>` | 否 | 最大页面限制（默认 20）。 |

## 工作流程

1. 根据用户请求构建搜索关键词和过滤器。
2. 执行 `lark-cli task +tasklist-search ...`
3. 报告匹配的任务清单，如果存在更多结果，则提供下一个 `page_token`。