#!/usr/bin/env python3
"""场景图 / 四视图 / 贴纸（本地 ComfyUI · Qwen Image 2.1 Image Edit，替代 GPT Image 2.5）。
用法：python3 comfy_scene.py scenes.json --out <目录> [--only open] [--redo open] [--steps 25] [--seed 3]

scenes.json：[{"id": "open", "prompt": "…", "refs": ["../assets/avatar_ref.jpg", "可选第二张参考.png"], "ratio": "9:16"}, …]
- refs：参考图（最多 10 张，路径相对 scenes.json），提示词里按顺序叫 Picture 1 / Picture 2…；不写就是纯文生图
- ratio：9:16（736×1312）/ 16:9（1312×736）/ 3:4（864×1152）/ 4:3 / 1:1（1024×1024），默认 9:16
- prompt：直接写要的结果，例如
    开场场景图：「Picture 1 中的女生站在直播间里，背后是灯光货架和环形补光灯，同样的发型、白色罗纹背心、同样的脸，竖屏自拍构图，画面里不要任何文字」
    四视图：「同一个人、同一套衣服发型，四格并排：正面 / 左侧 / 右侧 / 背面，浅灰无缝背景，不出现任何文字」
输出 <out>/<id>.png，进度存 <out>/.scene_state.json（改了内容才重做）。每张约 2–5 分钟（25 步，2026-11-12 实测首张含加载 307 秒）。人物在参考图里是近景时，「中景、头顶留背景」不一定听，要中景就给一张中景参考。
开场场景图要拿来当口播参考图时：script.json 那几段加 "ref": "<out>/<id>.png"（comfy_batch.py 会用它替代默认形象照）。
"""
import json, sys, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import comfy_batch as CB

SIZES = {"9:16": (736, 1312), "16:9": (1312, 736), "3:4": (864, 1152), "4:3": (1152, 864), "1:1": (1024, 1024)}


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-") or "--out" not in sys.argv:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    out = Path(arg("--out")).resolve(); out.mkdir(parents=True, exist_ok=True)
    steps, seed = int(arg("--steps", 25)), int(arg("--seed", 3))
    only = set(filter(None, arg("--only", "").split(","))); redo = set(filter(None, arg("--redo", "").split(",")))
    stf = out / ".scene_state.json"; st = json.loads(stf.read_text()) if stf.exists() else {}
    tpl = json.loads((HERE.parent / "comfy/qwen_edit.api.json").read_text())
    for s in json.loads(src.read_text()):
        if only and s["id"] not in only:
            continue
        w, h = SIZES.get(s.get("ratio", "9:16")) or sys.exit(f"{s['id']}：ratio 只能是 {', '.join(SIZES)}")
        refs = [(src.parent / r).resolve() for r in s.get("refs", [])]
        if len(refs) > 10: sys.exit(f"{s['id']}：参考图最多 10 张")
        for r in refs:
            if not r.exists(): sys.exit(f"{s['id']}：找不到参考图 {r}")
        key = hashlib.sha1(json.dumps([s["prompt"], w, h, steps, seed, [hashlib.sha1(r.read_bytes()).hexdigest() for r in refs]]).encode()).hexdigest()[:12]
        dst = out / f"{s['id']}.png"
        if st.get(s["id"]) == key and dst.exists() and s["id"] not in redo:
            print(f"  {s['id']} 已有，跳过"); continue
        wf = json.loads(json.dumps(tpl))
        for i, r in enumerate(refs, 1):
            nid = f"r{i}"
            wf[nid] = {"class_type": "LoadImage", "inputs": {"image": CB.upload(r, f"scene_ref_{hashlib.sha1(r.read_bytes()).hexdigest()[:10]}{r.suffix}")}}
            wf["474"]["inputs"][f"images.image_{i}"] = [nid, 0]
        wf["474"]["inputs"]["prompt"] = s["prompt"]
        wf["456"]["inputs"].update(width=w, height=h)
        wf["458"]["inputs"].update(seed=seed, steps=steps)
        wf["461"]["inputs"]["filename_prefix"] = f"koubo/scene/{s['id']}"
        outs, took = CB.wait(CB.submit(wf), f"{s['id']} 场景图", poll=5)
        CB.fetch(outs, "461", dst)
        st[s["id"]] = key; stf.write_text(json.dumps(st, indent=1))
        print(f"  {s['id']} 完成（{took:.0f}s，{w}×{h}，参考 {len(refs)} 张）→ {dst}", flush=True)


if __name__ == "__main__":
    main()
