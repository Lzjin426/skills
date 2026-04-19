# im +chat-messages-list

> **前提条件：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 以了解身份验证、全局参数和安全规则。

获取会话的消息列表。支持群聊和私聊。

此技能映射到快捷命令：`lark-cli im +chat-messages-list`（内部调用 `GET /open-apis/im/v1/messages`，并在需要时自动解析私聊的 chat_id）。

## 命令

```bash
# 获取群聊消息（默认输出 JSON）
lark-cli im +chat-messages-list --chat-id oc_xxx

# 获取与用户的私聊消息（传入 open_id，自动解析 p2p chat_id）
lark-cli im +chat-messages-list --user-id ou_xxx

# 指定时间范围（ISO 8601 格式）
lark-cli im +chat-messages-list --chat-id oc_xxx --start "2026-03-10T00:00:00+08:00" --end "2026-03-11T00:00:00+08:00"

# 指定时间范围（仅日期）
lark-cli im +chat-messages-list --chat-id oc_xxx --start 2026-03-10 --end 2026-03-11

# 控制排序顺序和分页大小（最大 50）
lark-cli im +chat-messages-list --chat-id oc_xxx --sort asc --page-size 20

# 分页
lark-cli im +chat-messages-list --chat-id oc_xxx --page-token "xxx"

# JSON 输出
lark-cli im +chat-messages-list --chat-id oc_xxx --format json
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--chat-id <id>` | 二选一 | 直接指定会话的 chat_id（例如群聊 `oc_xxx`） |
| `--user-id <id>` | 二选一 | 通过对方的 open_id（`ou_xxx`）指定私聊会话；p2p chat_id 会自动解析。需要用户身份（`--as user`）；不支持机器人身份 |
| `--start <time>` | 否 | 开始时间（ISO 8601 格式或仅日期） |
| `--end <time>` | 否 | 结束时间（ISO 8601 格式或仅日期） |
| `--sort <order>` | 否 | 排序顺序：`asc` / `desc`（默认 `desc`） |
| `--page-size <n>` | 否 | 分页大小（默认 50，最大 50） |
| `--page-token <token>` | 否 | 分页令牌 |

> 规则：`--chat-id` 和 `--user-id` 互斥。必须且只能提供其中一个。

## 资源渲染

消息会被渲染成人类可读的文本以供查看。图片消息会显示为占位符，例如 `[Image: img_xxx]`；文件和视频会在内容中显示资源键。此命令**不会**自动下载资源二进制文件。

当你需要从特定消息下载图片或文件时，请使用 [lark-im-messages-resources-download](lark-im-messages-resources-download.md)。

| 资源类型 | 内容中的标记 | 行为 |
|---------|-------------|------|
| 图片 | `[Image: img_xxx]` | 使用 `im +messages-resources-download --type image` 手动下载 |
| 文件 | `<file key="file_xxx" .../>` | 使用 `im +messages-resources-download --type file` 手动下载 |
| 音频 | `<audio key="file_xxx" .../>` | 使用 `im +messages-resources-download --type file` 手动下载 |
| 视频 | `<video key="file_xxx" .../>` | 使用 `im +messages-resources-download --type file` 手动下载 |

## 话题展开 (`thread_id`)

在 JSON 输出中，消息可能包含 `thread_id`（`omt_xxx`）字段，这表示该消息在话题中有回复。使用 [`im +threads-messages-list`](lark-im-threads-messages-list.md) 来查看该话题中的回复：

```bash
lark-cli im +threads-messages-list --thread omt_xxx
```

| 场景 | 建议 |
|------|------|
| 你需要上下文 | 对发现的 thread_id 调用 `im +threads-messages-list --sort desc --page-size 10` 以查看最近的回复 |
| 用户要求查看“完整讨论” | 使用 `im +threads-messages-list --sort asc --page-size 50`，然后根据需要分页 |
| 你只需要概览 | 跳过话题展开 |

