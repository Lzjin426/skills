# task +tasklist-members

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

管理任务清单成员（编辑者/所有者）。

## 推荐命令

```bash
# 添加成员
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --add "ou_aaa"

# 移除成员
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --remove "ou_aaa"

# 精确替换所有成员
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --set "ou_aaa,ou_bbb"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--tasklist-id <id>` | 是 | 任务清单的 GUID，或完整的 AppLink URL。 |
| `--add <ids>` | 否 | 要添加为成员的用户的 `open_id` 列表，以逗号分隔。 |
| `--remove <ids>` | 否 | 要从成员中移除的用户的 `open_id` 列表，以逗号分隔。 |
| `--set <ids>` | 否 | 要精确设置为成员的用户的 `open_id` 列表，以逗号分隔（将替换所有现有成员）。 |

## 工作流程

1.  确认任务清单以及要添加/移除/设置的成员。
2.  执行命令。
3.  报告成功。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户意图。