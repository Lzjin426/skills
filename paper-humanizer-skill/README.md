# Paper Humanizer Skill

中英文学术文本润色与人性化Skill，用于去除 AI 生成的痕迹，同时严格保持事实准确性。

## ✨ 主要功能

- 🎯 **去除 AI 痕迹**：识别并移除常见的 AI 写作模式
- 📚 **学术语气优化**：保持学术严谨性，提升文本自然度
- 🔒 **事实严格保护**：绝不编造数据、篡改数值或改变实验结论
- 🌍 **双语支持**：完整支持中文和英文学术写作
- ⚙️ **高度可配置**：多种参数配置，适应不同写作风格

## 🚀 快速开始

### 作为 Claude Code Skill 使用

#### 安装步骤

```bash
# 从 GitHub 克隆仓库
git clone https://github.com/crabin/paper-humanizer-skill.git /tmp/paper-humanizer-skill

# 创建 skills 目录（如果不存在）
mkdir -p ~/.claude/skills/

# 复制到 skills 目录
cp -r /tmp/paper-humanizer-skill ~/.claude/skills/paper-humanizer

# 验证安装
ls ~/.claude/skills/paper-humanizer/
```

#### 使用

在对话中直接使用，系统会采用**两阶段交互**：

1. 先输出 AI 特征分析、优化策略和下一步询问；
2. 你确认处理方式后，AI 再按你的选择继续（全文输出、逐章修改、局部修改或 Diff 模式）。

这样可避免长论文一次性输出全文导致的长时间等待。

### 命令行脚本使用

```bash
# 处理文本文件
python3 scripts/paper_humanizer.py --text-file input.txt --language auto

# 生成组合提示词供外部使用
python3 scripts/paper_humanizer.py --text-file input.txt --out prompt.md

# 从标准输入读取
cat input.txt | python3 scripts/paper_humanizer.py --language zh
```

## 📋 参数配置

### 基础参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--language` | auto/zh/en | auto | 文本语言（自动检测/中文/英文） |
| `--tone` | formal/semi-formal/concise/persuasive | formal | 写作语气风格 |
| `--field` | string | computer science | 研究领域（用于保持术语一致性） |
| `--audience` | string | academic | 目标读者群体 |

### 约束控制

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--strict-factuality` | flag | True | 严格保持事实性（不篡改数据） |
| `--no-strict-factuality` | flag | False | 允许适度调整表达 |
| `--keep-citations` | flag | True | 保留引用标记 [1], (Smith, 2023) |
| `--drop-citations` | flag | False | 移除引用标记 |
| `--blacklist-level` | low/medium/high | high | AI 痍迹短语过滤级别 |

## 📝 两阶段输出格式

本 Skill 采用**两阶段交互**设计，避免长论文一次性输出全文导致等待时间过长：

### 第一阶段：分析 + 询问

系统先输出以下内容，**不输出完整润色后的文章**：

```
1. 原文 AI 特征分析：
   - 识别 2-3 个主要 AI 模式问题

2. 核心优化策略：
   - 列出 3-5 个针对性优化策略

3. 优化亮点说明：
   - 突出 1-2 个代表性修改（可选）

4. 下一步行动：
   请告诉我你希望如何继续处理这篇论文（可直接回复编号或描述）：
   1. 全文输出：一次性输出完整润色后的文章
   2. 逐章修改：按章节逐段输出，每章完成后暂停等你确认
   3. 局部修改：只修改你指定的某一段或某几段
   4. Diff 模式：不输出全文，只给出关键改动的对照
```

### 第二阶段：按用户选择执行

用户确认后，AI 根据选择进入对应模式：

| 用户选择 | AI 行为 |
| --- | --- |
| 全文输出 | 一次性输出 `4. 优化后的文章：完整润色后的文本` |
| 逐章修改 | 输出 `4. 优化后的文章 — 第 X 章：`，完成后询问是否继续 |
| 局部修改 | 仅输出指定段落的润色结果 |
| Diff 模式 | 输出原文与建议的对比片段及修改理由 |

这样你可以先判断 AI 的分析是否合理，再决定是否让它继续修改，避免无效长输出。

## 🎯 核心原则

### 不可协商的约束

- ❌ **绝不编造**新的事实、结果、指标或参考文献
- ❌ **绝不改变**任何数值、超参数、阈值或对比结果
- ✅ **保留所有**引用标记（如 [1]、(Smith, 2023)、\cite{...}）
- ✅ **保持术语**在目标领域的一致性

### 去除的 AI 痕迹

**中文常见 AI 痕迹：**
- "值得注意的是"、"不难发现"、"基于以上分析"
- "综上所述"、"首先/其次/最后"、"本文将"
- "在一定程度上"、"显著提升"（无量化支撑时）
- "具有重要意义"、"此外"、"同时"（过度使用时）

**英文常见 AI 痕迹：**
- "It is worth noting that"、"It can be seen that"
- "In summary"、"Firstly, Secondly, Finally"
- "This paper aims to"、"To some extent"
- "Significantly improves"（无证据时）

完整列表见 `references/phrase_blacklist.md`

## 📖 使用示例

### 中文示例

**输入：**
```
值得注意的是，本文将提出一种基于WGAN-GP的改进方法，
并在NSL-KDD数据集上进行了实验。实验结果表明，该方法
在准确率上有显著提升。综上所述，本方法具有重要意义。
```

**第一阶段输出（分析 + 询问）：**
```
1. 原文 AI 特征分析：
   - 模式词堆砌：「值得注意的是」「本文将」「综上所述」
   - 空泛结论：「显著提升」「具有重要意义」缺乏量化支撑
   - 主语冗余：「本文将提出」可简化为主动宾结构

