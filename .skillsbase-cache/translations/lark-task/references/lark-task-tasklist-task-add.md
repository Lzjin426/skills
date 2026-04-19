# task +tasklist-task-add

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

将现有任务添加到任务清单。

## 推荐命令

```bash
# 将单个任务添加到任务清单
lark-cli task +tasklist-task-add --tasklist-id "<tasklist_guid>" --task-id "<task_guid>"

# 将多个任务添加到任务清单
lark-cli task +tasklist-task-add --tasklist-id "<tasklist_guid>" --task-id "<task_guid>,<another_task_guid>,<third_task_guid>"

# 将任务添加到任务清单的特定分区
lark-cli task +tasklist-task-add \
  --tasklist-id "<tasklist_guid>" \
  --task-id "<task_guid>" \
  --section-guid "<section_guid>"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--tasklist-id <guid>` | 是 | 任务清单的 GUID，或完整的 AppLink URL。 |
| `--task-id <guids>` | 是 | 要添加到任务清单的任务 GUID 列表，以逗号分隔。对于飞书任务 AppLink，请使用每个任务的 `guid` 查询参数，而不是 `suite_entity_num` / 显示任务 ID（如 `t104121`）。 |
| `--section-guid <guid>` | 否 | 要将任务添加到的自定义分区的 GUID。如果省略，任务将被添加到默认分区。 |

## 工作流程

1. 确认任务清单和要添加的任务。
2. 执行命令 `lark-cli task +tasklist-task-add ...`。
3. 报告结果（成功与失败的任务）。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户意图。