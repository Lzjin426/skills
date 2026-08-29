---
name: paperbanana
description: 将论文方法、图注或研究构想转为 NeurIPS、ICML、ACL 等风格的学术机制图、方法总览图和架构图。用于用户要求根据论文内容规划、生成、审阅或迭代学术示意图时。采用聊天驱动工作流：Codex 负责检索、规划、风格化和视觉审阅，最终图片通过 APINebula 的 Nano Banana 2（gemini-3.1-flash-image）生成。
---

# PaperBanana

将 PaperBanana 的五个角色保留为聊天中的工作顺序，而不是在本地重复调用另一套模型：

1. **Retriever**：必要时找目标领域或目标会议的真实图例与术语。
2. **Planner**：将方法拆成主张、输入、核心模块、数据/控制流、输出和面板层级。
3. **Stylist**：默认采用干净的 NeurIPS / ICML / ACL 方法图语言：白底、扁平或近矢量形状、克制配色、直接标签、明确的流向与视觉主次。
4. **Visualizer**：在用户确认生成后，用 `scripts/generate_apinebula_nanobanana.py` 调用 APINebula 的 `gemini-3.1-flash-image`。
5. **Critic**：读取成图，核对原始方法、箭头关系、标签、可读性、信息密度和是否出现伪造数据；不通过则用局部、明确的改图指令重生成。

## 生成前

先写出简短图稿合同：核心结论、图类型、目标读者/期刊、版式、必须出现的实体及连线、禁止出现的内容。对于真实数据图，使用 `nature-figure` 的 Python/R 路线；本 skill 仅负责机制图、算法图、系统架构图、研究流程与图形摘要草稿。

将用户提供的方法文本和图注转成一条英文生成提示词。强制说明：布局方向、模块间精确关系、颜色语义、最多需要的短标签、白底/充足留白，以及“不虚构数值、曲线、实验结果、机构标识或未支持的机制”。复杂图先产出一个主叙事，不要把每个细节塞进同一画面。

## APINebula 生成

仅在用户要求实际出图后调用：

```bash
python3 scripts/generate_apinebula_nanobanana.py \
  --prompt-file prompt.txt \
  --output outputs/figure.png \
  --aspect-ratio 16:9 \
  --image-size 2K
```

默认模型固定为 `gemini-3.1-flash-image`。脚本优先读取 `APINEBULA_API_KEY`，再读取同级 `apinebula-gpt-image` skill 的私有 `.api_key`；密钥绝不写入提示词、输出目录、代码、Git 或命令输出。调用会将提示词发送至 APINebula，未公开的论文内容须先取得用户许可。

先用 `--dry-run` 检查请求载荷；再进行付费调用。模型的文字与箭头不能视为最终定稿：对投稿图必须逐项人工核对，必要时在 SVG、Illustrator、Inkscape 或 PowerPoint 中重绘文字与连接线。

## 上游启动器

保留的 `run.py` 是原始 PaperBanana 的独立多模型启动器，依赖 OpenRouter/Google 的内部智能体调用。当前配置下不要调用它；聊天中的 Codex 已承担这些推理与审阅步骤，避免重复付费和不可控的双重规划。
