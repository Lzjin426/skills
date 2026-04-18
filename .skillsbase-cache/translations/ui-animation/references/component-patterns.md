# 组件动画模式

## 目录
- [按钮](#按钮)
- [弹出框与下拉菜单](#弹出框与下拉菜单)
- [工具提示](#工具提示)
- [抽屉与面板](#抽屉与面板)
- [模态框与对话框](#模态框与对话框)
- [消息提示](#消息提示)
- [列表与错开动画](#列表与错开动画)
- [悬停效果](#悬停效果)

## 按钮

在 `:active` 状态添加 `transform: scale(0.97)` 以实现即时按压反馈。

```css
.button {
  transition: transform 160ms cubic-bezier(0.22, 1, 0.36, 1);
}
.button:active {
  transform: scale(0.97);
}
```

使用模糊效果来掩盖按钮状态间不完美的淡入淡出过渡：

```css
.button-content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

保持模糊度低于 20px —— 重度模糊非常消耗性能，尤其是在 Safari 中。

## 弹出框与下拉菜单

从触发点缩放进入，而不是从中心。默认的 `transform-origin: center` 对于弹出框是错误的。

```css
/* Radix UI */
.popover {
  transform-origin: var(--radix-popover-content-transform-origin);
}

/* 数据属性回退方案 */
.popover[data-side="top"]    { transform-origin: bottom center; }
.popover[data-side="bottom"] { transform-origin: top center; }
.popover[data-side="left"]   { transform-origin: center right; }
.popover[data-side="right"]  { transform-origin: center left; }
```

从 `scale(0.88)` 开始，永远不要用 `scale(0)`。现实世界中没有任何事物是从虚无中出现的。

```css
.menu {
  transform: scale(0.88);
  opacity: 0;
  transition: transform 200ms cubic-bezier(0.22, 1, 0.36, 1),
              opacity 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.menu[data-open="true"] {
  transform: scale(1);
  opacity: 1;
}
```

## 工具提示

首次出现前延迟（300–500ms）以防止意外激活。一旦一个工具提示已打开，后续工具提示应无动画地立即打开。

```css
.tooltip {
  transition: transform 125ms ease-out, opacity 125ms ease-out;
  transform-origin: var(--transform-origin);
}
.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}
.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

## 抽屉与面板

使用移动缓动曲线。百分比 `translateY`/`translateX` 能适应任何抽屉高度。

```css
.drawer {
  transform: translateY(100%);
  transition: transform 240ms cubic-bezier(0.25, 1, 0.5, 1);
}
.drawer[data-open="true"] {
  transform: translateY(0);
}
```

```tsx
<motion.aside
  initial={{ transform: "translate3d(100%, 0, 0)" }}
  animate={{ transform: "translate3d(0, 0, 0)" }}
  exit={{ transform: "translate3d(100%, 0, 0)" }}
  transition={{ duration: 0.24, ease: [0.25, 1, 0.5, 1] }}
/>
```

## 模态框与对话框

**例外：模态框保持 `transform-origin: center`。** 它们代表应用级状态，而非锚定于某个触发器。

使用 `@starting-style` 实现无需 JavaScript 的进入动画：

```css
.modal {
  opacity: 1;
  transform: scale(1);
  transition: opacity 250ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 250ms cubic-bezier(0.22, 1, 0.36, 1);

  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

当 `@starting-style` 浏览器支持不足时，回退到 `data-mounted` 属性模式。

## 消息提示

从同一方向进入和退出以保持空间一致性（使滑动关闭操作更直观）。

```css
.toast {
  transform: translate3d(0, 6px, 0);
  opacity: 0;
  transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
              opacity 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.toast[data-open="true"] {
  transform: translate3d(0, 0, 0);
  opacity: 1;
}
```

对消息提示使用 CSS 过渡（而非关键帧）—— 它们被频繁添加，而关键帧在中断时会重新开始，而过渡则可以平滑地重新定位。

## 列表与错开动画

保持错开延迟简短（每项 30–50ms）。总错开时间应保持在 300ms 以内。

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
              opacity 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.list[data-open="true"] .item {
  opacity: 1;
  transform: translateY(0);
}
.list[data-open="true"] .item:nth-child(2) { transition-delay: 50ms; }
.list[data-open="true"] .item:nth-child(3) { transition-delay: 100ms; }
.list[data-open="true"] .item:nth-child(4) { transition-delay: 150ms; }
```

```tsx
const listVariants = {
  show: { transition: { staggerChildren: 0.05 } },
};
```

在错开动画播放期间，切勿阻塞交互。

## 悬停效果

通过媒体查询限制悬停动画，以避免在触摸设备上产生误触发。

```css
@media (hover: hover) and (pointer: fine) {
  .link {
    transition: color 200ms ease, opacity 200ms ease;
  }
  .link:hover {
    opacity: 0.8;
  }
}
```

通过在父元素上应用悬停并动画化子元素来修复悬停闪烁问题：

```css
.box:hover .box-inner {
  transform: translateY(-20%);
}
.box-inner {
  transition: transform 200ms ease;
}
```