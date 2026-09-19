#!/usr/bin/env python3
"""law-md-write 校验：扫描本地库里的 Markdown 结构违规。只读，不改文件。"""
import os, re, sys, unicodedata

VAULT = sys.argv[1] if len(sys.argv) > 1 else "/Users/fullstop/Documents/知识库"
SKIP_DIRS = {".obsidian", ".trash", ".git"}
SKIP_PARTS = ("/附件/", "/01-材料/", "/01-参考材料/")   # 附件与参考材料原文不按笔记规范要求
FENCE_MARK = chr(96) * 3

def clean_title(name):
    return re.sub(r"^\d+[- ]*", "", re.sub(r"\.md$", "", name)).strip()

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[\s_/\\|()（）\[\]【】“”\"'’‘·—–\-.,，。：:；;、!！?？]", "", s).lower()

def headings(text):
    out, fence = [], False
    for i, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith(FENCE_MARK):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            out.append((i, len(m.group(1)), m.group(2)))
    return out

def main():
    issues, notes, checked = [], 0, 0
    for dp, dn, fn in os.walk(VAULT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".")]   # 顺手跳过 .claudian 等工具目录
        for f in sorted(fn):
            if not f.endswith(".md"):
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, VAULT)
            if any(p in "/" + rel for p in SKIP_PARTS):
                continue
            notes += 1
            text = open(path, encoding="utf-8").read()
            hs = headings(text)
            if not hs:
                continue
            checked += 1
            def add(kind, detail):
                issues.append((kind, rel, detail))
            _, first_lvl, first_text = hs[0]
            if first_lvl != 1:
                add("首标题不是 H1", "H%d %s" % (first_lvl, first_text[:40]))
            if norm(first_text) == norm(clean_title(f)):
                add("首标题与文件名重复", first_text[:40])
            numbering_ok = first_lvl == 1   # 起头层级不对时编号核对没有意义，只跳过这一项
            counters, prev = [0] * 7, 0
            numbered = [bool(re.match(r"^\d+(\.\d+)*\.?\s", t)) for _, _, t in hs]
            if numbering_ok and any(numbered) and not all(numbered):
                add("编号混用", "同级标题有的带编号有的不带")
            mismatch = []
            for ln, lvl, txt in hs:
                if prev and lvl > prev + 1:
                    add("标题跳级", "L%d H%d->H%d %s" % (ln, prev, lvl, txt[:30]))
                prev = lvl
                counters[lvl] += 1
                for d in range(lvl + 1, 7):
                    counters[d] = 0
                want = ".".join(str(counters[i]) for i in range(1, lvl + 1))
                if lvl == 1:
                    want += "."
                m = re.match(r"^(\d+(?:\.\d+)*)(\.?)\s", txt)
                if not m:
                    continue
                segs = m.group(1).split(".")
                if any(len(s) > 2 for s in segs):   # 年份等非章节编号，跳过
                    continue
                if m.group(1) + m.group(2) != want:
                    mismatch.append("L%d 实%s 应%s" % (ln, m.group(1) + m.group(2), want))
            if numbering_ok and mismatch:
                add("编号不连续", "; ".join(mismatch[:3]))
            for ln, line in enumerate(text.split("\n"), 1):
                if re.search(r"(?<!\$)\$\$(?!\$)", line) and not line.strip().startswith("$$"):
                    add("行内使用 $$", "L%d" % ln)
                    break
            m = re.search(r"\n[ \t]*\n[ \t]*\n[ \t]*\n", text)
            if m:
                add("连续空行", "字符 %d" % m.start())
            for ln, line in enumerate(text.split("\n"), 1):
                if re.search(r"见\s*(第?\s*\d+(\.\d+)*\s*节|表\s*\d|图\s*\d|\d+-[^\s]*\.md)", line):
                    add("裸引用「见 xxx」", "L%d %s" % (ln, line.strip()[:40]))
                    break
            for ln, line in enumerate(text.split("\n"), 1):
                if re.search(r"!\[\[[^\]]*/[^\]]*\]\]|!\[[^\]]*\]\([^)]*/[^)]*\)", line):
                    add("图片引用带路径", "L%d" % ln)
                    break
                if re.search(r"\[\[[^\]]*/[^\]]*\]\]", line):
                    add("双链带路径", "L%d" % ln)
                    break
    by_kind = {}
    for kind, rel, detail in issues:
        by_kind.setdefault(kind, []).append((rel, detail))
    print("扫描 %d 篇（有标题 %d 篇）" % (notes, checked))
    for kind, items in sorted(by_kind.items(), key=lambda x: -len(x[1])):
        print("\n[%s] %d 处" % (kind, len(items)))
        for rel, detail in items[:6]:
            print("   %s  —  %s" % (rel, detail))
        if len(items) > 6:
            print("   … 另外 %d 处" % (len(items) - 6))
    if not issues:
        print("无违规")

main()
