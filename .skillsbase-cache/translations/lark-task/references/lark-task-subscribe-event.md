# task +subscribe-event

> **前置条件：** 请阅读 `../lark-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。
>
> **⚠️ 注意：** 此 API 同时支持 `user` 和 `bot` 身份。使用 `user` 可订阅当前用户有权访问的任务；使用 `bot` 可订阅**应用负责的**任务。

以当前身份订阅任务更新事件。

此快捷命令与 `event +subscribe` 不同：
- `task +subscribe-event` 为**当前身份**注册任务事件访问权限
- 使用 `--as user` 时，它将为**当前用户**订阅其创建、负责或关注的任务事件
- 使用 `--as bot` 时，它将使用**应用身份**订阅应用负责的任务事件

任务事件类型为：

```text
task.task.update_user_access_v2
```

在此事件中，任务变更通过提交类型（字符串值）表示。去重后的列表：

```text
task_assignees_update
task_completed_update
task_create
task_deleted
task_desc_update
task_followers_update
task_reminders_update
task_start_due_update
task_summary_update
```

事件负载结构（示例）：

```json
{
  "event_id": "evt_xxx",
  "event_types": ["task_summary_update"],
  "task_guid": "task_guid_xxx",
  "timestamp": "1775793266152",
  "type": "task.task.update_user_access_v2"
}
```

- `type`：事件类型，应为 `task.task.update_user_access_v2`
- `event_id`：唯一事件 ID（可用于去重）
- `event_types`：提交类型列表（参见上方的去重列表）
- `task_guid`：发生变更的任务 GUID
- `timestamp`：事件时间戳（毫秒）

在实践中，这意味着：
- 使用 `--as user` 时，订阅的用户可以接收其通过创建、分配或关注而可见的任务更新
- 使用 `--as bot` 时，订阅覆盖应用负责的任务

要实际接收已订阅的事件，请使用标准的事件 WebSocket 接收器：

```bash
lark-cli event +subscribe --event-types task.task.update_user_access_v2 --compact --quiet
```

完整流程为：
1. 使用 `lark-cli task +subscribe-event [--as user|bot]` 注册订阅
2. 使用 `lark-cli event +subscribe --event-types task.task.update_user_access_v2 ...` 接收这些事件

## 推荐命令

```bash
lark-cli task +subscribe-event
```
# 使用应用身份订阅
lark-cli task +subscribe-event --as bot


## 参数

此快捷命令无额外参数。

## 工作流程

1. 确认用户希望使用 `user` 身份还是 `bot` 身份订阅。
2. 执行 `lark-cli task +subscribe-event`
3. 报告订阅是否成功，并说明订阅适用于哪个身份。

> [!CAUTION]
> 这是一个**写操作**——执行前必须确认用户的意图。