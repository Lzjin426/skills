---
name: sequencing
description: Remotion 的序列模式——延迟、修剪、限制项目时长
metadata:
  tags: 序列, 系列, 时序, 延迟, 修剪
---

使用 `<Sequence>` 来延迟元素在时间轴上的出现时机。

```tsx
import { Sequence } from "remotion";

const {fps} = useVideoConfig();

<Sequence from={1 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Title />
</Sequence>
<Sequence from={2 * fps} durationInFrames={2 * fps} premountFor={1 * fps}>
  <Subtitle />
</Sequence>
```

默认情况下，这会将组件包裹在一个绝对填充元素中。  
如果不需要包裹元素，请使用 `layout` 属性：

```tsx
<Sequence layout="none">
  <Title />
</Sequence>
```

## 预加载

这会在组件实际播放前将其加载到时间轴中。  
务必为所有 `<Sequence>` 启用预加载！

```tsx
<Sequence premountFor={1 * fps}>
  <Title />
</Sequence>
```

## 系列

当元素需要依次播放且不重叠时，使用 `<Series>`。

```tsx
import {Series} from 'remotion';

<Series>
  <Series.Sequence durationInFrames={45}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <MainContent />
  </Series.Sequence>
  <Series.Sequence durationInFrames={30}>
    <Outro />
  </Series.Sequence>
</Series>;
```

与 `<Sequence>` 类似，使用 `<Series.Sequence>` 时，除非将 `layout` 属性设为 `none`，否则项目默认会被包裹在绝对填充元素中。

### 带重叠的系列

使用负偏移量来实现重叠序列：

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>
    <SceneA />
  </Series.Sequence>
  <Series.Sequence offset={-15} durationInFrames={60}>
    {/* 在 SceneA 结束前 15 帧开始 */}
    <SceneB />
  </Series.Sequence>
</Series>
```

## 序列内的帧引用

在 Sequence 内部，`useCurrentFrame()` 返回的是局部帧数（从 0 开始）：

```tsx
<Sequence from={60} durationInFrames={30}>
  <MyComponent />
  {/* 在 MyComponent 内部，useCurrentFrame() 返回 0-29，而非 60-89 */}
</Sequence>
```

## 嵌套序列

序列可以嵌套以实现复杂的时序控制：

```tsx
<Sequence from={0} durationInFrames={120}>
  <Background />
  <Sequence from={15} durationInFrames={90} layout="none">
    <Title />
  </Sequence>
  <Sequence from={45} durationInFrames={60} layout="none">
    <Subtitle />
  </Sequence>
</Sequence>
```