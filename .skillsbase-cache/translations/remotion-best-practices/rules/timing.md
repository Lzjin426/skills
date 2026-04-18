---
name: timing
description: Remotion 中的插值曲线 - 线性、缓动、弹簧动画
metadata:
  tags: spring, bounce, easing, interpolation
---

简单的线性插值可通过 `interpolate` 函数实现。

```ts title="在 100 帧内从 0 过渡到 1"
import {interpolate} from 'remotion';

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

默认情况下，数值不会被限制在 [0, 1] 范围内，因此可能超出该区间。  
以下是如何限制数值范围的方法：

```ts title="在 100 帧内从 0 过渡到 1，并限制外推范围"
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: 'clamp',
  extrapolateLeft: 'clamp',
});
```

## 弹簧动画

弹簧动画具有更自然的运动效果。  
它们会随时间从 0 过渡到 1。

```ts title="在 100 帧内从 0 到 1 的弹簧动画"
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();
const {fps} = useVideoConfig();

const scale = spring({
  frame,
  fps,
});
```

### 物理属性

默认配置为：`mass: 1, damping: 10, stiffness: 100`。  
这会使动画在稳定前带有轻微的弹跳效果。

可按如下方式覆盖配置：

```ts
const scale = spring({
  frame,
  fps,
  config: {damping: 200},
});
```

推荐的无弹跳自然运动配置为：`{ damping: 200 }`。

以下是一些常见配置：

```tsx
const smooth = {damping: 200}; // 平滑，无弹跳（用于微妙的揭示效果）
const snappy = {damping: 20, stiffness: 200}; // 敏捷，轻微弹跳（用于 UI 元素）
const bouncy = {damping: 8}; // 弹跳式入场（用于活泼的动画）
const heavy = {damping: 15, stiffness: 80, mass: 2}; // 沉重、缓慢、轻微弹跳
```

### 延迟

默认情况下，动画会立即开始。  
使用 `delay` 参数可将动画延迟指定帧数。

```tsx
const entrance = spring({
  frame: frame - ENTRANCE_DELAY,
  fps,
  delay: 20,
});
```

### 持续时间

`spring()` 的持续时间基于物理属性自然确定。  
若要将动画拉伸至特定时长，可使用 `durationInFrames` 参数。

```tsx
const spring = spring({
  frame,
  fps,
  durationInFrames: 40,
});
```

### 结合 spring() 与 interpolate()

将弹簧输出（0-1）映射到自定义范围：

```tsx
const springProgress = spring({
  frame,
  fps,
});

// 映射到旋转角度
const rotation = interpolate(springProgress, [0, 1], [0, 360]);

<div style={{rotate: rotation + 'deg'}} />;
```

### 叠加弹簧效果

弹簧函数返回数值，因此可进行数学运算：

```tsx
const frame = useCurrentFrame();
const {fps, durationInFrames} = useVideoConfig();

const inAnimation = spring({
  frame,
  fps,
});
const outAnimation = spring({
  frame,
  fps,
  durationInFrames: 1 * fps,
  delay: durationInFrames - 1 * fps,
});

const scale = inAnimation - outAnimation;
```

## 缓动

可在 `interpolate` 函数中添加缓动效果：

```ts
import {interpolate, Easing} from 'remotion';

const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

默认缓动函数为 `Easing.linear`。  
其他凸度类型包括：

- `Easing.in`：启动缓慢，逐渐加速
- `Easing.out`：启动快速，逐渐减速
- `Easing.inOut`

以及曲线类型（按从最线性到最弯曲排序）：

- `Easing.quad`
- `Easing.sin`
- `Easing.exp`
- `Easing.circle`

缓动函数需结合凸度与曲线类型：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

也支持三次贝塞尔曲线：

```ts
const value1 = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```