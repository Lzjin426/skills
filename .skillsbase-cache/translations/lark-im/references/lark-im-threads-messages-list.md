# im +threads-messages-list

> **前置要求：** 请先阅读 [`../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 以了解身份验证、全局参数和安全规则。

获取线程内的回复消息列表。当 `im +chat-messages-list` 返回的消息中包含 `thread_id` 字段时，可使用此命令查看该线程中的所有回复。

此技能映射的快捷命令为：`lark-cli im +threads-messages-list`（内部调用 `GET /open-apis/im/v1/messages` 并设置 `container_id_type=thread` 来获取线程消息）。

## 命令

```bash
# 获取线程回复（默认按时间升序，表格输出）
lark-cli im +threads-messages-list --thread omt_xxx

# 按时间倒序（最新优先）
lark-cli im +threads-messages-list --thread omt_xxx --sort desc

# 控制每页大小
lark-cli im +threads-messages-list --thread omt_xxx --page-size 20

# 分页
lark-cli im +threads-messages-list --thread omt_xxx --page-token <PAGE_TOKEN>

# 输出格式选项
lark-cli im +threads-messages-list --thread omt_xxx --format pretty
lark-cli im +threads-messages-list --thread omt_xxx --format table
lark-cli im +threads-messages-list --thread omt_xxx --format csv

# 以机器人身份查看
lark-cli im +threads-messages-list --thread omt_xxx --as bot

# 预览请求而不执行
lark-cli im +threads-messages-list --thread omt_xxx --dry-run
```

## 参数

| 参数 | 是否必需 | 描述 |
|------|------|------|
| `--thread <id>` | 是 | 线程 ID（格式为 `om_xxx` 或 `omt_xxx`） |
| `--sort <order>` | 否 | 排序顺序：`asc`（默认）/ `desc` |
| `--page-size <n>` | 否 | 每页项目数（默认 50，范围 1-500） |
| `--page-token <token>` | 否 | 用于获取下一页的分页令牌 |
| `--format <fmt>` | 否 | 输出格式：`json`（默认）/ `pretty` / `table` / `ndjson` / `csv` |
| `--as <identity>` | 否 | 身份类型：`user`（默认）/ `bot` |
| `--dry-run` | 否 | 仅打印请求，不执行 |

## 核心约束

### 1. `thread_id` 的来源

`thread_id`（`omt_xxx` 或 `om_xxx`）来源于 `im +chat-messages-list` 或 `im +messages-search` 返回结果中的 `thread_id` 字段。请勿猜测线程 ID。应先获取消息，然后使用返回的值。

### 2. 不支持时间过滤

由于飞书 API 的限制，线程消息不支持 `start_time` / `end_time` 过滤。请使用分页和排序顺序来控制范围。

### 3. 分页（`has_more` / `page_token`）

- 当结果包含 `has_more=true` 时，使用 `page_token` 获取下一页
- 如果需要完整的线程，请持续分页；如果只需要概览，通常第一页就足够了

### 4. 推荐的扩展策略

| 场景 | 推荐参数 |
|------|---------|
| 快速查看最近的回复 | `--sort desc --page-size 10` |
| 按时间顺序阅读完整线程 | `--sort asc --page-size 50`，然后根据需要分页 |
| 仅确认是否存在回复 | `--sort desc --page-size 1` |

## 使用场景

### 场景 1：展开在群消息中发现的线程

```bash
# 步骤 1：获取群消息并找到包含 thread_id 的消息
lark-cli im +chat-messages-list --chat-id oc_xxx

# 步骤 2：从 JSON 输出中提取 thread_id 并获取线程回复
lark-cli im +threads-messages-list --thread omt_xxx
```

### 场景 2：对长线程进行分页

```bash
# 第一页
lark-cli im +threads-messages-list --thread omt_xxx

# 如果返回了 has_more=true，则使用 page_token 继续
lark-cli im +threads-messages-list --thread omt_xxx --page-token <PAGE_TOKEN>
```

## 资源渲染

线程回复会被渲染成人类可读的文本。图片消息会显示为占位符，例如 `[图片: img_xxx]`；资源二进制文件**不会**自动下载。

其他资源类型（文件、音频、视频）仍需通过 `im +messages-resources-download` 手动下载。请参阅 [lark-im-messages-resources-download](lark-im-messages-resources-download.md)。

## 常见错误与故障排除

| 现象 | 根本原因 | 解决方案 |
|---------|---------|---------|
| "无效的线程 ID 格式" | `thread_id` 不以 `om_` 或 `omt_` 开头 | 使用有效的 `om_xxx` 或 `omt_xxx` 值 |
| 线程结果为空 | 错误的 thread_id 或线程中没有回复 | 确认 thread_id 来自 `im +chat-messages-list` 的输出 |
| 权限被拒绝 | 用户未授权或不是会话成员 | 确保 OAuth 授权已完成，且身份是聊天成员 |

## 参考

- [lark-im](../SKILL.md) - 所有与消息相关的命令
- [lark-im-chat-messages-list](lark-im-chat-messages-list.md) - 获取会话消息（`thread_id` 的来源）
- [lark-shared](../../lark-shared/SKILL.md) - 身份验证和全局参数