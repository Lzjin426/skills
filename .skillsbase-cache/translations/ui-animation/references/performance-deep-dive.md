# 性能深度解析

超越 SKILL.md 中快速规则的进阶性能指南。

## 目录
- [CSS 与 JS 动画对比](#css-与-js-动画对比)
- [Web Animations API (WAAPI)](#web-animations-api-waapi)
- [CSS 变量继承陷阱](#css-变量继承陷阱)
- [Motion 变换所有权](#motion-变换所有权)
- [暂停屏幕外的循环动画](#暂停屏幕外的循环动画)
- [合成层与 will-change](#合成层与-will-change)
- [修复抖动的 1 像素偏移](#修复抖动的-1-像素偏移)

## CSS 与 JS 动画对比

| 方法 | 驱动方 | 可中断性 | 最佳适用场景 |
|---|---|---|---|
| CSS 过渡动画 | 浏览器/合成器（针对 transform/opacity） | 是（可重定向） | 预定义的状态变化 |
| CSS 关键帧动画 | 浏览器/合成器（当属性允许时） | 否（从零重新开始） | 循环动画、预定义序列 |
| WAAPI (`el.animate()`) | 浏览器动画引擎 | 是（可取消/反转） | 需要命令式控制的动态值 |
| Motion 值 (`x`, `y`, `style`) | Motion DOM 渲染器，无 React 重渲染 | 是 | React 手势、拖拽、协调的 UI |
| JS (`requestAnimationFrame`) | 主线程 | 是（手动控制） | 复杂编排、物理模拟 |

**规则：CSS 过渡动画 > WAAPI > CSS 关键帧动画 > JS。** 在高负载情况下（页面导航、大量渲染），CSS 动画保持流畅，而 JS 动画会掉帧。

## Web Animations API (WAAPI)

具备 CSS 性能的 JavaScript 控制。硬件加速、可中断、基于 Promise。

```ts
const animation = element.animate(
  [
    { transform: "translateY(100%)", opacity: 0 },
    { transform: "translateY(0)", opacity: 1 },
  ],
  {
    duration: 300,
    easing: "cubic-bezier(0.22, 1, 0.36, 1)",
    fill: "forwards",
  }
);

// 随时取消或反转
animation.reverse();
await animation.finished;
```

## CSS 变量继承陷阱

更改父元素上的 CSS 变量会触发**所有子元素**的样式重新计算。在一个包含许多项目的抽屉组件中，更新容器上的 `--swipe-amount` 会导致昂贵的样式重计算。

```ts
// 错误：触发所有子元素的重计算
element.style.setProperty("--swipe-amount", `${distance}px`);

// 正确：仅影响当前元素
element.style.transform = `translateY(${distance}px)`;
```

例外：使用 `@property` 并设置 `inherits: false` 可以避免级联影响，但浏览器支持有限。

## Motion 变换所有权

Motion 的 `x`/`y` 值是用于单轴移动和拖拽的一等 API。它们更新时不会触发 React 重渲染，是手势密集型组件的默认选择。

```tsx
const x = useMotionValue(0);

// 用于拖拽和轴移动的惯用 Motion API
<motion.div drag="x" style={{ x }} />

// 当需要编写多个变换函数或与非 Motion 代码交互时，
// 使用一个手写的 transform 字符串
<motion.div animate={{ transform: "translateX(100px) rotate(4deg)" }} />
```

不要在同一元素上混合使用 Motion 的 `x`/`y` 属性和单独手写的 `transform` 字符串。选择一个变换所有者。

## 暂停屏幕外的循环动画

循环动画即使不可见也会消耗 GPU 资源。

```ts
"use client";
import { useEffect, useRef } from "react";

export function usePauseOffscreen<T extends HTMLElement>() {
  const ref = useRef<T | null>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const io = new IntersectionObserver(([entry]) => {
      el.style.animationPlayState = entry.isIntersecting ? "running" : "paused";
    });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return ref;
}
```

## 合成层与 will-change

`will-change` 会创建一个新的合成器层——这会带来内存开销。

- 仅在动画期间提升，结束后移除
- 仅适用于 `transform` 和 `opacity`
- 过多的层比不提升更糟糕

```css
.animating { will-change: transform, opacity; }
```

在动画开始时切换类，在 `transitionend` 或 `animationend` 事件后移除。

## 修复抖动的 1 像素偏移

元素在动画开始/结束时可能因 GPU/CPU 切换而偏移 1 像素。在动画期间（非永久）应用 `will-change: transform`，以在整个过程中保持 GPU 合成。

```css
/* 在动画期间应用，动画结束后移除 */
.animating {
  will-change: transform;
}
```