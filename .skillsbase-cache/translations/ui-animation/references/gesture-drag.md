# 手势与拖拽动画

用户直接操作元素时的拖拽、滑动和手势交互模式。

## 目录
- [基于动量的关闭](#基于动量的关闭)
- [边界阻尼](#边界阻尼)
- [指针捕获](#指针捕获)
- [多点触控防护](#多点触控防护)
- [摩擦与硬性停止](#摩擦与硬性停止)
- [滑动关闭模式](#滑动关闭模式)

## 基于动量的关闭

无需拖拽超过距离阈值。计算释放时的速度——快速轻弹就应足以触发关闭。

```ts
function onPointerUp(e: PointerEvent) {
  const timeTaken = Date.now() - dragStartTime;
  const velocity = Math.abs(swipeAmount) / timeTaken;

  if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
    dismiss();
  } else {
    snapBack();
  }
}
```

使用速度 > 0.11 作为合理的默认阈值。结合最小距离阈值（例如 20px）以防止意外关闭。

## 边界阻尼

当用户拖拽超出自然边界时（例如在已到达顶部时继续向上拉动抽屉），应用阻尼效果。拖拽越远，元素移动越少。

```ts
function applyDamping(offset: number, max: number): number {
  return max * (1 - Math.exp(-offset / max));
}

// 用法：随着偏移量增加，移动逐渐减弱
const dampedOffset = applyDamping(rawOffset, 200);
```

现实中的物体不会突然停止——它们会先减速。使用摩擦而非硬性停止总是感觉更自然。

## 指针捕获

一旦开始拖拽，捕获元素上的所有指针事件。这确保即使指针离开元素边界，拖拽仍能继续。

```ts
function onPointerDown(e: PointerEvent) {
  (e.target as HTMLElement).setPointerCapture(e.pointerId);
  isDragging = true;
}

function onPointerUp(e: PointerEvent) {
  (e.target as HTMLElement).releasePointerCapture(e.pointerId);
  isDragging = false;
}
```

始终使用 `setPointerCapture`——没有它，快速滑动会脱离元素，导致拖拽中断。

## 多点触控防护

初始拖拽开始后，忽略额外的触摸点。没有此防护，拖拽过程中切换手指会导致元素跳动。

```ts
let activeTouchId: number | null = null;

function onPointerDown(e: PointerEvent) {
  if (activeTouchId !== null) return; // 忽略额外触摸
  activeTouchId = e.pointerId;
  // 开始拖拽...
}

function onPointerUp(e: PointerEvent) {
  if (e.pointerId !== activeTouchId) return;
  activeTouchId = null;
  // 结束拖拽...
}
```

## 摩擦与硬性停止

与其阻止拖拽越过边界，不如允许越过但增加摩擦：

```ts
function applyFriction(delta: number, isAtBoundary: boolean): number {
  if (!isAtBoundary) return delta;
  return delta * 0.3; // 边界处仅允许 30% 的移动
}
```

硬性停止感觉像是故障——用户期望符合物理规律。为滚动容器、滑块和抽屉应用摩擦效果。

## 滑动关闭模式

结合速度、距离和方向实现完整的滑动手势：

```ts
function handleSwipeEnd(direction: "left" | "right", distance: number, velocity: number) {
  const shouldDismiss = distance > THRESHOLD || velocity > 0.11;

  if (shouldDismiss) {
    // 沿滑动方向以剩余动量动画退出
    animateOut(direction, velocity);
  } else {
    // 弹性回弹至原点
    springBack();
  }
}
```

退出动画应沿滑动方向延续动量——突然切换到不同方向会感觉错误。