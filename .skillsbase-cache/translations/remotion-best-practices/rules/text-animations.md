---
name: text-animations
description: 适用于 Remotion 的排版与文字动画模式。
metadata:
  tags: typography, text, typewriter, highlighter ken
---

## 文字动画

基于 `useCurrentFrame()`，逐字符缩减字符串以创建打字机效果。

## 打字机效果

查看 [Typewriter](assets/text-animations-typewriter.tsx) 获取一个包含闪烁光标及首句后暂停的高级示例。

始终使用字符串切片实现打字机效果，切勿使用逐字符透明度。

## 单词高亮

查看 [Word Highlight](assets/text-animations-word-highlight.tsx) 获取单词高亮动画示例，例如使用荧光笔效果。