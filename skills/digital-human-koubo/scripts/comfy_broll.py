#!/usr/bin/env python3
"""B-roll 批量生成（本地 ComfyUI · MiniMax H3，替代 Renoise Wan 3.0）。
用法：python3 comfy_broll.py broll.json --out <工程>/public/broll [--stage plan|run] [--only B01,B03] [--redo B02] [--mp 0.8] [--steps 8] [--seed 7]

broll.json：[{"id": "B01", "sec": 5, "scene": "…", "camera": "…", "sound": "…", "image": "可选首帧.png", "prompt": "可选：整段 H3 提示词，写了就不拼"}, …]
- scene：具体场景 + 人物动作 + 光线（英文；中国场景写 Chinese city street / red yuan banknotes；人物写普通路人，不写名人）
- camera：镜头运动，按 H3 写法，例如 "The camera pushes in with small amplitude at slow speed toward …"（不写默认缓慢推近）
- sound：环境声（B-roll 在成片里是静音的，写不写都行）
- image：有首帧就走图生视频（I2VA，比如用 Qwen Image 2.1 先出一张图）；没有就是文生视频（T2VA）
- sec：默认 5；画面比场景短时 Lin 模板会自动放慢到 0.55 倍，场景超过 9 秒就拆两个 B-roll
输出 <out>/<id>.mp4（16:9，24fps，带 H3 生成的环境声），提示词存 <out>/prompts/<id>.txt，进度存 <out>/.broll_state.json（改了内容才重做）。
默认 0.8MP（1216×672）、8 步 Lightning；5 秒一段约 5–6 分钟（RTX 3090 实测）。
提示：带招牌的街景 H3 会画出乱码汉字。要么写 "shop signs are blurred and out of focus"，要么挑没有招牌的画面（手部特写、俯拍、自然景）。--mp 0.4（864×480）约快一倍，铺满 1080p 会软一些。
"""
import json, math, sys, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import comfy_batch as CB   # upload / submit / wait / fetch / frames_for，ComfyUI 地址读 persona.json

SIZES = {0.4: (864, 480), 0.5: (960, 544), 0.6: (1056, 608), 0.7: (1152, 640), 0.8: (1216, 672), 0.9: (1280, 736)}
SEC_PER_FRAME_STEP_08MP = 5.3 * 60 / (124 * 8)   # 2026-11-12 实测：文生 5 秒 / 1216×672 / 8 步 = 5.3 分钟
NO_TEXT = "No readable text, no logos, no watermarks, no subtitles, no on-screen captions."


def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


def build_prompt(b):
    if b.get("prompt"):
        return b["prompt"]
    camera = b.get("camera") or "The camera pushes in with small amplitude at slow speed."
    body = (f"integrated_multimodal_description: [Shot 1] Live-action, cinematic documentary B-roll, {b['scene'].rstrip('.')}. "
            f"{camera.rstrip('.')}. Natural color grading, shallow depth of field, a single continuous shot with no cuts. {NO_TEXT}\n\n"
            f"overall_soundscape: {b.get('sound') or 'Quiet natural ambience that matches the scene, no voices.'}\n\n"
            f"non_diegetic_music: None.")
    if b.get("image"):
        return "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\n" + body
    return body


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-") or "--out" not in sys.argv:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    out = Path(arg("--out")).resolve(); out.mkdir(parents=True, exist_ok=True)
    mp = float(arg("--mp", 0.8)); w, h = SIZES.get(mp) or sys.exit(f"--mp 只能是 {sorted(SIZES)}")
    steps, seed = int(arg("--steps", 8)), int(arg("--seed", 7))
    only = set(filter(None, arg("--only", "").split(","))); redo = set(filter(None, arg("--redo", "").split(",")))
    B = [b for b in json.loads(src.read_text()) if not only or b["id"] in only]
    stf = out / ".broll_state.json"; st = json.loads(stf.read_text()) if stf.exists() else {}
    per_min = lambda n: n * steps * SEC_PER_FRAME_STEP_08MP * (w * h) / (1216 * 672) / 60
    if arg("--stage", "run") == "plan":
        tot = 0
        for b in B:
            n = CB.frames_for(b.get("sec", 5)); m = per_min(n); tot += m
            print(f"  {b['id']:5s} {'图生' if b.get('image') else '文生'} {b.get('sec', 5)}s → {n} 帧  约 {m:4.1f} 分钟")
        print(f"{len(B)} 段 · {w}×{h} · {steps} 步 · 预计 {tot:.0f} 分钟（{tot / 60:.1f} 小时）· 不花积分，占用本机 GPU")
        return
    tpl = json.loads((HERE.parent / "comfy/h3_i2v.api.json").read_text())
    for b in B:
        bid, sec = b["id"], b.get("sec", 5)
        if sec > 15: sys.exit(f"{bid}：H3 单段最多 15 秒")
        n = CB.frames_for(sec)
        prompt = build_prompt(b)
        img = (src.parent / b["image"]).resolve() if b.get("image") else None
        key = hashlib.sha1(json.dumps([prompt, n, w, h, steps, seed, img and img.read_bytes().hex()[:4096]]).encode()).hexdigest()[:12]
        dst = out / f"{bid}.mp4"
        if st.get(bid) == key and dst.exists() and bid not in redo:
            print(f"  {bid} 已有，跳过"); continue
        (out / "prompts").mkdir(exist_ok=True); (out / "prompts" / f"{bid}.txt").write_text(prompt)
        wf = json.loads(json.dumps(tpl))
        if img:
            wf["114"]["inputs"]["image"] = CB.upload(img, f"broll_{key}{img.suffix}")
        else:
            del wf["114"]; del wf["131"]["inputs"]["first_frame"]
        wf["131"]["inputs"].update(prompt=prompt, width=w, height=h, length=n)
        wf["124"]["inputs"]["steps"] = steps
        wf["129"]["inputs"]["noise_seed"] = seed
        wf["92"]["inputs"]["filename_prefix"] = f"koubo/broll/{bid}"
        print(f"  {bid} 提交（{'图生' if img else '文生'}，{n} 帧 ≈ {n / 24:.2f}s，{w}×{h}，{steps} 步，预计 {per_min(n):.0f} 分钟）", flush=True)
        outs, took = CB.wait(CB.submit(wf), f"{bid} B-roll", poll=20)
        CB.fetch(outs, "92", dst)
        st[bid] = key; stf.write_text(json.dumps(st, indent=1))
        print(f"  {bid} 完成（{took / 60:.1f} 分钟）→ {dst}", flush=True)
    print("完成。plan.json 里 broll 场景写 \"clip\": \"<id>\"，clipLen 写实际秒数（不写按 5 秒算）。")


if __name__ == "__main__":
    main()
