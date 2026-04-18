# Tailwind 动画预设

适用于 `tailwind.config.ts` 的即用配置。

---

## 完整动画配置

添加到 Tailwind 配置文件的 `theme.extend` 中：

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  // ... 其他配置
  theme: {
    extend: {
      // ... 其他扩展配置
      
      keyframes: {
        // === 淡入淡出动画 ===
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'fade-out': {
          from: { opacity: '1' },
          to: { opacity: '0' },
        },
        'fade-slide-in': {
          from: { 
            opacity: '0', 
            transform: 'translateY(20px)',
            filter: 'blur(4px)',
          },
          to: { 
            opacity: '1', 
            transform: 'translateY(0)',
            filter: 'blur(0)',
          },
        },
        'fade-slide-in-right': {
          from: { 
            opacity: '0', 
            transform: 'translateX(20px)',
          },
          to: { 
            opacity: '1', 
            transform: 'translateX(0)',
          },
        },
        'fade-slide-in-left': {
          from: { 
            opacity: '0', 
            transform: 'translateX(-20px)',
          },
          to: { 
            opacity: '1', 
            transform: 'translateX(0)',
          },
        },

        // === 缩放动画 ===
        'scale-in': {
          from: { 
            opacity: '0', 
            transform: 'scale(0.9)',
          },
          to: { 
            opacity: '1', 
            transform: 'scale(1)',
          },
        },
        'scale-out': {
          from: { 
            opacity: '1', 
            transform: 'scale(1)',
          },
          to: { 
            opacity: '0', 
            transform: 'scale(0.9)',
          },
        },

        // === 滑动动画 ===
        'slide-up': {
          from: { transform: 'translateY(100%)' },
          to: { transform: 'translateY(0)' },
        },
        'slide-down': {
          from: { transform: 'translateY(-100%)' },
          to: { transform: 'translateY(0)' },
        },
        'slide-left': {
          from: { transform: 'translateX(100%)' },
          to: { transform: 'translateX(0)' },
        },
        'slide-right': {
          from: { transform: 'translateX(-100%)' },
          to: { transform: 'translateX(0)' },
        },

        // === 裁剪路径显示动画 ===
        'clip-reveal-right': {
          from: { clipPath: 'inset(0 100% 0 0)' },
          to: { clipPath: 'inset(0 0 0 0)' },
        },
        'clip-reveal-left': {
          from: { clipPath: 'inset(0 0 0 100%)' },
          to: { clipPath: 'inset(0 0 0 0)' },
        },
        'clip-reveal-up': {
          from: { clipPath: 'inset(100% 0 0 0)' },
          to: { clipPath: 'inset(0 0 0 0)' },
        },
        'clip-reveal-down': {
          from: { clipPath: 'inset(0 0 100% 0)' },
          to: { clipPath: 'inset(0 0 0 0)' },
        },

        // === 连续动画 ===
        'marquee': {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(-50%)' },
        },
        'marquee-reverse': {
          from: { transform: 'translateX(-50%)' },
          to: { transform: 'translateX(0)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'pulse-soft': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        'spin-slow': {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' },
        },
        'blink': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },

        // === 背景动画 ===
        'gradient-shift': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'kenburns': {
          from: { transform: 'scale(1)' },
          to: { transform: 'scale(1.1)' },
        },

        // === 特殊效果 ===
        'ripple': {
          from: { 
            width: '0', 
            height: '0', 
            opacity: '0.5',
          },
          to: { 
            width: '200px', 
            height: '200px', 
            opacity: '0',
          },
        },
        'beam-rotate': {
          to: { transform: 'rotate(360deg)' },
        },
        'shimmer': {
          from: { backgroundPosition: '-200% 0' },
          to: { backgroundPosition: '200% 0' },
        },
      },

      animation: {
        // === 淡入淡出 ===
        'fade-in': 'fade-in 0.5s ease-out both',
        'fade-out': 'fade-out 0.3s ease-out both',
        'fade-slide-in': 'fade-slide-in 0.6s ease-out both',
        'fade-slide-in-right': 'fade-slide-in-right 0.5s ease-out both',
        'fade-slide-in-left': 'fade-slide-in-left 0.5s ease-out both',

        // === 缩放 ===
        'scale-in': 'scale-in 0.3s ease-out both',
        'scale-out': 'scale-out 0.2s ease-in both',

        // === 滑动 ===
        'slide-up': 'slide-up 0.5s ease-out both',
        'slide-down': 'slide-down 0.5s ease-out both',
        'slide-left': 'slide-left 0.5s ease-out both',
        'slide-right': 'slide-right 0.5s ease-out both',

        // === 裁剪显示 ===
        'clip-reveal-right': 'clip-reveal-right 0.8s ease-out both',
        'clip-reveal-left': 'clip-reveal-left 0.8s ease-out both',
        'clip-reveal-up': 'clip-reveal-up 0.8s ease-out both',
        'clip-reveal-down': 'clip-reveal-down 0.8s ease-out both',

        // === 连续动画 ===
        'marquee': 'marquee 30s linear infinite',
        'marquee-fast': 'marquee 15s linear infinite',
        'marquee-slow': 'marquee 45s linear infinite',
        'marquee-reverse': 'marquee-reverse 30s linear infinite',
        'float': 'float 3s ease-in-out infinite',
        'pulse-soft': 'pulse-soft 2s ease-in-out infinite',
        'spin-slow': 'spin-slow 8s linear infinite',
        'blink': 'blink 1s step-end infinite',

        // === 背景 ===
        'gradient-shift': 'gradient-shift 15s ease infinite',
        'kenburns': 'kenburns 20s ease-out forwards',

        // === 特殊效果 ===
        'ripple': 'ripple 0.6s ease-out forwards',
        'beam-rotate': 'beam-rotate 2s linear infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
    },
  },
};

