# 任务 +update

> **前提条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

更新飞书中的现有任务。

## 推荐命令

```bash
# 更新任务摘要
lark-cli task +update --task-id "<task_guid>" --summary "新摘要"

# 更新多个任务的截止日期
lark-cli task +update --task-id "<task_guid>,<another_task_guid>" --due "+2d"

# 使用 JSON 数据更新
lark-cli task +update --task-id "<task_guid>" --data '{"description": "新描述"}'
```

## 参数

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `--task-id <guid>` | 是 | 要更新的任务 GUID。支持逗号分隔的多个任务 GUID。对于飞书任务应用链接，请使用 `guid` 查询参数，而不是 `suite_entity_num` / 显示任务 ID（如 `t104121`）。 |
| `--summary <text>` | 否 | 任务的新摘要/标题。 |
| `--description <text>` | 否 | 任务的新描述。 |
| `--due <time>` | 否 | 新的截止日期（支持相对时间）。 |
| `--data <json>` | 否 | 用于更新字段的 JSON 负载。 |

## 工作流程

1.  向用户确认要更新的任务和字段。
2.  执行 `lark-cli task +update --task-id "..." ...`
3.  报告更新成功。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户的意图。