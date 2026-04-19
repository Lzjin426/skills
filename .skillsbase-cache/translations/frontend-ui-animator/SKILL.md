---
name: frontend-ui-animator
description: 为 Next.js + Tailwind + React 项目分析和实现有目的的 UI 动画。当用户要求添加动画、增强 UI 动效、为页面/组件添加动画或改进视觉反馈时使用。触发词包括“添加动画”、“UI 动画”、“动效设计”、“悬停效果”、“滚动动画”、“页面过渡”、“微交互”。
---

# 前端 UI 动画师

实现有目的、高性能的动画，以增强用户体验而不致使用户感到负担。重点关注关键场景：首屏介绍、悬停反馈、内容展现和导航过渡。

## 核心理念

**“你不需要处处使用动画”** – 优先级排序：

| 优先级 | 领域 | 目的 |
|----------|------|---------|
| 1 | 首屏介绍 | 第一印象，品牌个性 |
| 2 | 悬停交互 | 反馈，可发现性 |
| 3 | 内容展现 | 引导注意力，降低认知负荷 |
| 4 | 背景效果 | 氛围，深度感 |
| 5 | 导航过渡 | 空间感知，连续性 |

## 工作流程

按顺序执行各阶段。完成前一阶段后再进入下一阶段。

### 阶段 1：分析

1. **扫描项目结构** – 识别 `app/` 中的所有页面和 `components/` 中的所有组件
2. **检查现有设置** – 查看 `tailwind.config.ts` 中已有的动画/关键帧
3. **识别动画候选对象** – 按优先级类别列出组件
4. **记录约束条件** – 注意已安装的动画库（如 framer-motion 等）

输出：动画审计表。参见 `references/component-checklist.md`。

### 阶段 2：规划

1. **将动画映射到组件** – 分配具体的动画模式
2. **确定触发条件** – 加载、滚动（交叉观察）、悬停、点击
3. **估算工作量** – 低（仅 CSS）、中（需要钩子）、高（需要库）
4. **提出分阶段推出计划** – 先实现快速见效的部分

输出：包含组件 → 动画映射的实现计划。

### 阶段 3：实现

1. **扩展 Tailwind 配置** – 添加关键帧和动画工具类
2. **添加减少动画支持** – 优先考虑无障碍性
3. **创建可复用的钩子** – 如需要，创建 `useScrollReveal`、`useMousePosition`
4. **按组件应用动画** – 遵循 `references/animation-patterns.md` 中的模式

**性能规则：**
```tsx
// ✅ 正确做法：仅使用变换和透明度
transform: translateY(20px);
opacity: 0.5;
filter: blur(4px);

// ❌ 错误做法：动画化布局属性
margin-top: 20px;
height: 100px;
width: 200px;
```

### 阶段 4：验证

1. 在浏览器中测试 – 对所有动画进行视觉质量检查
2. 测试减少动画 – 验证 `prefers-reduced-motion` 是否生效
3. 检查 CLS – 动画不应导致布局偏移
4. 性能审计 – 滚动动画不应出现卡顿

## 快速参考

### 动画触发条件

| 触发条件 | 实现方式 |
|---------|----------------|
| 页面加载 | 使用 CSS `animation` 和 `animation-delay` 实现错开效果 |
| 滚动进入视图 | `IntersectionObserver` 或 `react-intersection-observer` |
| 悬停 | Tailwind `hover:` 工具类或 CSS `:hover` |
| 点击/轻触 | 使用 `useState` 驱动状态变化 |

### 常见模式

**错开子元素动画：**
```tsx
{items.map((item, i) => (
  <div 
    key={item.id}
    style={{ animationDelay: `${i * 100}ms` }}
    className="animate-fade-slide-in"
  />
))}
```

**滚动展现钩子：**
```tsx
const useScrollReveal = (threshold = 0.1) => {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setIsVisible(true),
      { threshold }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [threshold]);

  return { ref, isVisible };
};
```

**用法：**
```tsx
const { ref, isVisible } = useScrollReveal();
<div ref={ref} className={isVisible ? 'animate-fade-in' : 'opacity-0'} />
```

## 资源

- **动画模式**：参见 `references/animation-patterns.md`
- **审计模板**：参见 `references/component-checklist.md`
- **Tailwind 预设**：参见 `references/tailwind-presets.md`

## 技术栈

- **CSS 动画**：默认用于简单效果
- **Tailwind 工具类**：用于悬停状态和基本动画
- **Framer Motion**：用于复杂编排、手势、布局动画
- **GSAP**：用于基于时间线的序列（如果已安装）

## 无障碍性（必需）

始终在全局 CSS 中包含：
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```