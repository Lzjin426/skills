# im +messages-resources-download

> **前提条件：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md)，了解身份验证、全局参数和安全规则。

从消息中下载图片或文件资源。支持使用 HTTP Range 请求**自动分块下载大文件**。资源通过 `message_id` + `file_key` 的组合来标识，两者均直接来自 `im +chat-messages-list` 返回的消息内容。

> **注意：** 只读消息命令会在消息内容中呈现资源键，但不会自动下载二进制文件。当您需要获取实际的图片/文件字节数据或将其保存到特定路径时，请使用此命令。

此技能映射到快捷命令：`lark-cli im +messages-resources-download`（内部调用 `GET /open-apis/im/v1/messages/{message_id}/resources/{file_key}`）。

## 命令

```bash
# 下载图片（保存到当前目录）
lark-cli im +messages-resources-download --message-id om_xxx --file-key img_v3_xxx --type image

# 下载文件
lark-cli im +messages-resources-download --message-id om_xxx --file-key file_v3_xxx --type file

# 指定输出路径
lark-cli im +messages-resources-download --message-id om_xxx --file-key img_v3_xxx --type image --output ./photo.png

# 以机器人身份下载
lark-cli im +messages-resources-download --message-id om_xxx --file-key img_v3_xxx --type image --as bot

# 预览请求而不执行
lark-cli im +messages-resources-download --message-id om_xxx --file-key img_v3_xxx --type image --dry-run
```

## 参数

| 参数 | 是否必需 | 描述 |
|------|------|------|
| `--message-id <id>` | 是 | 消息 ID（格式为 `om_xxx`） |
| `--file-key <key>` | 是 | 资源键（`img_xxx` 或 `file_xxx`） |
| `--type <type>` | 是 | 资源类型：`image` 或 `file` |
| `--output <path>` | 否 | 输出路径（仅支持相对路径；不允许使用 `..` 进行路径遍历；默认为 `file_key` 作为文件名）。如果未提供文件扩展名，将根据 Content-Type 自动添加 |
| `--as <identity>` | 否 | 身份类型：`user`（默认）或 `bot` |
| `--dry-run` | 否 | 仅打印请求，不执行 |

## 大文件下载（自动分块）

下载大文件时，该命令会自动使用 **HTTP Range 请求**进行可靠的分块下载：

| 行为 | 详情 |
|----------|---------|
| 探测块 | 前 128 KB 用于检测文件大小和 Content-Type |
| 块大小 | 每个后续请求 8 MB |
| 工作线程 | 单线程顺序下载（确保可靠性） |
| 重试 | 对于瞬时请求失败，最多重试 2 次，并采用指数退避策略 |

**优势：**
- 减少大文件下载期间瞬时请求失败的影响
- 根据 Content-Type 自动检测并附加正确的文件扩展名
- 下载完成后验证文件大小完整性

## `file_key` 来源

消息内容中的不同资源标记对应不同的 `file_key` 和 `type` 值：

| 消息类型 | 内容中的标记 | `file_key` 格式 | `--type` |
|---------|-------------|---------------|--------|
| 图片 | `img_xxx` | `img_xxx` | `image` |
| 文件 | `file_xxx` | `file_xxx` | `file` |
| 音频 | `file_xxx` | `file_xxx` | `file` |
| 视频 | `file_xxx` | `file_xxx` | `file` |

## 使用场景

### 场景：从消息中提取并下载图片

```bash
# 步骤 1：获取消息并找到包含图片的消息
lark-cli im +chat-messages-list --chat-id oc_xxx
# 在响应中您会看到：{ "msg_type": "image", "content": "{\"image_key\":\"img_v3_xxx\"}" }

# 步骤 2：下载图片
lark-cli im +messages-resources-download --message-id om_xxx --file-key img_v3_xxx --type image
```

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| 下载失败 | `file_key` 与 `message_id` 不匹配 | 确保 `file_key` 来自该消息的内容 |
| 遇到错误码 234002 或 14005 | 无权限，**并非**缺少 API 范围 | 无法访问此聊天或文件已被删除 — 请勿重试，将错误返回给用户 |
| 权限被拒绝 | `im:message:readonly` 未授权 | 运行 `auth login --scope "im:message:readonly"` |
| 文件大小不匹配 | 分块下载完整性检查失败 | 下载期间网络不稳定；重试命令 |
| Content-Range 错误 | 服务器返回了无效的范围头 | 瞬时 API 问题；重试命令 |

## 参考

- [lark-im](../SKILL.md) - 所有与消息相关的命令
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数