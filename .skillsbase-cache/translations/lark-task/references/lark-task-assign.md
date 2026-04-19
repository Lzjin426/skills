# task +assign

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

为任务分配或移除成员（负责人）。

## 推荐命令

```bash
# 添加负责人
lark-cli task +assign --task-id "<task_guid>" --add "ou_aaa"

# 转移负责人（移除旧的，添加新的）
lark-cli task +assign --task-id "<task_guid>" --remove "ou_old" --add "ou_new"

# 添加多个负责人
lark-cli task +assign --task-id "<task_guid>" --add "ou_aaa,ou_bbb"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--task-id <guid>` | 是 | 要修改的任务 GUID。对于飞书任务应用链接，请使用 `guid` 查询参数，而不是 `suite_entity_num` / 显示的任务 ID（如 `t104121`）。 |
| `--add <ids>` | 否 | 要添加为负责人的用户 `open_id` 列表，以逗号分隔。 |
| `--remove <ids>` | 否 | 要从负责人中移除的用户 `open_id` 列表，以逗号分隔。 |

## 工作流程

1.  确认任务以及要添加/移除的成员。
2.  执行命令。
3.  报告操作成功以及新的负责人数量。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户的意图。