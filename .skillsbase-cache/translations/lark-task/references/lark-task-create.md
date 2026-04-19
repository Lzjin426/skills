# task +create

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

在 Lark 中创建一个新任务。

## 推荐命令

```bash
# 创建包含所有详细信息的任务
lark-cli task +create \
  --summary "季度销售回顾" \
  --description "回顾上个季度的销售表现。" \
  --assignee "ou_xxx" \
  --due "2026-03-25" \
  --tasklist-id "https://applink.larkoffice.com/client/todo/task_list?guid=a4b00000-000-000-000-00000000036c"

# 创建一个简单的任务
lark-cli task +create \
  --summary "买牛奶"

# 预览 API 调用而不实际执行
lark-cli task +create --summary "测试任务" --dry-run
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--summary <text>` | 是 | 任务的标题或摘要 |
| `--description <text>` | 否 | 任务的详细描述 |
| `--assignee <id>` | 否 | 要分配任务的用户的 `open_id`（例如 `ou_xxx`） |
| `--due <time>` | 否 | 截止日期。支持 ISO 8601 格式、`YYYY-MM-DD`、相对时间（例如 `+2d`）或毫秒时间戳。`YYYY-MM-DD` 和相对时间将自动设置为全天任务。 |
| `--tasklist-id <id>` | 否 | 任务列表的 GUID，或完整的 AppLink URL（CLI 会自动从 URL 中提取 `guid` 参数）。 |
| `--idempotency-key <key>` | 否 | 客户端令牌，用于确保请求的幂等性。 |
| `--dry-run` | 否 | 预览 API 调用（JSON 负载）而不实际创建任务。 |

## 工作流程

1.  与用户确认：任务摘要、截止日期、负责人和任务列表（如果需要）。
    -   **关于负责人的关键规则**：如果用户明确或暗示说“给我创建一个任务”或“帮我新建/创建一个任务”，你**必须**将任务分配给当前登录的用户。你可以通过执行 `lark-cli auth status`（它默认已输出 JSON，因此不要添加 `--json`）或先执行 `lark-cli contact +get-user` 来获取当前用户的 `open_id`，提取 `userOpenId` 或 `open_id`，然后将其传递给 `--assignee` 参数。
2.  执行 `lark-cli task +create --summary "..." ...`
3.  报告结果：任务 ID 和摘要。

> [!CAUTION]
> 这是一个**写操作** —— 在执行前必须确认用户的意图。

## 参考

- [lark-task](../SKILL.md) -- 所有任务命令
- [lark-shared](../../lark-shared/SKILL.md) -- 身份验证和全局参数