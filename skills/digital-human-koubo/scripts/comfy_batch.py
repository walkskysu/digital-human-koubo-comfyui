#!/usr/bin/env python3
"""口播稿 → 本地 ComfyUI 批量生成：Qwen3-TTS 克隆配音 → MiniMax H3 参考生视频（配音当 <Audio 1> fully_copy 对口型）→ 把原配音合回画面。

用法（需要 PyAV：用 ~/.venvs/comfy-mcp/bin/python 跑）：
  python comfy_batch.py script.json [--stage plan|tts|video|all] [--only s1,s3] [--redo s2] [--seed 20261112] [--steps 4] [--ratio 9:16]
  某段念错：script.json 那段加 "seed": 新数 再跑（只重做这一段，其他段缓存不受影响）

- script.json 和 build_tasks.py 同一份：[{"id","t","shot","host","lang","purpose"?}, ...]
- 主播：不写 "host" 用 annie（横屏 16:9）。要竖屏：整条片加 --ratio 9:16，或某段写 "ratio": "9:16"，
  横屏主播会换用 comfy.hosts.<host>.vertical 里的竖屏形象图；ella 本来就是竖屏自拍。
- 输出都在 script.json 同目录：
    gen/tts/<id>.flac     Qwen3-TTS 配音（音色 = persona.json → comfy.hosts.<host>.voice_ref）
    gen/raw/<id>.mp4      H3 原始输出（声音是 H3 重新合成的）
    gen/<id>.mp4          画面 + 原配音（交给 assemble.py：--src 'gen/{id}.mp4'）
    gen/prompts/<id>.txt  H3 提示词
    gen/state.json        进度；中断后重跑会跳过已完成的段，台词改了会自动重做
    ids.json              {段 id: 段 id}，给 assemble.py 用
- --stage plan：只出时长估算和预计耗时，不提交（配音前按 5.4 字/秒估；配好音后按实际时长）
- 先 --stage tts 全部配完 → 听一遍（尤其第 1 段）→ 再 --stage video。all = 两步连着跑。
- 单段配音超过 comfy.max_line_seconds（14 秒，H3 单段最多 345 帧 ≈ 14.4 秒）会报错：把台词拆短。
"""
import json, math, re, sys, time, uuid, hashlib, urllib.request, urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
P = json.loads((HERE / "persona.json").read_text())
C = P["comfy"]
URL = C["url"].rstrip("/")
LANG = {  # script.json 的 lang → (Qwen3-TTS target_language, H3 <d>[..] 标签, 提示词里的语言名)
    "Mandarin Chinese": ("Chinese", "Chinese", "Mandarin Chinese"), "Chinese": ("Chinese", "Chinese", "Mandarin Chinese"),
    "English": ("English", "English", "English"), "Japanese": ("Japanese", "Japanese", "Japanese"),
    "Korean": ("Korean", "Korean", "Korean"), "French": ("French", "French", "French"),
    "Spanish": ("Spanish", "Spanish", "Spanish"), "German": ("German", "German", "German"),
    "Italian": ("Italian", "Italian", "Italian"), "Portuguese": ("Portuguese", "Portuguese", "Portuguese"),
    "Russian": ("Russian", "Russian", "Russian"),
}
SEC_PER_FRAME_STEP = 8.1 * 60 / (243 * 4)   # 2026-11-12 实测：243 帧 × 4 步 ≈ 8.1 分钟（672×1216）


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


# ---------- ComfyUI HTTP ----------
def http(path, data=None, headers=None, timeout=60):
    req = urllib.request.Request(URL + path, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def upload(local: Path, name: str):
    """把文件放进 ComfyUI 的 input 目录（/upload/image 也收音频）。"""
    b = uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\ninput\r\n"
            f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + local.read_bytes() + f"\r\n--{b}--\r\n".encode()
    r = json.loads(http("/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={b}"}, timeout=300))
    return r["name"] if not r.get("subfolder") else f"{r['subfolder']}/{r['name']}"


