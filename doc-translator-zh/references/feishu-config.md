# 飞书输出默认配置

本文件记录 doc-translator-zh Skill 的默认飞书输出位置。

## 默认目标文件夹

- **名称**：标准&论文
- **URL**：https://my.feishu.cn/drive/folder/BXaMfawkhlGHfTdIkaNcQhlRnWc
- **Token**：`BXaMfawkhlGHfTdIkaNcQhlRnWc`

当用户选择「生成飞书文档」且没有指定其他位置时，文档应创建到此文件夹下。

## 使用方式

创建飞书文档时，在 `lark-cli docs +create` 命令中加入：

```bash
--parent-token BXaMfawkhlGHfTdIkaNcQhlRnWc
```

示例：

```bash
lark-cli docs +create --api-version v2 \
  --parent-token BXaMfawkhlGHfTdIkaNcQhlRnWc \
  --content $'标题内容'
```

## 覆盖默认位置

如果用户明确要求放到其他文件夹，使用用户指定的位置，覆盖本默认值。
