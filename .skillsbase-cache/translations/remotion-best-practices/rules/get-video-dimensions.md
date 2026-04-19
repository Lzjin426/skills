---
name: get-video-dimensions
description: 使用 Mediabunny 获取视频文件的宽度和高度
metadata:
  tags: 尺寸, 宽度, 高度, 分辨率, 大小, 视频
---

# 使用 Mediabunny 获取视频尺寸

Mediabunny 可以提取视频文件的宽度和高度。它适用于浏览器、Node.js 和 Bun 环境。

## 获取视频尺寸

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getVideoDimensions = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const videoTrack = await input.getPrimaryVideoTrack();
  if (!videoTrack) {
    throw new Error("No video track found");
  }

  return {
    width: videoTrack.displayWidth,
    height: videoTrack.displayHeight,
  };
};
```

## 使用方法

```tsx
const dimensions = await getVideoDimensions("https://remotion.media/video.mp4");
console.log(dimensions.width);  // 例如 1920
console.log(dimensions.height); // 例如 1080
```

## 使用本地文件

对于本地文件，请使用 `FileSource` 替代 `UrlSource`：

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // 来自输入或拖放的文件对象
});

const videoTrack = await input.getPrimaryVideoTrack();
const width = videoTrack.displayWidth;
const height = videoTrack.displayHeight;
```

## 在 Remotion 中使用 staticFile

```tsx
import { staticFile } from "remotion";

const dimensions = await getVideoDimensions(staticFile("video.mp4"));
```