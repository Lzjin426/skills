# task +set-ancestor

> **前提条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

为任务设置一个父任务，或清除父任务使其独立。

## 推荐命令

```bash
# 设置父任务
lark-cli task +set-ancestor --task-id "guid_1" --ancestor-id "guid_2"

# 清除父任务
lark-cli task +set-ancestor --task-id "guid_1"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--task-id <guid>` | 是 | 要更新的任务 GUID。 |
| `--ancestor-id <guid>` | 否 | 父任务 GUID。省略此参数以清除父任务。 |

## 工作流程

1.  确认子任务，以及（如果适用）父任务。
2.  执行 `lark-cli task +set-ancestor ...`
3.  报告更新后的任务 GUID 以及父任务是已设置还是已清除。

> [!CAUTION]
> 这是一个**写入操作**——执行前必须确认用户意图。