# im +chat-create

> **前提条件：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 以了解身份验证、全局参数和安全规则。

创建群聊。支持用户身份（`--as user`）和机器人身份（`--as bot`）。您可以指定群组名称、描述、成员（用户/机器人）、所有者以及聊天类型（私密/公开）。

此技能映射到快捷命令：`lark-cli im +chat-create`（内部调用 `POST /open-apis/im/v1/chats`）。

- `--as bot` 需要 `im:chat:create` 权限范围。
- `--as user` 需要 `im:chat:create_by_user` 权限范围。

## 命令

```bash
# 创建私密群聊（默认）
lark-cli im +chat-create --name "我的群组"

# 创建公开群聊（名称必填且至少 2 个字符）
lark-cli im +chat-create --name "公开群组" --type public

# 指定群组所有者
lark-cli im +chat-create --name "我的群组" --owner ou_xxx

# 邀请用户成员（逗号分隔的 open_ids，最多 50 个）
lark-cli im +chat-create --name "我的群组" --users "ou_aaa,ou_bbb"

# 邀请机器人成员（逗号分隔的应用 ID，最多 5 个）
lark-cli im +chat-create --name "我的群组" --bots "cli_aaa,cli_bbb"

# 同时邀请用户和机器人
lark-cli im +chat-create --name "我的群组" --users "ou_aaa" --bots "cli_aaa"

# 将创建机器人设为群管理员（仅限机器人身份）
lark-cli im +chat-create --name "我的群组" --set-bot-manager --as bot

# JSON 输出
lark-cli im +chat-create --name "我的群组" --format json

# 使用机器人身份创建群组
lark-cli im +chat-create --name "我的群组" --users "ou_aaa" --as bot

# 使用用户身份创建群组
lark-cli im +chat-create --name "我的群组" --users "ou_aaa,ou_bbb" --as user

# 预览请求而不实际创建
lark-cli im +chat-create --name "我的群组" --dry-run
```

## 参数

| 参数 | 是否必填 | 限制 | 描述 |
|------|------|------|------|
| `--name <name>` | 公开群组必填 | 最长 60 个字符；公开群组至少 2 个字符 | 群组名称（私密群组若省略则默认为 `"(no subject)"`） |
| `--description <text>` | 否 | 最长 100 个字符 | 群组描述 |
| `--users <ids>` | 否 | 最多 50 个，格式 `ou_xxx` | 逗号分隔的用户 open_ids |
| `--bots <ids>` | 否 | 最多 5 个，格式 `cli_xxx` | 逗号分隔的机器人应用 ID |
| `--owner <open_id>` | 否 | 格式 `ou_xxx` | 所有者 open_id（使用 `--as bot` 时默认为机器人，使用 `--as user` 时默认为授权用户） |
| `--type <type>` | 否 | `private`（默认）或 `public` | 群组类型 |
| `--set-bot-manager` | 否 | - | 将创建机器人设为群管理员（仅在使用 `--as bot` 时有效） |
| `--format json` | 否 | - | 以 JSON 格式输出 |
| `--as <identity>` | 否 | `bot` 或 `user` | 身份类型 |
| `--dry-run` | 否 | - | 预览请求而不执行 |

## AI 使用指南

### 使用 `--as bot` 时

机器人在创建群组时可能无法邀请与其相互不可见的用户（错误 232043）。为避免此问题，请使用下面的**两步流程**，而不是在 `--users` 中传递其他用户的 open_ids。

1.  **获取当前用户的 open_id：** 运行 `lark-cli contact +search-user --query "<姓名或邮箱>"` 来获取。
2.  **创建群组 — 默认包含当前用户：**

    ```bash
    lark-cli im +chat-create --name "<群组名称>" \
      --users "<当前用户 open_id>" --as bot
    ```

    **默认行为：** 始终将当前用户添加到群组中，除非用户明确表示“不要添加我”或“仅机器人群组” — 只有在这种情况下才省略 `--users`。

3.  **通过用户身份添加其他成员**（要求当前用户已在群组中）：

    ```bash
    lark-cli im chat.members create \
      --params '{"chat_id":"<步骤 2 中的 chat_id>","member_id_type":"open_id","succeed_type":1}' \
      --data '{"id_list":["ou_aaa","ou_bbb"]}' \
      --as user
    ```

    `succeed_type=1` 确保可联系到的用户被成功添加；无法联系到的用户将在 `invalid_id_list` 中返回，而不会导致整个请求失败。

4.  **检查响应中的 `invalid_id_list`**。如果非空，向用户报告哪些成员无法添加。

### 使用 `--as user` 时

用户身份没有机器人可见性的限制，因此可以一步创建群组并邀请成员：

```bash
lark-cli im +chat-create --name "<群组名称>" --users "ou_aaa,ou_bbb" --as user
```

授权用户自动成为群组创建者和成员。

## 输出字段

| 字段 | 描述 |
|------|------|
| `chat_id` | 新群组的 ID（`oc_xxx` 格式） |
| `name` | 群组名称 |
| `chat_type` | 群组类型（`private` / `public`） |
| `owner_id` | 所有者 ID（当机器人创建群组且未指定 `--owner` 时可能为空） |
| `external` | 是否为外部群组 |
| `share_link` | 群组分享链接（如果获取失败则省略） |

## 使用场景

### 场景 1：创建群组并指定所有者

```bash
lark-cli im +chat-create --name "项目讨论群" --owner ou_xxx
```

### 场景 2：创建群组并邀请用户和机器人

```bash
lark-cli im +chat-create --name "项目讨论群" \
  --owner ou_xxx \
  --users "ou_aaa,ou_bbb" \
  --bots "cli_aaa"
```

### 场景 3：创建群组并发送欢迎消息

```bash
CHAT_ID=$(lark-cli im +chat-create --name "新群组" --format json | jq -r '.data.chat_id')
lark-cli im +messages-send --chat-id "$CHAT_ID" --text "欢迎大家！"
```

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| 权限被拒绝 (99991672) | 应用未启用 `im:chat:create`（机器人）或 `im:chat:create_by_user`（用户）权限 | 在开放平台控制台中为应用启用所需权限 |
| `--name is required for public groups and must be at least 2 characters` | 创建公开群组时未提供名称或名称少于 2 个字符 | 提供至少 2 个字符的名称 |
| `--name exceeds the maximum of 60 characters` | 群组名称过长 | 将名称缩短至 60 个字符以内 |
| `--description exceeds the maximum of 100 characters` | 群组描述过长 | 将描述缩短至 100 个字符以内 |
| `--users exceeds the maximum of 50` | 提供的用户成员过多 | 将操作分批进行，稍后再添加更多成员 |
| `--bots exceeds the maximum of 5` | 提供的机器人成员过多 | 一次最多邀请 5 个机器人 |
| `invalid user id: expected open_id (ou_xxx)` | 用户 ID 格式无效 | 对用户使用 `ou_xxx` 格式 |
| `invalid bot id: expected app ID (cli_xxx)` | 机器人 ID 格式无效 | 对机器人使用 `cli_xxx` 格式 |
| `invalid --owner: expected open_id (ou_xxx)` | 所有者 ID 格式无效 | 对所有者使用 `ou_xxx` 格式 |
| `bot is invisible to user` (232043) | 机器人与目标用户相互不可见 | 遵循上方 AI 使用指南中的两步流程 — 创建时不要在 `--users` 中传递其他用户 |

## 参考

- [lark-im](../SKILL.md) - 所有 IM 命令
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数