## 输出字段

| 字段 | 说明 |
|------|------|
| `messages` | 消息数组 |
| `total` | 当前页的消息数量 |
| `has_more` | 是否有更多页可用 |
| `page_token` | 下一页的分页令牌 |

每条消息包含：

| 字段 | 说明 |
|------|------|
| `message_id` | 消息 ID |
| `msg_type` | 消息类型：`text`、`image`、`file`、`interactive`、`post`、`audio`、`video`、`system` 等 |
| `create_time` | 创建时间 |
| `sender` | 发送者信息（对于用户发送者包含 `name`） |
| `content` | 消息内容 |
| `deleted` | 消息是否已被撤回（始终存在，`true` = 已撤回） |
| `updated` | 消息发送后是否被编辑过 |
| `mentions` | 消息中 @ 提及的数组；每个元素包含 `{id, key, name}`。仅当消息包含 @ 提及时存在 |
| `thread_id` | 话题 ID（`omt_xxx`），如果该消息在话题中有回复。仅当存在回复时存在 |

## 分页 (`has_more` / `page_token`)

当有更多数据可用时，`im +chat-messages-list` 会返回 `has_more` 和 `page_token`。使用 `--page-token` 继续获取：

```bash
lark-cli im +chat-messages-list --chat-id oc_xxx --page-token <PAGE_TOKEN>
```

你也可以回退到通用 API：

```bash
lark-cli api GET /open-apis/im/v1/messages \
  --params 'container_id_type=chat&container_id=oc_xxx&page_size=50&page_token=<PAGE_TOKEN>'
```

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| `specify --chat-id <chat_id> or --user-id <open_id>` | 未提供 `--chat-id` 或 `--user-id` | 必须且只能提供一个 |
| `--chat-id and --user-id cannot be specified together` | 同时提供了两个参数 | 只使用一个 |
| `--user-id requires user identity (--as user); use --chat-id when calling with bot identity` | 在机器人身份下使用了 `--user-id` | p2p 解析端点需要用户身份。要么传递 `--as user`，要么单独查找 p2p `chat_id` 并通过 `--chat-id` 传递 |
| `P2P chat not found for this user` | 使用了 `--user-id`，但当前身份与该用户之间不存在私聊会话 | 确认当前身份与目标用户之间存在私聊关系 |
| `--start: invalid time format` | 时间格式无效 | 使用 ISO 8601 或仅日期格式，例如 `2026-03-10` |
| 权限被拒绝 | 缺少消息读取权限 | 确保应用已启用 `im:message:readonly` 和 `im:chat:read` |

## AI 使用指南

1.  **从聊天名称解析 chat_id：** 当用户通过名称引用聊天，而你没有 `chat_id` 时，请先使用 [`+chat-search`](lark-im-chat-search.md)：
    ```bash
    # 通过名称查找 chat_id，然后列出消息
    lark-cli im +chat-search --query "<聊天名称关键词>" --format json
    lark-cli im +chat-messages-list --chat-id <chat_id>
    ```
    **不要使用 `im chats search` 或 `im chats list` — 始终使用 `+chat-search` 快捷命令。**
2.  **优先使用 `--chat-id`：** 如果已知 chat_id，直接使用它以避免额外的 API 调用。
3.  **对于私聊：** 使用 `--user-id` 自动解析 p2p chat，而不是手动查找。这需要用户身份（`--as user`）；对于机器人身份，请自行解析 p2p `chat_id` 并通过 `--chat-id` 传递。
4.  **对于时间范围：** 支持 ISO 8601 和仅日期输入。仅日期格式通常更简单。
5.  **对于完整内容：** 表格输出会截断内容。当你需要完整的消息正文时，请使用 `--format json`。
6.  **对于发送者信息：** 该命令已解析发送者姓名，因此你无需单独查找。

## 参考

- [lark-im](../SKILL.md) - 所有 IM 命令
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数