export default config;
```

---

## 全局 CSS 补充

添加到 `globals.css`：

```css
/* === 减少运动 === */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* === 工具类 === */

/* 错开延迟工具类 */
.stagger-1 { animation-delay: 100ms; }
.stagger-2 { animation-delay: 200ms; }
.stagger-3 { animation-delay: 300ms; }
.stagger-4 { animation-delay: 400ms; }
.stagger-5 { animation-delay: 500ms; }
.stagger-6 { animation-delay: 600ms; }
.stagger-7 { animation-delay: 700ms; }
.stagger-8 { animation-delay: 800ms; }

/* 悬停时暂停动画（用于跑马灯） */
.hover-pause:hover {
  animation-play-state: paused;
}

/* 跑马灯边缘淡出遮罩 */
.marquee-mask {
  mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 10%,
    black 90%,
    transparent 100%
  );
}

/* 按钮光束效果基础样式 */
.btn-beam {
  position: relative;
  overflow: hidden;
}

.btn-beam::before {
  content: '';
  position: absolute;
  inset: 0;
  border: 1px solid transparent;
  border-radius: inherit;
  background: linear-gradient(90deg, transparent, hsl(var(--primary)), transparent) border-box;
  mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s;
}

.btn-beam:hover::before {
  opacity: 1;
  animation: beam-rotate 2s linear infinite;
}

/* 微光骨架屏效果 */
.shimmer {
  background: linear-gradient(
    90deg,
    hsl(var(--muted)) 0%,
    hsl(var(--muted-foreground) / 0.1) 50%,
    hsl(var(--muted)) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s linear infinite;
}
```

---

## 最小配置（快速开始）

如果只需要基础功能：

```ts
keyframes: {
  'fade-slide-in': {
    from: { opacity: '0', transform: 'translateY(20px)' },
    to: { opacity: '1', transform: 'translateY(0)' },
  },
  'scale-in': {
    from: { opacity: '0', transform: 'scale(0.95)' },
    to: { opacity: '1', transform: 'scale(1)' },
  },
  'marquee': {
    from: { transform: 'translateX(0)' },
    to: { transform: 'translateX(-50%)' },
  },
},
animation: {
  'fade-slide-in': 'fade-slide-in 0.5s ease-out both',
  'scale-in': 'scale-in 0.3s ease-out both',
  'marquee': 'marquee 30s linear infinite',
},
```

---

## 使用示例

### 英雄区域

```tsx
<section className="relative">
  <h1 className="animate-fade-slide-in">欢迎</h1>
  <p className="animate-fade-slide-in stagger-1">副标题文本</p>
  <button className="animate-fade-slide-in stagger-2 hover:-translate-y-0.5 hover:shadow-lg transition-all">
    开始使用
  </button>
</section>
```

### 带错开效果的卡片网格

```tsx
<div className="grid grid-cols-3 gap-6">
  {cards.map((card, i) => (
    <div
      key={card.id}
      className="animate-fade-slide-in hover:scale-[1.02] hover:shadow-xl transition-all"
      style={{ animationDelay: `${i * 100}ms` }}
    >
      {card.content}
    </div>
  ))}
</div>
```

### Logo 跑马灯

```tsx
<div className="overflow-hidden marquee-mask">
  <div className="flex gap-8 animate-marquee hover-pause">
    {[...logos, ...logos].map((logo, i) => (
      <img key={i} src={logo} className="h-8 w-auto" />
    ))}
  </div>
</div>
```

### 带效果的按钮

```tsx
<button className="btn-beam px-6 py-3 rounded-full bg-primary text-primary-foreground hover:-translate-y-0.5 hover:shadow-lg transition-all">
  联系我们
</button>
```