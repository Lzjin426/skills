# 任务 +评论

> **前提条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。

为现有任务添加评论。

## 推荐命令

```bash
# 添加评论
lark-cli task +comment --task-id "<task_guid>" --content "看起来不错！"
```

## 参数

| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `--task-id <guid>` | 是 | 要评论的任务 GUID。对于飞书任务应用链接，请使用 `guid` 查询参数，而不是 `suite_entity_num` / 显示的任务 ID（如 `t104121`）。 |
| `--content <text>` | 是 | 评论的文本内容。 |

## 工作流程

1.  确认任务和评论内容。
2.  执行 `lark-cli task +comment --task-id "..." --content "..."`
3.  报告成功和评论 ID。

> [!CAUTION]
> 这是一个 **写入操作** —— 执行前必须确认用户意图。