def submit(wf):
    try:
        r = json.loads(http("/prompt", json.dumps({"prompt": wf, "client_id": "koubo-batch"}).encode(), {"Content-Type": "application/json"}))
    except urllib.error.HTTPError as e:
        sys.exit(f"ComfyUI 拒收（HTTP {e.code}）：{e.read().decode(errors='replace')[:800]}")
    except urllib.error.URLError as e:
        sys.exit(f"连不上 ComfyUI（{URL}）：{e.reason}。先在 Windows 上打开 ComfyUI Desktop")
    if r.get("node_errors"):
        sys.exit(f"ComfyUI 拒收：{json.dumps(r['node_errors'], ensure_ascii=False)[:800]}")
    return r["prompt_id"]


def wait(pid, label, poll=10, limit=3 * 3600):
    t0 = time.time()
    while time.time() - t0 < limit:
        h = json.loads(http(f"/history/{pid}"))
        if pid in h and h[pid].get("status", {}).get("completed") is not None:
            st = h[pid]["status"]
            if st.get("status_str") != "success":
                err = [m for m in st.get("messages", []) if m[0] == "execution_error"]
                sys.exit(f"{label} 失败：{json.dumps(err, ensure_ascii=False)[:800]}")
            return h[pid]["outputs"], time.time() - t0
        time.sleep(poll)
    sys.exit(f"{label} 超过 {limit // 60} 分钟没完成（prompt_id {pid}），去 ComfyUI 看日志")


def fetch(outputs, node, dst: Path):
    items = [x for v in outputs.get(node, {}).values() if isinstance(v, list) for x in v if isinstance(x, dict) and "filename" in x]
    if not items:
        sys.exit(f"节点 {node} 没有输出文件")
    f = items[0]
    q = urllib.parse.urlencode({"filename": f["filename"], "subfolder": f.get("subfolder", ""), "type": f.get("type", "output")})
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(http(f"/view?{q}", timeout=600))
    return dst


# ---------- 媒体 ----------
def duration(path: Path):
    import av
    with av.open(str(path)) as c:
        s = c.streams.audio[0] if c.streams.audio else c.streams.video[0]
        return float(s.duration * s.time_base) if s.duration else c.duration / 1e6


def mux(video: Path, audio: Path, out: Path):
    """画面原样拷贝 + 原配音（AAC 48k）；配音比画面短，结尾自然静音。"""
    import av
    vin, ain = av.open(str(video)), av.open(str(audio))
    o = av.open(str(out), "w")
    vs = o.add_stream_from_template(vin.streams.video[0])
    a_s = o.add_stream("aac", rate=48000)
    a_s.layout = "mono"
    for p in vin.demux(vin.streams.video[0]):
        if p.dts is None:
            continue
        p.stream = vs
        o.mux(p)
    rs = av.AudioResampler(format="fltp", layout="mono", rate=48000)
    for fr in ain.decode(audio=0):
        for f in rs.resample(fr):
            o.mux(a_s.encode(f))
    for f in rs.resample(None):
        o.mux(a_s.encode(f))
    o.mux(a_s.encode(None))
    o.close(); vin.close(); ain.close()


# ---------- 业务 ----------
def frames_for(sec):
    """H3 帧数网格是 17k+5（24fps），向上取整。"""
    n = math.ceil(sec * C["fps"])
    return n + (-(n - 5)) % 17


def est_seconds(text, lang):
    if LANG.get(lang, ("",))[0] == "Chinese":
        return len(re.sub(r"[\s，。、：；！？,.:;!?“”]", "", text)) / P["voice"]["speed_cps"]
    if re.search(r"[぀-ヿ가-힯]", text):
        return len(re.sub(r"\s", "", text)) / 7
    return len(text.split()) / 2.6