2. 核心优化策略：
   - 删除模式词，改用直接陈述
   - 补充量化数据（如准确率提升 X%）
   - 将结论具体化到应用场景

3. 优化亮点说明：
   - 把「本文将提出一种基于WGAN-GP的改进方法」改为「本研究提出了一种基于 WGAN-GP 的改进方法」

4. 下一步行动：
   请告诉我你希望如何继续处理这篇论文（可直接回复编号或描述）：
   1. 全文输出：一次性输出完整润色后的文章
   2. 逐章修改：按章节逐段输出，每章完成后暂停等你确认
   3. 局部修改：只修改你指定的某一段或某几段
   4. Diff 模式：不输出全文，只给出关键改动的对照
```

**第二阶段输出（用户选择「全文输出」后）：**
```
4. 优化后的文章：
本研究提出了一种基于 WGAN-GP 的改进方法，并在 NSL-KDD
数据集上进行了验证。实验结果显示，该方法将准确率提升了
X%，表明该方法在网络安全入侵检测领域具有应用价值。
```

### 英文示例

**输入：**
```
It is worth noting that this paper aims to propose an improved
method based on WGAN-GP and conducts experiments on the NSL-KDD
dataset. The experimental results show that the method significantly
improves accuracy. In summary, the proposed method is of great significance.
```

**第一阶段输出（分析 + 询问）：**
```
1. 原文 AI 特征分析：
   - 模式词："It is worth noting that", "this paper aims to", "In summary"
   - 空泛结论："significantly improves", "of great significance" 缺乏量化支撑
   - 冗余主语："this paper aims to propose" 可直接用 "This study presents"

2. 核心优化策略：
   - Remove AI-isms and empty intensifiers
   - Add quantified results (e.g., X% accuracy improvement)
   - Make the conclusion specific to the application domain

3. 优化亮点说明：
   - Replace "It is worth noting that this paper aims to propose" with "This study presents"

4. 下一步行动：
   请告诉我你希望如何继续处理这篇论文（可直接回复编号或描述）：
   1. 全文输出：一次性输出完整润色后的文章
   2. 逐章修改：按章节逐段输出，每章完成后暂停等你确认
   3. 局部修改：只修改你指定的某一段或某几段
   4. Diff 模式：不输出全文，只给出关键改动的对照
```

**第二阶段输出（用户选择「全文输出」后）：**
```
4. 优化后的文章：
This study presents an improved WGAN-GP-based method, validated on
the NSL-KDD dataset. Results demonstrate a X% accuracy improvement,
indicating the method's practical value in network intrusion detection.
```

## 🧪 测试用例

以下两个测试用例可用于验证 skill 功能是否正常。

### 测试用例一：中文学术段落（含多种 AI 痕迹）

**输入文本**（来自 `examples/zh_input_rich.txt`）：
```
在当今人工智能技术迅猛发展的背景下，网络安全问题愈发凸显其重要性。值得注意的是，传统的入侵
检测系统在面对不断演变的网络攻击时，往往表现出明显的局限性。不难发现，现有方法在处理类别不
平衡数据集时存在诸多不足，严重制约了模型的泛化能力。

为了解决上述问题，本文旨在提出一种基于改进WGAN-GP的入侵检测方法。本文将深度学习与生成对抗
网络有机结合，充分发挥二者各自的优势，有效地、全面地解决了传统方法存在的不足之处。

