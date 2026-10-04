"""启发式 token 估算（中英文混合）。

⚠️ 这是**启发式估算，不是精确值**。真实 token 数必须用对应模型的官方 tokenizer
（如 tiktoken）才能得到。这里的规则只是为了在没有任何依赖时给出量级参考：

- 每个汉字（含常见中文标点）≈ 1 个 token；
- 英文及其它非中文内容：按“单词数 × 1.3”四舍五入（经验上约 0.75 个英文单词 = 1 token）；
  连续的字母/数字串算一个词。
"""

from __future__ import annotations

import re

# CJK 统一表意文字
_CJK_IDEO = re.compile(r"[一-鿿]")
# 常见中文标点
_CJK_PUNCT = "，。！？；：、「」『』“”‘’（）《》—…·"
# 英文单词/数字串
_WORD = re.compile(r"[A-Za-z0-9]+")

WORDS_PER_TOKEN = 1.3  # 英文：多少个单词约等于 1 个 token


def _is_cjk(ch: str) -> bool:
    return bool(_CJK_IDEO.match(ch)) or ch in _CJK_PUNCT


def estimate_tokens(text: str) -> dict:
    """估算一段文本的 token 数，返回明细与总数。

    返回 dict: {"cjk_chars", "latin_words", "cjk_tokens", "latin_tokens", "total"}
    """
    cjk_chars = 0
    latin_words = 0
    buf = []

    def flush_latin():
        nonlocal latin_words
        if not buf:
            return
        latin_words += len(_WORD.findall("".join(buf)))
        buf.clear()

    for ch in text:
        if _is_cjk(ch):
            flush_latin()
            cjk_chars += 1
        else:
            buf.append(ch)
    flush_latin()

    cjk_tokens = cjk_chars
    latin_tokens = round(latin_words * WORDS_PER_TOKEN)
    return {
        "cjk_chars": cjk_chars,
        "latin_words": latin_words,
        "cjk_tokens": cjk_tokens,
        "latin_tokens": latin_tokens,
        "total": cjk_tokens + latin_tokens,
    }
