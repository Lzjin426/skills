---
name: ui-animation
description: 负责创建、评审和调试用户界面动效与动画实现。涵盖弹簧动画、手势、拖拽交互、裁剪路径揭示、缓动、时序及动画评审。适用于设计、实现或评审动效、CSS过渡、关键帧、framer-motion、弹簧动画，或当需要处理“添加动画”、“让交互更流畅”、“评审我的动画”、“这里是否需要动画”或“添加滑动手势”等需求时使用。
---

# UI 动画

## 参考文件

| 文件 | 阅读时机 |
|---|---|
| [references/decision-framework.md](references/decision-framework.md) | 默认：动画决策、缓动与时长 |
| [references/spring-animations.md](references/spring-animations.md) | 使用弹簧物理、framer-motion useSpring、配置弹簧参数 |
| [references/component-patterns.md](references/component-patterns.md) | 构建带动画的按钮、弹出框、工具提示、抽屉、模态框、通知 |
| [references/clip-path-techniques.md](references/clip-path-techniques.md) | 使用 clip-path 实现揭示效果、标签页、长按删除、对比滑块 |
| [references/gesture-drag.md](references/gesture-drag.md) | 实现拖拽、滑动关闭、动量、指针捕获 |
| [references/performance-deep-dive.md](references/performance-deep-dive.md) | 调试卡顿、CSS 与 JS 对比、WAAPI、CSS 变量陷阱、Framer Motion 注意事项 |
| [references/review-format.md](references/review-format.md) | 评审动画代码——使用“前/后/原因”表格与问题清单 |

## 核心规则

- 为反馈、引导、连续性或刻意营造愉悦感而添加动画。
- 切勿为键盘触发的操作（快捷键、箭头导航、Tab/焦点切换）添加动画。
- 对于可中断的 UI，优先使用 CSS 过渡；关键帧仅用于预定义序列。
- 优先级：CSS 过渡 > WAAPI > CSS 关键帧 > JS（requestAnimationFrame）。
- 确保动画可中断且由输入驱动。
- 非对称时序：进入可稍慢；退出应迅速。
- 使用 `@starting-style` 实现 DOM 进入动画；回退方案为 `data-mounted`。
- 轻微的 `filter: blur(2px)` 可掩盖粗糙的交叉淡入淡出。

## 应动画化的属性

- 位移：仅限 `transform` 和 `opacity`。
- 状态反馈：`color`、`background-color` 和 `opacity` 可接受。
- 切勿动画化布局属性（`width`、`height`、`top`、`left`）；切勿使用 `transition: all`。
- 避免为核心交互动画化 `filter`；如不可避免，模糊度保持 ≤ 20px。
- SVG：在 `<g>` 包装器上应用变换，并设置 `transform-box: fill-box; transform-origin: center`。
- 在主题切换期间禁用过渡（`[data-theme-switching] * { transition: none !important }`）。

## 缓动默认值

| 元素 | 时长 | 缓动 |
|---|---|---|
| 按钮按下反馈 | 100–160ms | `cubic-bezier(0.22, 1, 0.36, 1)` |
| 工具提示、小型弹出框 | 125–200ms | `ease-out` 或进入曲线 |
| 下拉菜单、选择框 | 150–250ms | `cubic-bezier(0.22, 1, 0.36, 1)` |
| 模态框、抽屉 | 200–350ms | `cubic-bezier(0.22, 1, 0.36, 1)` |
| 屏幕内移动/滑动 | 200–300ms | `cubic-bezier(0.25, 1, 0.5, 1)` |
| 简单悬停（颜色/透明度） | 200ms | `ease` |
| 示意性/营销动画 | 最长 1000ms | 弹簧或自定义曲线 |

**命名曲线**
- **进入：** `cubic-bezier(0.22, 1, 0.36, 1)` —— 用于入场和基于变换的悬停
- **移动：** `cubic-bezier(0.25, 1, 0.5, 1)` —— 用于滑动、抽屉、面板
- **抽屉（类 iOS 风格）：** `cubic-bezier(0.32, 0.72, 0, 1)`