def host_of(s):
    h = s.get("host", "annie")
    if h not in C["hosts"]:
        sys.exit(f"{s['id']}：persona.json → comfy.hosts 里没有主播「{h}」")
    H = C["hosts"][h]
    ratio = s.get("ratio") or RATIO
    if ratio == "9:16" and H["size"][0] > H["size"][1]:   # 横屏主播要出竖屏：换用 vertical 里的形象图、尺寸和构图
        if not H.get("vertical"):
            sys.exit(f"{s['id']}：主播「{h}」只有横屏形象图，没有 comfy.hosts.{h}.vertical，出不了 9:16")
        H = dict(H, **H["vertical"], _variant="v")
    elif ratio == "16:9" and H["size"][0] < H["size"][1]:
        sys.exit(f"{s['id']}：主播「{h}」只有竖屏形象图，出不了 16:9（换一个横屏主播）")
    return h, H


def build_prompt(s, H, lang):
    tts_lang, tag, name = LANG[lang]
    act = P["acts"].get(s.get("shot", "full"), P["acts"]["full"])
    act = act[0].upper() + act[1:]
    purpose = s.get("purpose") or PURPOSE
    return C["prompt_template"].format(who=H["who"], look=H["look"], lang=name, voice=H["voice"], framing=H["framing"],
                                       purpose=f"speaking straight into the camera, {purpose}", shot_desc=H["shot_desc"],
                                       lang_tag=tag, line=s["t"], act=f"While talking: {act}", camera=H["camera"],
                                       pron=H["pron"], poss=H["poss"])


def key(*parts):
    return hashlib.sha1("\x00".join(map(str, parts)).encode()).hexdigest()[:12]


def save_state():
    STATE_F.write_text(json.dumps(STATE, ensure_ascii=False, indent=1))


def do_tts(s):
    sid = s["id"]; lang = s.get("lang", "Mandarin Chinese"); host, H = host_of(s)
    if lang not in LANG:
        sys.exit(f"{sid}：Qwen3-TTS 不支持 {lang}（支持 {', '.join(sorted({v[0] for v in LANG.values()}))}）")
    if not H.get("voice_ref"):
        sys.exit(f"主播「{host}」还没有 voice_ref：先录 12–20 秒干声放进 assets/，写进 persona.json → comfy.hosts.{host}")
    k = key(s["t"], lang, H["voice_ref"], H["voice_ref_text"], s.get("seed", SEED), C["tts_model"])
    out = GEN / "tts" / f"{sid}.flac"
    st = STATE.setdefault(sid, {})
    if st.get("tts_key") == k and out.exists() and sid not in REDO:
        return st["tts_sec"]
    ref_name = upload(HERE / H["voice_ref"], f"koubo_voice_{host}{Path(H['voice_ref']).suffix}")
    wf = json.loads((HERE / C["workflows"]["tts"]).read_text())
    wf["1"]["inputs"]["model_repo"] = C["tts_model"]
    wf["2"]["inputs"]["audio"] = ref_name
    wf["3"]["inputs"]["ref_text"] = H["voice_ref_text"]
    wf["4"]["inputs"].update(target_text=s["t"], target_language=LANG[lang][0], seed=s.get("seed", SEED))
    wf["9"]["inputs"]["filename_prefix"] = f"koubo/{PROJ}/tts_{sid}"
    outs, took = wait(submit(wf), f"{sid} 配音")
    fetch(outs, "9", out)
    sec = duration(out)
    heard, acc = asr_check(out, f"koubo_{PROJ}_{sid}.flac", s["t"], lang)
    st.update(tts_key=k, tts_sec=round(sec, 3), video_key=None, heard=heard, acc=acc)
    save_state()
    flag = "  ⚠ 超长，拆短这段台词再配" if sec > C["max_line_seconds"] else ""
    if acc is not None and acc < 0.9:
        flag += f"  ⚠ 回听准确率 {acc:.0%}，听一下；念错就在 script.json 这段加 \"seed\": 新数 再跑"
    print(f"  {sid} 配音 {sec:.2f}s（{took:.0f}s）回听 {'-' if acc is None else f'{acc:.0%}'}：{heard}{flag}", flush=True)
    return sec


from numcn import cn_digits  # noqa: E402  阿拉伯数字 → 中文读法


