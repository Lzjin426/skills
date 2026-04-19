# im +chat-search

> **前提条件：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 以了解身份验证、全局参数和安全规则。

搜索用户或机器人可见的群聊列表，包括用户或机器人已加入的群聊以及对其可见的公开群聊。支持对群聊名称和成员名称进行关键词匹配，包括拼音和前缀模糊搜索。

此技能映射到快捷命令：`lark-cli im +chat-search`（内部调用 `POST /open-apis/im/v2/chats/search`）。

## 命令

```bash
# 通过关键词搜索群聊
lark-cli im +chat-search --query "project"

# 按搜索类型限制
lark-cli im +chat-search --query "project" --search-types "private,public_joined"

# 按成员 open_ids 过滤（同时使用关键词）
lark-cli im +chat-search --query "project" --member-ids "ou_xxx,ou_yyy"

# 仅通过成员 open_ids 搜索
lark-cli im +chat-search --member-ids "ou_xxx,ou_yyy"

# 仅显示你创建或管理的群聊
lark-cli im +chat-search --query "project" --is-manager

# 设置每页大小
lark-cli im +chat-search --query "project" --page-size 10

# 分页
lark-cli im +chat-search --query "project" --page-token "xxx"

# JSON 输出
lark-cli im +chat-search --query "project" --format json

# 预览请求而不执行
lark-cli im +chat-search --query "project" --dry-run
```

## 参数

| 参数 | 是否必需 | 限制 | 描述 |
|------|------|------|------|
| `--query <keyword>` | 否（`--query` / `--member-ids` 至少需要一个） | 最多 64 个字符 | 搜索关键词。支持匹配本地化的群聊名称、成员名称、多语言搜索、拼音和前缀模糊搜索。如果查询包含 `-`，会自动用引号包裹 |
| `--search-types <types>` | 否 | 逗号分隔：`private`, `external`, `public_joined`, `public_not_joined` | 限制搜索返回的可见群聊类型 |
| `--member-ids <ids>` | 否（`--query` / `--member-ids` 至少需要一个） | 最多 50 个，格式 `ou_xxx` | 按成员 open_ids 过滤；可单独使用或与 `--query` 结合使用 |
| `--is-manager` | 否 | - | 仅显示你创建或管理的群聊 |
| `--disable-search-by-user` | 否 | - | 禁用基于成员名称的匹配，仅按群聊名称搜索 |
| `--sort-by <field>` | 否 | `create_time_desc`, `update_time_desc`, `member_count_desc` | 按字段降序排序 |
| `--page-size <n>` | 否 | 1-100，默认 20 | 每页结果数量 |
| `--page-token <token>` | 否 | - | 来自先前响应的分页令牌 |
| `--format json` | 否 | - | 以 JSON 格式输出 |
| `--dry-run` | 否 | - | 预览请求而不执行 |

> **注意：** 同时支持 `--as user`（默认）和 `--as bot`。使用机器人身份时，应用必须已启用机器人能力。

## 输出字段

| 字段 | 描述 |
|------|------|
| `chat_id` | 群聊 ID（`oc_xxx` 格式） |
| `name` | 群聊名称 |
| `description` | 群聊描述 |
| `owner_id` | 群主 ID |
| `external` | 是否为外部群聊 |
| `chat_status` | 群聊状态（`normal` / `dissolved` / `dissolved_save`） |

## 使用场景

### 场景 1：搜索包含关键词的群聊

```bash
lark-cli im +chat-search --query "design review"
```

### 场景 2：搜索群聊并列出最近消息

```bash
CHAT_ID=$(lark-cli im +chat-search --query "project" --format json | jq -r '.data.chats[0].chat_id')
lark-cli im +chat-messages-list --chat-id "$CHAT_ID"
```

### 场景 3：搜索群聊并发送消息

```bash
CHAT_ID=$(lark-cli im +chat-search --query "daily report" --format json | jq -r '.data.chats[0].chat_id')
lark-cli im +messages-send --chat-id "$CHAT_ID" --text "Today's progress update"
```

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| `--query and --member-ids cannot both be empty` | 两者均未提供 | 至少提供 `--query` 或 `--member-ids` |
| 结果为空 | 没有可见群聊匹配关键词或过滤器 | 放宽关键词或过滤器并重试 |
| `--page-size must be an integer between 1 and 100` | page-size 超出范围或不是整数 | 使用 1 到 100 之间的整数 |
| 权限被拒绝 (99991672) | 机器人应用未启用 `im:chat:read` TAT 权限 | 在开放平台控制台中为应用启用该权限 |
| 使用 `--as user` 时权限被拒绝 (99991679) | UAT 未授权 `im:chat:read` | 运行 `lark-cli auth login --scope "im:chat:read"` |
| `Bot ability is not activated` (232025) | 应用未启用机器人能力 | 在开放平台控制台中启用机器人能力 |

## AI 使用指南

当用户要求搜索群聊时，请遵循以下规则：

1.  **至少需要一个过滤器：** `--query` 和 `--member-ids` 不能同时为空。单独使用或组合使用均有效。
2.  **搜索范围有限：** 只能找到当前用户或机器人可见的群聊（已加入的群聊加上公开群聊）。这不是对所有群聊的全局搜索。
3.  **控制结果数量：** 结果集可能很大。请有意识地使用 `--page-size`。
4.  **建议后续操作：** 找到群聊后，常见的下一步包括列出最近消息（`im +chat-messages-list`）或发送消息（`im +messages-send`）。
5.  **切勿回退到群聊列表：** 如果 `+chat-search` 返回空结果，**不要**尝试使用 `im chats list` 或 `GET /open-apis/im/v1/chats` 作为回退方案。列表 API 不是搜索 API——它返回所有群聊而不进行关键词过滤，无法帮助定位目标群聊。相反，应请用户优化关键词或检查该群聊是否对当前身份可见。

## 参考

- [lark-im](../SKILL.md) - 所有 IM 命令
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数