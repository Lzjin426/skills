#!/usr/bin/env python3
"""MiMo V2.5 视觉描述脚本 — 让无视觉能力的模型（如 DeepSeek）通过 MiMo 看懂图片。

支持两种模式：
  parallel（默认） : 每张图一个请求，并发执行，输出每张图的独立详细描述。
  together         : 所有图片放进同一个请求，让模型一次性对比/整体描述多张图。

API 端点（官方文档 https://mimo.mi.com/docs）：
  POST https://api.xiaomimimo.com/v1/chat/completions
  认证：Authorization: Bearer <key>（也支持 api-key header）
  模型：mimo-v2.5（图片理解目前仅支持该模型）
  图片输入：公开 URL 或 data:image/{mime};base64,<base64>，单图 ≤ 50MB

密钥优先级：环境变量 MIMO_API_KEY > 本 skill 目录下私有 .api_key 文件。
"""

import argparse
import base64
import concurrent.futures
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request

BASE_URL = "https://api.xiaomimimo.com/v1/chat/completions"
MODEL = "mimo-v2.5"
DEFAULT_MAX_TOKENS = 4096  # 推理模型需要足够大的 token 预算，否则 content 会被截断为空

DEFAULT_PROMPT = (
    "请尽可能详细地描述这张图片的内容，包括：整体场景、主体对象、颜色与光线、"
    "文字信息（如有，请逐字转录）、人物/物体的位置关系、情绪或氛围，以及任何值得注意的细节。"
    "如果图片是截图、图表、界面或文档，请完整转述其中的文字和结构。"
)


def build_payload(content_parts: list, max_tokens: int, thinking: bool) -> dict:
    """构造请求体。MiMo V2.5 是推理模型，默认关闭思考模式（更快、更省），
    需要深度分析时用 --thinking 开启。"""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content_parts}],
        "max_completion_tokens": max_tokens,
        "temperature": 0.7,
        "stream": False,
    }
    if not thinking:
        payload["thinking"] = {"type": "disabled"}
    return payload


def build_request(content_parts: list, api_key: str, max_tokens: int,
                  thinking: bool, timeout: int) -> urllib.request.Request:
    payload = build_payload(content_parts, max_tokens, thinking)
    return urllib.request.Request(
        BASE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )


def load_api_key(skill_dir: str) -> str:
    key = os.environ.get("MIMO_API_KEY") or os.environ.get("MIMO_VISION_API_KEY")
    if key:
        return key.strip()
    key_file = os.path.join(skill_dir, ".api_key")
    if os.path.isfile(key_file):
        with open(key_file, "r", encoding="utf-8") as f:
            key = f.read().strip()
        if key:
            return key
    sys.stderr.write("错误：未找到 MiMo API key。请设置环境变量 MIMO_API_KEY 或在 skill 目录创建 .api_key 文件。\n")
    sys.exit(2)


def to_image_url(image: str) -> tuple[str, str]:
    """把本地路径或 URL 转成 API 可用的 image_url，返回 (label, url)。"""
    if image.startswith(("http://", "https://")):
        return image, image
    if not os.path.isfile(image):
        sys.stderr.write(f"错误：文件不存在或不是本地路径/URL：{image}\n")
        sys.exit(2)
    size = os.path.getsize(image)
    if size > 50 * 1024 * 1024:
        sys.stderr.write(f"错误：图片超过 50MB 上限：{image} ({size/1024/1024:.1f}MB)\n")
        sys.exit(2)
    mime = mimetypes.guess_type(image)[0] or "image/png"
    with open(image, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return os.path.basename(image), f"data:{mime};base64,{b64}"


def call_mimo(content_parts: list, api_key: str, max_tokens: int,
              thinking: bool, timeout: int) -> dict:
    req = build_request(content_parts, api_key, max_tokens, thinking, timeout)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body[:500]}") from e


def extract_content(data: dict) -> str:
    try:
        content = data["choices"][0]["message"].get("content") or ""
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"响应格式异常：{json.dumps(data, ensure_ascii=False)[:500]}") from e
    if not content:
        finish = data.get("choices", [{}])[0].get("finish_reason")
        if finish == "length":
            raise RuntimeError("输出被 max_completion_tokens 截断（content 为空）。请增大 --max-tokens 后重试。")
        raise RuntimeError("MiMo 返回了空 content。请检查图片是否有效或增大 --max-tokens。")
    return content.strip()


def describe_one(item: tuple[str, str], prompt: str, api_key: str,
                 max_tokens: int, thinking: bool, timeout: int) -> tuple[str, str]:
    label, url = item
    try:
        content_parts = [
            {"type": "image_url", "image_url": {"url": url}},
            {"type": "text", "text": prompt},
        ]
        data = call_mimo(content_parts, api_key, max_tokens, thinking, timeout)
        return label, extract_content(data)
    except Exception as e:
        return label, f"[错误] {e}"


def main() -> int:
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser(
        description="用 MiMo V2.5 描述一张或多张图片（并行或一起看）。"
    )
    parser.add_argument("images", nargs="+", help="图片本地路径或 http(s) URL，至少一张")
    parser.add_argument("--mode", choices=["parallel", "together"], default="parallel",
                        help="parallel=每图一请求并发（默认）；together=所有图放同一请求一起看")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT,
                        help="描述指令，默认是详细描述（含文字转录）")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS,
                        help="单次请求最大输出 token，默认 4096（推理模型需要较大预算）")
    parser.add_argument("--concurrency", type=int, default=4,
                        help="parallel 模式的并发请求数，默认 4")
    parser.add_argument("--thinking", action="store_true",
                        help="开启 MiMo 深度思考模式（更慢更贵但分析更深）；默认关闭")
    parser.add_argument("--timeout", type=int, default=180, help="单请求超时秒数，默认 180")
    args = parser.parse_args()

    api_key = load_api_key(skill_dir)
    items = [to_image_url(img) for img in args.images]

    if args.mode == "together":
        content_parts = [{"type": "image_url", "image_url": {"url": url}} for _, url in items]
        content_parts.append({"type": "text", "text": (
            f"这里有 {len(items)} 张图片。{args.prompt}"
            "请按图片顺序逐一描述（标注 图片 1、图片 2 …），并指出它们之间的异同或关联。"
        )})
        try:
            with urllib.request.urlopen(
                build_request(content_parts, api_key, args.max_tokens, args.thinking, args.timeout)
            ) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            sys.stderr.write(f"请求失败 HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:500]}\n")
            return 1
        print(extract_content(data))
        return 0

    # parallel 模式：每图一请求，并发执行
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = [
            ex.submit(describe_one, item, args.prompt, api_key, args.max_tokens, args.thinking, args.timeout)
            for item in items
        ]
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())
    # 按输入顺序输出
    order = {label: i for i, (label, _) in enumerate(items)}
    results.sort(key=lambda r: order.get(r[0], 0))
    for i, (label, desc) in enumerate(results, 1):
        print(f"## 图片 {i}：{label}")
        print(desc)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