ASR_LANG = {"Chinese": "zn", "English": "en", "Japanese": "ja", "Korean": "ko"}


def asr_check(path, name, text, lang):
    """SenseVoice 不带原文提示转写配音，和稿子比。只支持中英日韩，其他语言返回 (None, None)。"""
    code = ASR_LANG.get(LANG[lang][0])
    if not code:
        return None, None
    import difflib
    up = upload(path, name)
    wf = {"1": {"class_type": "LoadAudio", "inputs": {"audio": up}},
          "2": {"class_type": "Qwen3TTSSenseVoiceASR", "inputs": {"audio": ["1", 0], "model_id": "iic/SenseVoiceSmall", "language": code}},
          "3": {"class_type": "PreviewAny", "inputs": {"source": ["2", 0]}}}
    outs, _ = wait(submit(wf), "回听", poll=2)
    heard = "".join(outs.get("3", {}).get("text", []))
    norm = lambda x: re.sub(r"[\W_]", "", cn_digits(x)).lower()
    return heard, round(difflib.SequenceMatcher(None, norm(text), norm(heard)).ratio(), 3)


def do_video(s):
    sid = s["id"]; lang = s.get("lang", "Mandarin Chinese"); host, H = host_of(s)
    st = STATE.get(sid, {}); tts = GEN / "tts" / f"{sid}.flac"
    if not tts.exists() or not st.get("tts_key"):
        sys.exit(f"{sid} 还没配音：先跑 --stage tts")
    sec = st["tts_sec"]
    if s.get("ref"):   # 这一段用合成好的场景图当参考（comfy_scene.py 出的图），替代默认形象照
        ref = (ROOT / s["ref"]).resolve()
        if not ref.exists():
            sys.exit(f"{sid}：找不到参考图 {ref}")
        # look 里常写着默认布景（如「深蓝灰墙演播室」），会把场景图的背景拉回去：换成只描述人物的 look_person
        H = dict(H, avatar=str(ref), look=s.get("look") or H.get("look_person") or H["look"], shot_desc=(
            f"A shot of <Subject 1> framed exactly as in <Picture 1>, in the same environment, background, lighting and outfit as <Picture 1>. "
            f"{H['pron'].capitalize()} looks straight into the lens with warm eye contact and a relaxed, friendly smile."))
        host = f"{host}_{hashlib.sha1(ref.read_bytes()).hexdigest()[:8]}"
    if sec > C["max_line_seconds"]:
        sys.exit(f"{sid} 配音 {sec:.2f}s 超过 {C['max_line_seconds']}s：拆短台词，重新配音")
    if H.get("_variant") and not s.get("ref"):
        host = f"{host}_{H['_variant']}"
    n = frames_for(sec + C["tail_seconds"])
    prompt = build_prompt(s, H, lang)
    w, h = H["size"]
    k = key(st["tts_key"], prompt, n, w, h, H["avatar"], host, s.get("seed", SEED), STEPS)
    out = GEN / f"{sid}.mp4"
    if st.get("video_key") == k and out.exists() and sid not in REDO:
        print(f"  {sid} 已有，跳过", flush=True)
        return
    (GEN / "prompts").mkdir(parents=True, exist_ok=True)
    (GEN / "prompts" / f"{sid}.txt").write_text(prompt)
    img = upload(HERE / H["avatar"], f"koubo_avatar_{host}{Path(H['avatar']).suffix}")
    aud = upload(tts, f"koubo_{PROJ}_{sid}.flac")
    wf = json.loads((HERE / C["workflows"]["video"]).read_text())
    wf["136"]["inputs"].update(prompt=prompt, width=w, height=h, length=n)
    wf["137"]["inputs"]["image"] = img
    wf["200"]["inputs"]["audio"] = aud
    wf["129"]["inputs"]["noise_seed"] = s.get("seed", SEED)
    wf["124"]["inputs"]["steps"] = STEPS
    wf["92"]["inputs"]["filename_prefix"] = f"koubo/{PROJ}/video_{sid}"
    print(f"  {sid} 提交视频：{n} 帧 ≈ {n / C['fps']:.2f}s，{w}×{h}，{STEPS} 步，预计 {n * STEPS * SEC_PER_FRAME_STEP / 60:.0f} 分钟", flush=True)
    outs, took = wait(submit(wf), f"{sid} 视频", poll=20)
    raw = fetch(outs, "92", GEN / "raw" / f"{sid}.mp4")
    mux(raw, tts, out)
    st.update(video_key=k, frames=n, video_min=round(took / 60, 1))
    save_state()
    print(f"  {sid} 完成（{took / 60:.1f} 分钟）→ {out.relative_to(ROOT)}", flush=True)


