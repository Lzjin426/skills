---
name: lark-event
version: 1.0.0
description: "飞书事件订阅：通过 WebSocket 长连接实时监听飞书事件（消息、通讯录变更、日历变更等），输出 NDJSON 到 stdout，支持 compact Agent 友好格式、正则路由、文件输出。当用户需要实时监听飞书事件、构建事件驱动管道时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli event --help"
---

# event (v1)

> **前置条件：** 先阅读 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md) 了解认证、权限处理和安全规则。

## 快捷命令（推荐优先使用）

快捷命令是对常用操作的高级封装（`lark-cli event +<verb> [flags]`）。有快捷命令的操作优先使用。

| 快捷命令 | 说明 |
|----------|------|
| [`+subscribe`](references/lark-event-subscribe.md) | 通过 WebSocket 长连接订阅飞书事件（只读，输出 NDJSON）；仅限机器人使用；支持 compact Agent 友好格式、正则路由、文件输出 |