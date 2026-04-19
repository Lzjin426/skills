---
name: gif
description: 在 Remotion 中显示 GIF、APNG、AVIF 和 WebP 图像
metadata:
  tags: gif, 动画, 图像, 动态图, apng, avif, webp
---

# 在 Remotion 中使用动态图像

## 基本用法

使用 `<AnimatedImage>` 来显示 GIF、APNG、AVIF 或 WebP 图像，并与 Remotion 的时间线同步：

```tsx
import {AnimatedImage, staticFile} from 'remotion';

export const MyComposition = () => {
  return <AnimatedImage src={staticFile('animation.gif')} width={500} height={500} />;
};
```

也支持远程 URL（必须启用 CORS）：

```tsx
<AnimatedImage src="https://example.com/animation.gif" width={500} height={500} />
```

## 尺寸与适配

通过 `fit` 属性控制图像如何填充其容器：

```tsx
// 拉伸以填充（默认）
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="fill" />

// 保持宽高比，适应容器内部
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="contain" />

// 填充容器，必要时裁剪
<AnimatedImage src={staticFile("animation.gif")} width={500} height={300} fit="cover" />
```

## 播放速度

使用 `playbackRate` 控制动画速度：

```tsx
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} playbackRate={2} /> {/* 2倍速 */}
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} playbackRate={0.5} /> {/* 半速 */}
```

## 循环行为

控制动画结束时的行为：

```tsx
// 无限循环（默认）
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="loop" />

// 播放一次，显示最后一帧
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="pause-after-finish" />

// 播放一次，然后清空画布
<AnimatedImage src={staticFile("animation.gif")} width={500} height={500} loopBehavior="clear-after-finish" />
```

## 样式

使用 `style` 属性添加额外的 CSS（使用 `width` 和 `height` 属性设置尺寸）：

```tsx
<AnimatedImage
  src={staticFile('animation.gif')}
  width={500}
  height={500}
  style={{
    borderRadius: 20,
    position: 'absolute',
    top: 100,
    left: 50,
  }}
/>
```

## 获取 GIF 时长

使用 `@remotion/gif` 中的 `getGifDurationInSeconds()` 来获取 GIF 的时长。

```bash
npx remotion add @remotion/gif # 如果项目使用 npm
bunx remotion add @remotion/gif # 如果项目使用 bun
yarn remotion add @remotion/gif # 如果项目使用 yarn
pnpm exec remotion add @remotion/gif # 如果项目使用 pnpm
```

```tsx
import {getGifDurationInSeconds} from '@remotion/gif';
import {staticFile} from 'remotion';

const duration = await getGifDurationInSeconds(staticFile('animation.gif'));
console.log(duration); // 例如 2.5
```

这对于将合成时长设置为与 GIF 匹配非常有用：

```tsx
import {getGifDurationInSeconds} from '@remotion/gif';
import {staticFile, CalculateMetadataFunction} from 'remotion';

const calculateMetadata: CalculateMetadataFunction = async () => {
  const duration = await getGifDurationInSeconds(staticFile('animation.gif'));
  return {
    durationInFrames: Math.ceil(duration * 30),
  };
};
```

## 替代方案

如果 `<AnimatedImage>` 无法工作（仅支持 Chrome 和 Firefox），可以使用 `@remotion/gif` 中的 `<Gif>` 组件。

```bash
npx remotion add @remotion/gif # 如果项目使用 npm
bunx remotion add @remotion/gif # 如果项目使用 bun
yarn remotion add @remotion/gif # 如果项目使用 yarn
pnpm exec remotion add @remotion/gif # 如果项目使用 pnpm
```

```tsx
import {Gif} from '@remotion/gif';
import {staticFile} from 'remotion';

export const MyComposition = () => {
  return <Gif src={staticFile('animation.gif')} width={500} height={500} />;
};
```

`<Gif>` 组件具有与 `<AnimatedImage>` 相同的属性，但仅支持 GIF 文件。