def free_vram():
    try:
        http("/free", json.dumps({"unload_models": True, "free_memory": True}).encode(), {"Content-Type": "application/json"})
    except Exception as e:
        print(f"  （释放显存失败，继续：{e}）")


def plan(S):
    total_min, rows = 0, []
    for s in S:
        st = STATE.get(s["id"], {})
        sec = st.get("tts_sec") or est_seconds(s["t"], s.get("lang", "Mandarin Chinese"))
        n = frames_for(sec + C["tail_seconds"])
        m = n * STEPS * SEC_PER_FRAME_STEP / 60 * (lambda w, h: w * h / (672 * 1216))(*host_of(s)[1]["size"])
        total_min += m
        warn = " ⚠ 超长，拆短" if sec > C["max_line_seconds"] else ""
        rows.append(f"  {s['id']:5s} {'实测' if st.get('tts_sec') else '估算'} {sec:5.2f}s → {n} 帧  约 {m:4.1f} 分钟{warn}")
    print("\n".join(rows))
    print(f"{len(S)} 段 · 视频预计 {total_min:.0f} 分钟（{total_min / 60:.1f} 小时）· 配音每段约 0.5–1 分钟 · 不花积分，占用本机 GPU")


def main():
    global ROOT, GEN, STATE_F, STATE, PROJ, SEED, STEPS, REDO, RATIO, PURPOSE
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    ROOT = src.parent; GEN = ROOT / "gen"; GEN.mkdir(exist_ok=True)
    STATE_F = GEN / "state.json"
    STATE = json.loads(STATE_F.read_text()) if STATE_F.exists() else {}
    PROJ = re.sub(r"[^\w-]", "_", ROOT.name)[:40] or "koubo"
    SEED, STEPS = int(arg("--seed", 20261112)), int(arg("--steps", 4))
    REDO = set(filter(None, arg("--redo", "").split(",")))
    RATIO = arg("--ratio")   # 9:16 / 16:9；不写就按主播形象图自己的画幅
    PURPOSE = arg("--purpose", "like a friendly Chinese tech vlogger explaining clearly")
    stage = arg("--stage", "all")
    S = json.loads(src.read_text())
    only = set(filter(None, arg("--only", "").split(",")))
    if only:
        S = [s for s in S if s["id"] in only]
    if stage == "plan":
        return plan(S)
    if stage in ("tts", "all"):
        print(f"== 配音 {len(S)} 段", flush=True)
        for s in S:
            do_tts(s)
    if stage in ("video", "all"):
        long_ = [s["id"] for s in S if STATE.get(s["id"], {}).get("tts_sec", 0) > C["max_line_seconds"]]
        if long_:
            sys.exit(f"这些段配音超过 {C['max_line_seconds']}s，先拆短：{', '.join(long_)}")
        free_vram()   # 先卸掉 TTS 模型，给 H3 腾显存
        print(f"== 视频 {len(S)} 段", flush=True)
        for s in S:
            do_video(s)
    full = json.loads(src.read_text())
    (ROOT / "ids.json").write_text(json.dumps({s["id"]: s["id"] for s in full}, ensure_ascii=False, indent=1))
    print("完成。拼接：python3 scripts/assemble.py script.json ids.json --src 'gen/{id}.mp4'")


if __name__ == "__main__":
    main()
