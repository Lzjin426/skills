# im +chat-update

> **前提条件：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 以了解身份验证、全局参数和安全规则。

更新群组的名称或描述。支持 **TAT（机器人）** 和 **UAT（用户）** 两种身份。

此技能映射到快捷命令：`lark-cli im +chat-update`（内部调用 `PUT /open-apis/im/v1/chats/:chat_id`）。

## 命令

```bash
# 更新群组名称
lark-cli im +chat-update --chat-id oc_xxx --name "新群组名称"

# 更新群组描述
lark-cli im +chat-update --chat-id oc_xxx --description "更新后的群组描述"

# 同时更新多个字段
lark-cli im +chat-update --chat-id oc_xxx \
  --name "Q2 项目团队" \
  --description "负责 Q2 目标跟踪"

# 预览请求而不实际执行
lark-cli im +chat-update --chat-id oc_xxx --name "测试" --dry-run
```

## 参数

### 必需参数

| 参数 | 描述 |
|------|------|
| `--chat-id <oc_xxx>` | 群组 ID |

### 可选字段

| 参数 | 限制 | 描述 |
|------|------|------|
| `--name <name>` | 最多 60 个字符 | 群组名称 |
| `--description <text>` | 最多 100 个字符 | 群组描述 |

### 全局参数

| 参数 | 描述 |
|------|------|
| `--format json` | 以 JSON 格式输出（默认） |
| `--dry-run` | 预览请求而不实际执行 |

## 使用场景

### 场景 1：重命名群组并更新其描述

```bash
lark-cli im +chat-update --chat-id oc_xxx \
  --name "Q2 项目团队" \
  --description "负责 Q2 目标跟踪"
```

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| `无效的 --chat-id: 应为群组 ID (oc_xxx)` | 无效的 chat_id 格式 | 使用有效的 `oc_xxx` 群组 ID |
| `--name 超过 60 个字符的最大限制` | 群组名称过长 | 将名称缩短至 60 个字符以内 |
| `--description 超过 100 个字符的最大限制` | 群组描述过长 | 将描述缩短至 100 个字符以内 |
| `必须指定至少一个字段进行更新` | 未提供任何更新字段 | 指定至少一个要更新的字段 |
| 权限被拒绝 (99991679) | 缺少 `im:chat:update` 权限 | 运行 `lark-cli auth login --scope "im:chat:update"` |
| 非群主/管理员无法更新 (232016/232002/232017) | 当前身份不是群主或管理员 | 尝试使用 `--as bot` 或 `--as user` 切换身份 |
| 不在群组中 (232011) | 当前用户不是群组成员 | 使用成员身份（`--as bot`）或先加入群组 |

## AI 使用指南

### 身份选择

`+chat-update` 支持用户和机器人两种身份（`--as user` / `--as bot`）。

尽可能根据上下文推断群主身份（例如，如果机器人刚刚创建了群组，则群主就是该机器人）并直接使用匹配的身份。如果所有权不明确，请先查询群组并确认 `owner_id`。

身份选择应遵循 [群聊身份规则](lark-im-chat-identity.md)：如果用户明确指定了身份，则直接使用；否则根据上下文推断群主身份。

## 参考

- [lark-im](../SKILL.md) - 所有 IM 命令
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数