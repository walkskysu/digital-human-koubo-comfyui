#!/usr/bin/env python3
"""阿拉伯数字 → 中文读法。whisper / SenseVoice 常把念出来的「七十二」「百分之六」写成「72」「6%」，比对、对齐前先统一成念法。"""
import re


def cn_int(n: int) -> str:
    """整数 → 中文读法（99 → 九十九，2026 → 二千零二十六），用于回听比对。"""
    D = "零一二三四五六七八九"
    if n == 0:
        return "零"
    if n >= 10 ** 8:
        return cn_int(n // 10 ** 8) + "亿" + ("零" if n % 10 ** 8 < 10 ** 7 and n % 10 ** 8 else "") + (cn_int(n % 10 ** 8) if n % 10 ** 8 else "")
    if n >= 10 ** 4:
        return cn_int(n // 10 ** 4) + "万" + ("零" if n % 10 ** 4 < 1000 and n % 10 ** 4 else "") + (cn_int(n % 10 ** 4) if n % 10 ** 4 else "")
    out, zero = "", False
    for unit, u in ((1000, "千"), (100, "百"), (10, "十"), (1, "")):
        d = n // unit % 10
        if d:
            out += ("零" if zero and out else "") + D[d] + u; zero = False
        elif out:
            zero = True
    return out[1:] if out.startswith("一十") else out


def cn_digits(text: str) -> str:
    """把阿拉伯数字换成中文读法（小数点后逐位读），稿子和转写都过一遍再比，免得「九十九」和「99」算错。"""
    def rep(m):
        a, _, b = m.group(0).partition(".")
        return cn_int(int(a)) + ("点" + "".join("零一二三四五六七八九"[int(c)] for c in b) if b else "")
    text = re.sub(r"(\d+(?:\.\d+)?)\s*[%％]", lambda m: "百分之" + m.group(1), text)
    return re.sub(r"\d+(?:\.\d+)?", rep, text)
