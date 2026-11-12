#!/usr/bin/env python3
"""BGM 生成（本地 ComfyUI · MiniMax Music 3）。
用法：python3 comfy_music.py --out <工程>/edit/public/music/bgm.mp3 [--caption "…"] [--lyrics "…"] [--sec 60] [--seed 7] [--steps 30]
- caption：三段式英文描述 Global Metadata → Vocal Details → Arrangement（风格 / BPM / 调性 / 情绪 → 人声 → 配器与结构）。不写用下面的 DEFAULT_CAPTION（知识口播用：轻快、温暖、纯音乐）
- lyrics：只放结构标签就是纯音乐，例如 "[Intro]\\n\\n[Instrumental]\\n\\n[Outro]"（默认）。口播 BGM 一定要纯音乐，人声会和口播打架
- sec：60 秒左右就够，lin_mix.py 会 3 秒交叉淡化循环到成片长度
输出 --out（.mp3 或 .wav / .flac，按后缀转），旁边存 <名>.prompt.txt。RTX 3090：60 秒约 1–3 分钟（首次含加载更久）。
"""
import json, sys, subprocess, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import comfy_batch as CB

DEFAULT_CAPTION = (
    "Global Metadata: Light corporate lo-fi / soft pop instrumental, 92 BPM, C major. Warm, optimistic, calm and focused, "
    "like a friendly explainer video about personal finance. Steady energy from start to end with no big drops or build-ups, "
    "clean modern mix, leaves plenty of space in the mid range for a spoken voice-over.\n\n"
    "Vocal Details: Pure instrumental, no vocals, no humming, no vocal chops, no spoken words.\n\n"
    "Arrangement: Soft electric piano chords as the bed, gentle plucked synth and muted guitar playing a light repeating motif, "
    "round warm bass, tight soft kick and light finger-snap backbeat with shaker. Intro: piano alone for two bars then the beat comes in. "
    "Main body: the same groove loops evenly with small melodic variations, never busy. Outro: elements drop out and the piano ends on a soft resolved chord.")
DEFAULT_LYRICS = "[Intro]\n\n[Instrumental]\n\n[Instrumental]\n\n[Outro]"


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def main():
    if "--out" not in sys.argv:
        sys.exit(__doc__)
    out = Path(arg("--out")).resolve(); out.parent.mkdir(parents=True, exist_ok=True)
    cap, lyr = arg("--caption", DEFAULT_CAPTION), arg("--lyrics", DEFAULT_LYRICS).replace("\\n", "\n")
    sec, seed, steps = float(arg("--sec", 60)), int(arg("--seed", 7)), int(arg("--steps", 30))
    wf = json.loads((HERE.parent / "comfy/music.api.json").read_text())
    wf["13"]["inputs"].update(caption=cap, lyrics=lyr, seed=seed, max_duration=sec)
    wf["9"]["inputs"].update(seed=seed, steps=steps)
    tag = hashlib.sha1(json.dumps([cap, lyr, sec, seed, steps]).encode()).hexdigest()[:8]
    wf["35"]["inputs"]["filename_prefix"] = f"koubo/music/bgm_{tag}"
    out.with_suffix(".prompt.txt").write_text(f"caption:\n{cap}\n\nlyrics:\n{lyr}\n\nsec={sec} seed={seed} steps={steps}\n")
    outs, took = CB.wait(CB.submit(wf), "BGM", poll=5)
    raw = out.with_name(out.stem + "_raw.flac")
    CB.fetch(outs, "35", raw)
    if out.suffix.lower() == ".flac":
        raw.replace(out)
    else:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), *(["-q:a", "0"] if out.suffix.lower() == ".mp3" else []), str(out)], check=True)
        raw.unlink()
    print(f"BGM 完成（{took:.0f}s）→ {out}")


if __name__ == "__main__":
    main()