UI 中避免使用 `ease-in`。优先使用 [easing.dev](https://easing.dev/) 的自定义曲线。

## 空间与序列

- 为弹出框在触发点设置 `transform-origin`；模态框保持 `center`。
- 对于对话框/菜单，起始缩放约为 `scale(0.85–0.9)`。切勿使用 `scale(0)`。
- 逐项揭示的延迟间隔为 30–50ms；总延迟不超过 300ms。

## 可访问性

- 将悬停动画限制在 `@media (hover: hover) and (pointer: fine)` 后，以避免触控设备误触发。
- 在直接操作期间，保持元素锁定于指针。仅在释放后添加缓动。

## 性能

- 仅动画化 `transform` 和 `opacity` —— 这些属性跳过布局和绘制。
- 使用 `IntersectionObserver` 在元素离开屏幕时暂停循环动画。
- 仅在重度运动期间为 `transform`/`opacity` 切换 `will-change` —— 结束后移除。
- 不要使用 CSS 变量动画化拖拽手势（会触发所有子元素重新计算）。
- Motion 的 `x`/`y` 值是轴移动和拖拽的常规选择。当需要单一变换所有者以组合变换或实现互操作时，使用完整的 `transform` 字符串。
- 关于 WAAPI、合成层及 CSS 与 JS 对比，请参阅 [references/performance-deep-dive.md](references/performance-deep-dive.md)。

## 反模式

- `transition: all` —— 触发布局重计算并动画化非预期属性。
- 为交互反馈动画化布局属性（`width`、`height`、`top`、`left`）。
- 在 UI 入场时使用 `ease-in` —— 感觉迟滞。
- 从 `scale(0)` 开始动画 —— 现实世界中无物凭空出现。使用 `scale(0.85–0.95)`。
- 在无用户触发时于挂载时动画化 —— 意外的动效会令人迷失方向。
- 永久设置 `will-change` —— 仅在重度运动期间切换它。
- 使用 CSS 变量进行拖拽手势动画 —— 每帧都会重绘。
- 对称的进入/退出时序 —— 退出应更快（用户期望即时响应）。
- 拖拽边界处的硬停止 —— 改用摩擦/阻尼。
- 在同一元素上混合使用 Motion 的 `x`/`y` 属性与手写的 `transform` 字符串。
- 在频繁触发的元素上使用关键帧 —— 使用 CSS 过渡以保证可中断性。

## 工作流程

复制并跟踪此清单：

```text
动画进度：
- [ ] 步骤 1：决定交互是否应动画化
- [ ] 步骤 2：选择目的、缓动和时长
- [ ] 步骤 3：选择实现方式
- [ ] 步骤 4：加载相关组件或技术参考
- [ ] 步骤 5：验证时序、中断和设备行为
```

1.  回答 [references/decision-framework.md](references/decision-framework.md) 中的四个问题：是否应动画化？目的是什么？使用何种缓动？速度如何？
2.  从上方的缓动默认值表中选择时长。
3.  选择实现方式：CSS 过渡 > WAAPI > 弹簧动画 > 关键帧 > JS。
4.  加载与你的组件类型或技术相关的参考文件。
5.  评审时，使用 [references/review-format.md](references/review-format.md) 中的“前/后/原因”表格格式。

## 验证

- 确认没有布局属性动画（`width`、`height`、`top`、`left`）。
- 检查循环动画在离开屏幕时是否暂停。
- 确认 `will-change` 仅在动画期间切换，而非永久设置。
- 快速重新切换组件，确认过渡能干净地重定向，而非从零重新开始。
- 在开发者工具中将动画速度降至 0.1x，以捕捉全速下不可见的时序问题。
- 录制并逐帧回放，以协调属性时序。
- 在真实设备（而非仅模拟器）上测试触控交互。