---
name: charts
description: Remotion 的图表与数据可视化模式。适用于创建条形图、饼图、直方图、进度条或任何数据驱动的动画。
metadata:
  tags: 图表, 数据, 可视化, 条形图, 饼图, 图形
---

# Remotion 中的图表

你可以使用常规的 React 代码在 Remotion 中创建条形图——允许使用 HTML 和 SVG，也可以使用 D3.js。

## 禁用非由 `useCurrentFrame()` 驱动的动画

请禁用所有第三方库的动画效果。  
它们会在渲染过程中导致闪烁。  
相反，所有动画都应通过 `useCurrentFrame()` 来驱动。

## 条形图动画

查看 [条形图示例](assets/charts/bar-chart.tsx) 获取基础实现示例。

### 错开显示的条形

你可以像这样为条形的高度添加动画并实现错开效果：

```tsx
const STAGGER_DELAY = 5;
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const bars = data.map((item, i) => {
  const delay = i * STAGGER_DELAY;
  const height = spring({
    frame,
    fps,
    delay,
    config: {damping: 200},
  });
  return <div style={{height: height * item.value}} />;
});
```

## 饼图动画

使用 stroke-dashoffset 为扇区添加动画，从 12 点钟方向开始。

```tsx
const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const progress = interpolate(frame, [0, 100], [0, 1]);

const circumference = 2 * Math.PI * radius;
const segmentLength = (value / total) * circumference;
const offset = interpolate(progress, [0, 1], [segmentLength, 0]);

<circle r={radius} cx={center} cy={center} fill="none" stroke={color} strokeWidth={strokeWidth} strokeDasharray={`${segmentLength} ${circumference}`} strokeDashoffset={offset} transform={`rotate(-90 ${center} ${center})`} />;
```