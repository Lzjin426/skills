# 用于动画的 clip-path

`clip-path` 是 CSS 中最强大的动画工具之一。它支持硬件加速，并能创造出仅靠 `opacity` 和 `transform` 无法实现的效果。

## 目录
- [inset 形状](#the-inset-shape)
- [标签颜色过渡](#tab-colour-transitions)
- [长按删除](#hold-to-delete)
- [滚动时图像显现](#image-reveals-on-scroll)
- [对比滑块](#comparison-sliders)

## inset 形状

`clip-path: inset(top right bottom left)` 定义了一个矩形裁剪区域。每个值从对应方向“切入”元素。

```css
/* 从右侧完全隐藏 */
.hidden { clip-path: inset(0 100% 0 0); }

/* 完全可见 */
.visible { clip-path: inset(0 0 0 0); }
```

通过 CSS 过渡在不同状态间进行动画：

```css
.reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 300ms cubic-bezier(0.22, 1, 0.36, 1);
}
.reveal.active {
  clip-path: inset(0 0 0 0);
}
```

## 标签颜色过渡

复制标签列表。将副本样式设为“激活”状态（不同背景、不同文字颜色）。裁剪副本，仅显示激活的标签。在标签切换时对裁剪区域进行动画。

这能创造出无缝的颜色过渡效果，而单独对 `color` 进行过渡动画永远无法实现。

```css
.tabs-active-overlay {
  clip-path: inset(0 var(--clip-right) 0 var(--clip-left));
  transition: clip-path 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
```

当激活标签改变时，通过 JavaScript 更新 `--clip-left` 和 `--clip-right`。

## 长按删除

在彩色遮罩层上使用 `clip-path: inset(0 100% 0 0)`。在 `:active` 状态下，以 `linear` 缓动在 2 秒内过渡到 `inset(0 0 0 0)`。释放时，以 200 毫秒的 `ease-out` 缓动快速恢复。同时配合按钮上的 `scale(0.97)` 来提供按压反馈。

```css
.delete-overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms ease-out;
}

.delete-button:active .delete-overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;
}
```

## 滚动时图像显现

初始状态为 `clip-path: inset(0 0 100% 0)`（从底部隐藏）。当元素进入视口时，动画过渡到 `inset(0 0 0 0)`。

```tsx
"use client";
import { useRef, useEffect, useState } from "react";

export function RevealImage({ src, alt }: { src: string; alt: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisible(true); },
      { threshold: 0.1, rootMargin: "-100px" }
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      style={{
        clipPath: visible ? "inset(0 0 0 0)" : "inset(0 0 100% 0)",
        transition: "clip-path 800ms cubic-bezier(0.77, 0, 0.175, 1)",
      }}
    >
      <img src={src} alt={alt} />
    </div>
  );
}
```

## 对比滑块

将两张图像叠加。使用 `clip-path: inset(0 50% 0 0)` 裁剪顶部图像。根据拖拽位置调整右侧的 inset 值。无需额外的 DOM 元素，完全由硬件加速。

```css
.comparison-top {
  clip-path: inset(0 var(--split) 0 0);
}
```

通过滑块手柄上的指针事件更新 `--split`。