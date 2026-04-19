# task +tasklist-create

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

创建一个新的任务清单，并可选择在其中批量创建任务。

## 推荐命令

```bash
# 创建一个空的任务清单
lark-cli task +tasklist-create --name "Q1 Goals"

# 创建一个任务清单并添加成员
lark-cli task +tasklist-create --name "Project A" --member "ou_xxx,ou_yyy"

# 创建一个任务清单并在其中批量创建任务
lark-cli task +tasklist-create --name "Launch Checklist" --data '[{"summary": "Code Review", "assignee": "ou_aaa"}, {"summary": "Deploy", "assignee": "ou_bbb"}]'
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--name <text>` | 是 | 任务清单的名称。 |
| `--member <ids>` | 否 | 以逗号分隔的用户 `open_id` 列表，将其添加为编辑者。 |
| `--data <json>` | 否 | 任务定义的 JSON 数组，用于自动创建并添加到任务清单中。 |

## 工作流程

1.  确认任务清单名称、成员以及任务（如果有）。
2.  执行命令 `lark-cli task +tasklist-create ...`。
3.  报告成功，包括新的任务清单 ID 和批量任务创建的结果。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户的意图。