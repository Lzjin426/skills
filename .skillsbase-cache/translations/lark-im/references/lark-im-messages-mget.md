# im +messages-mget

> **前置条件：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 以了解身份验证、全局参数和安全规则。

批量获取消息详情。给定一个消息 ID 列表，此命令可一次性返回多条消息的完整内容，并自动解析发送者姓名。

> **同时支持 `--as user`（默认）和 `--as bot`。**

此技能映射到快捷命令：`lark-cli im +messages-mget`（内部调用 `GET /open-apis/im/v1/messages/mget`）。

## 命令

```bash
# 获取单条消息
lark-cli im +messages-mget --message-ids om_xxx

# 批量获取多条消息（逗号分隔）
lark-cli im +messages-mget --message-ids "om_aaa,om_bbb,om_ccc"

# JSON 格式输出
lark-cli im +messages-mget --message-ids "om_aaa,om_bbb" --format json

# 预览请求而不实际执行
lark-cli im +messages-mget --message-ids "om_aaa" --dry-run
```

## 参数

| 参数 | 是否必需 | 限制 | 描述 |
|------|------|------|------|
| `--message-ids <ids>` | 是 | 至少一个，最多 50 个，`om_xxx` 格式，逗号分隔 | 消息 ID 列表 |

## 输出字段

| 字段 | 描述 |
|------|------|
| `messages` | 消息数组 |
| `total` | 返回的消息数量 |

每条消息包含：

| 字段 | 描述 |
|------|------|
| `message_id` | 消息 ID |
| `msg_type` | 消息类型（`text`、`image`、`file` 等） |
| `create_time` | 创建时间 |
| `sender` | 发送者信息（包含 `name`） |
| `content` | 消息内容 |

## 使用场景

### 场景 1：获取特定消息的完整内容

```bash
lark-cli im +messages-mget --message-ids om_xxx --format json
```

### 场景 2：一次性批量获取多条消息

```bash
lark-cli im +messages-mget --message-ids "om_aaa,om_bbb,om_ccc"
```

### 场景 3：与消息列表命令结合使用

先通过 `+chat-messages-list` 获取消息 ID，再通过 `+messages-mget` 获取完整内容：

```bash
# 获取消息列表
lark-cli im +chat-messages-list --chat-id oc_xxx --format json

# 获取特定消息详情
lark-cli im +messages-mget --message-ids "om_aaa,om_bbb"
```

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| `--message-ids 需要至少一个消息 ID` | 未提供消息 ID | 提供至少一个消息 ID |
| `无效的消息 ID：必须以 om_ 开头` | 消息 ID 格式无效 | 消息 ID 必须以 `om_` 开头 |
| 权限被拒绝 | 缺少消息读取权限 | 确保应用已启用 `im:message:readonly` 和 `contact:user.base:readonly` 权限 |
| 结果为空 | 消息 ID 不存在或无法访问 | 验证 ID 和访问权限 |

## AI 使用指南

1.  **使用 JSON 获取完整内容：** 表格输出会截断内容。当需要完整消息体时，请使用 `--format json`。
2.  **发送者姓名已自动丰富：** 此命令会自动解析发送者姓名，因此无需额外查找。
3.  **图片以占位符形式呈现：** 图片消息会显示为占位符，例如 `[Image: img_xxx]`。当需要二进制资源时，请使用 `+messages-resources-download`。
4.  **批量处理更高效：** 在一个请求中获取多个 ID 比重复调用 API 更高效。

## 参考

- [lark-im](../SKILL.md) - 所有 IM 命令
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数