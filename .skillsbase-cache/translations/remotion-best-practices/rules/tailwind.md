---
name: tailwind
description: 在 Remotion 中使用 TailwindCSS。
metadata:
---

如果项目中已安装 TailwindCSS，你可以在 Remotion 中使用且应当使用它。

请勿使用 `transition-*` 或 `animate-*` 类——始终通过 `useCurrentFrame()` 钩子来实现动画效果。

首先需要在 Remotion 项目中安装并启用 Tailwind——请通过 WebFetch 获取 https://www.remotion.dev/docs/tailwind 以查看详细说明。