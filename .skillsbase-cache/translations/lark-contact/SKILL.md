---
name: lark-contact
version: 1.0.0
description: "飞书通讯录：查询组织架构、人员信息和搜索员工。获取当前用户或指定用户的详细信息、通过关键词搜索员工（姓名/邮箱/手机号）。当用户需要查看个人信息、查找同事 open_id 或联系方式、按姓名搜索员工、查询部门结构时使用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli contact --help"
---

# contact (v1)

**重要提示 — 开始前必须先使用 Read 工具读取 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，其中包含认证、权限处理**

## 快捷操作（推荐优先使用）

快捷操作是对常用操作的高级封装（`lark-cli contact +<verb> [flags]`）。有快捷操作时优先使用。

| 快捷操作 | 说明 |
|----------|------|
| [`+search-user`](references/lark-contact-search-user.md) | 搜索用户（结果按相关性排序） |
| [`+get-user`](references/lark-contact-get-user.md) | 获取用户信息（省略 user_id 表示获取当前用户信息；提供 user_id 可获取指定用户信息） |