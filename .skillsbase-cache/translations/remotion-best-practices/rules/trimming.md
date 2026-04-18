---
name: trimming
description: Remotion 剪辑模式 - 裁剪动画的开头或结尾
metadata:
  tags: sequence, trim, clip, cut, offset
---

使用带负值 `from` 的 `<Sequence>` 来裁剪动画的开头。

## 裁剪开头

负值的 `from` 会将时间向前推移，使动画从中间开始播放：

```tsx
import { Sequence, useVideoConfig } from "remotion";

const fps = useVideoConfig();

<Sequence from={-0.5 * fps}>
  <MyAnimation />
</Sequence>
```

动画从第 15 帧开始出现——前 15 帧被裁剪掉。
在 `<MyAnimation>` 内部，`useCurrentFrame()` 从 15 开始计数，而不是 0。

## 裁剪结尾

使用 `durationInFrames` 在指定时长后卸载内容：

```tsx

<Sequence durationInFrames={1.5 * fps}>
  <MyAnimation />
</Sequence>
```

动画播放 45 帧后，组件将被卸载。

## 裁剪与延迟

嵌套序列可以同时裁剪开头并延迟显示时机：

```tsx
<Sequence from={30}>
  <Sequence from={-15}>
    <MyAnimation />
  </Sequence>
</Sequence>
```

内层序列裁剪开头的 15 帧，外层序列将结果延迟 30 帧显示。