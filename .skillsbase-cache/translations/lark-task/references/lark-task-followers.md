# task +followers

> **前提条件：** 请先阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

管理任务关注者。为现有任务添加或移除关注者。

## 推荐命令

```bash
# 添加关注者
lark-cli task +followers --task-id "<task_guid>" --add "ou_aaa"

# 移除关注者
lark-cli task +followers --task-id "<task_guid>" --remove "ou_aaa"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--task-id <guid>` | 是 | 要修改的任务 GUID。对于飞书任务应用链接，请使用 `guid` 查询参数，而不是 `suite_entity_num` / 显示的任务 ID（如 `t104121`）。 |
| `--add <ids>` | 否 | 要添加为关注者的用户 `open_id` 列表，以逗号分隔。 |
| `--remove <ids>` | 否 | 要从关注者中移除的用户 `open_id` 列表，以逗号分隔。 |

## 工作流程

1.  确认任务及要添加/移除的关注者。
2.  执行命令。
3.  报告成功。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户的意图。