综上所述，本文提出的方法不仅在技术层面实现了重要突破，更为入侵检测领域的发展提供了新的思路
和方向，具有重要的理论意义和实践价值。
```

**预期 AI 特征分析**：
- ❌ 模式词：「值得注意的是」「不难发现」「本文旨在」「综上所述」「有效地、全面地」「具有重要意义」
- ❌ 空洞套话：「充分发挥」「有机结合」「具有重要的理论意义和实践价值」
- ❌ 无量化支撑的「显著提升」「重要突破」

**预期优化结果示例**：
```
传统入侵检测系统难以应对持续演变的网络攻击，在类别不平衡数据集上的泛化能力尤为薄弱。
本研究提出一种基于改进 WGAN-GP 的入侵检测方法，将生成对抗网络与深度学习相结合，针对
类别不平衡问题进行专项优化。实验结果表明，该方法在 NSL-KDD 数据集上的准确率、召回率
和 F1 值均有提升，具体改进幅度见表2。
```

---

### 测试用例二：英文学术段落（含多种 AI 痕迹）

**输入文本**（来自 `examples/en_input_rich.txt`）：
```
In today's rapidly evolving digital landscape, cybersecurity threats are becoming increasingly
sophisticated. It is worth noting that traditional intrusion detection systems often struggle
to keep pace with the ever-changing nature of network attacks.

To address this issue, this paper aims to propose an innovative framework based on an improved
WGAN-GP architecture. Furthermore, the method holistically addresses the multifaceted challenges
of intrusion detection in a comprehensive and robust manner.

In conclusion, the proposed method represents a significant advancement in the field. Based on
the above analysis, it can be concluded that this work has far-reaching implications for
cybersecurity research and practice.
```

**预期 AI 特征分析**：
- ❌ 模式词：`It is worth noting that`、`this paper aims to`、`In conclusion`、`Based on the above analysis`
- ❌ 空洞修饰：`rapidly evolving landscape`、`holistically addresses the multifaceted challenges`、`comprehensive and robust`
- ❌ 无量化支撑的 `significant advancement`、`far-reaching implications`

**预期优化结果示例**：
```
Traditional intrusion detection systems struggle to adapt to evolving network attacks, particularly
under class-imbalanced conditions. This work proposes an improved WGAN-GP framework that directly
targets class imbalance in intrusion detection. On the NSL-KDD dataset, the method achieves
improvements in accuracy, recall, and F1 score over existing baselines (see Table 2), suggesting
practical applicability in real-world cybersecurity deployments.
```

---

## 📂 项目结构

```
paper-humanizer/
├── README.md                      # 本文档
├── SKILL.md                       # Skill 元数据定义
├── references/                    # 参考文档
│   ├── system_prompt.md           # 系统提示词（核心编辑原则）
│   ├── user_template.md           # 用户提示词模板
│   └── phrase_blacklist.md        # AI 痕迹短语黑名单
├── scripts/                       # 脚本工具
│   ├── paper_humanizer.py         # Python CLI 工具
│   └── paper_humanizer.sh         # Bash 包装脚本
└── examples/                      # 使用示例
    ├── zh_input.txt               # 中文简单示例输入
    ├── zh_input_rich.txt          # 中文完整段落示例（含 6+ AI 痕迹）
    ├── en_input.txt               # 英文简单示例输入
    ├── en_input_rich.txt          # 英文完整段落示例（含 8+ AI 痕迹）
    └── run_demo.sh                # 演示脚本
```

## ⚠️ 注意事项

1. **事实性保护**：如检测到原文存在矛盾或歧义，会在"核心优化策略"部分提出中性建议，而非直接修改文本
2. **技术术语**：保持技术术语原样（如 GAN、WGAN-GP、NSL-KDD），除非上下文要求标准翻译
3. **语言保持**：输出语言与输入保持一致，除非用户明确要求翻译
4. **引用标记**：默认保留所有引用标记，可通过 `--drop-citations` 参数移除

## 🔧 高级配置

### 领域特定术语

通过 `--field` 参数指定研究领域，系统会：
- 保持该领域的术语一致性
- 使用符合领域惯例的表达方式
- 保留特定缩写和专业词汇

### 语气风格选择

- `formal`：正式学术写作（论文、期刊投稿）
- `semi-formal`：半正式（技术报告、博客）
- `concise`：简洁风格（摘要、总结）
- `persuasive`：说服性风格（申请材料、项目书）

## 📚 相关文档

- `references/system_prompt.md` - 完整编辑原则和约束条件
- `references/phrase_blacklist.md` - AI 痕迹短语完整列表
- `references/user_template.md` - 参数化提示词模板
- `SKILL.md` - Skill 元数据和快速参考

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可

本 skill 为学术辅助工具，请负责任地使用。优化后的文本仍需作者仔细校对。
