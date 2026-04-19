# task +search

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。
>
> **⚠️ 注意：** 此 API 必须使用用户身份调用。**请勿使用应用身份，否则调用将失败。**

通过关键词和可选筛选条件搜索任务。

## 推荐命令

```bash
# 按关键词搜索
lark-cli task +search --query "test"

# 搜索分配给特定用户的未完成任务
lark-cli task +search --assignee "ou_xxx,ou_yyy" --completed=false

# 按截止时间范围搜索
lark-cli task +search --query "release" --due "-1d,+7d"
```

## 参数

| 参数 | 必填 | 描述 |
|-----------|----------|-------------|
| `--query <string>` | 否 | 搜索关键词。如果省略，必须提供至少一个筛选条件。 |
| `--creator <ids>` | 否 | 创建者的 open_id，以逗号分隔。 |
| `--assignee <ids>` | 否 | 负责人的 open_id，以逗号分隔。 |
| `--follower <ids>` | 否 | 关注者的 open_id，以逗号分隔。 |
| `--completed=<bool>` | 否 | 按完成状态筛选。 |
| `--due <range>` | 否 | 截止时间范围，格式为 `起始,结束`。每侧支持 ISO/日期/相对时间/毫秒时间戳输入。 |
| `--page-token <string>` | 否 | 用于分页的页面令牌。 |
| `--page-all` | 否 | 自动遍历所有页面（最多 40 页）。 |
| `--page-limit <int>` | 否 | 最大页面限制（默认 20）。 |

## 工作流程

1. 根据用户请求构建关键词和筛选条件。
2. 执行 `lark-cli task +search ...`
3. 报告匹配的任务，如果存在更多结果，则包含下一个 `page_token`。