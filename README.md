<div align="center">

# Digital Human Koubo · ComfyUI Local Edition

**One photo + one script → a lip-synced digital-human talking-head video, generated entirely on your own GPU.**
Voice cloning, lip sync, scenes, B-roll, music, captions and pro-YouTuber-style packaging — driven by your AI agent through **local ComfyUI**. No credits, no API keys.

**English** · [简体中文](README.zh-CN.md)

<sub>Based on <a href="https://github.com/andyhuo520/digital-human-koubo">andyhuo520/digital-human-koubo</a> by Berryxia — this version adds a fully local ComfyUI route.</sub>

[![Local ComfyUI](https://img.shields.io/badge/generation-local%20ComfyUI-3b5bdb)](https://github.com/comfyanonymous/ComfyUI)
![Tested on RTX 3090](https://img.shields.io/badge/tested-RTX%203090%2024GB-76b900)
![Open models](https://img.shields.io/badge/models-MiniMax%20H3%20·%20Qwen3--TTS%20·%20Qwen%20Image%202.1-6e40c9)
[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](LICENSE)
![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-orange)
![Remotion](https://img.shields.io/badge/edit-Remotion%204-0b84f3)

<img src="docs/images/local-cover.jpg" width="880" alt="Covers of the five videos made with the local ComfyUI route">

</div>

> **Everything in the videos above was generated on one RTX 3090** — voice, lip-synced presenter, scene images, B-roll, music and sound effects:
> **Qwen3-TTS** clones the presenter's voice → **MiniMax H3** generates the presenter *from that audio* so the lips match → **Qwen Image 2.1** makes scenes → **MiniMax Music 3** writes the BGM → **earshot** adds sound effects → **Remotion** edits and packages.
> Jump to: [Local demos](#local-demos) · [Install](docs/INSTALL.md) · [ComfyUI workflows](#comfyui-workflows) · [Quick start](#quick-start)
>
> The original cloud route ([Renoise MCP](#cloud-route-renoise-mcp-optional): Grok Video, GPT Image, Wan) is still included — choose per video.

---

## Local demos

One short video per editing style, all made end to end with the local route on an RTX 3090 (each ~40-second video took roughly 40–70 minutes of GPU time). Click a GIF or "Watch" for the full video.

<div align="center">
<a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4"><img src="docs/gifs/local-b-five-styles.gif" width="270"></a><br>
<b>Style B · Talking head with animated captions</b> · 9:16 · 44 s · 8 segments<br>
"One photo, five kinds of talking-head video" — selfie-vlog and full shots, captions, emoji, picture-in-picture<br>
<a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4">▶ Watch</a>
</div>

| | |
|:---:|:---:|
| <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4"><img src="docs/gifs/local-a-72-rule.gif" width="400"></a> | <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4"><img src="docs/gifs/local-c-h3-launch.gif" width="400"></a> |
| **Style A · Finance explainer** · 16:9 · 35 s<br>"The rule of 72": text behind the presenter, boards + presenter PiP, bar chart, H3 B-roll<br>[▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4) | **Style C · Launch breakdown** · 16:9 · 41 s<br>"MiniMax H3: picture and sound together" — presenter on the side, spec cards<br>[▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4) |
| <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4"><img src="docs/gifs/local-d-tutorial.gif" width="400"></a> | <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4"><img src="docs/gifs/local-e-relay.gif" width="400"></a> |
| **Style D · Step-by-step tutorial** · 16:9 · 44 s<br>"Three steps to a local talking-head video" — terminal, timeline, step tracker<br>[▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4) | **Style E · Two-host relay** · 16:9 · 37 s<br>"3 traps on Double 11" — two presenters, a Qwen Image scene, one line in English<br>[▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4) |

> All presenters are AI digital humans (`assets/host_girl_*.png` and the voice samples are AI-generated, not real people), and every video carries the label "内容由 AI 数字人演绎" (performed by an AI digital human). Demos of the original cloud route are further down under [Cloud route](#cloud-route-renoise-mcp-optional).

---

## Install (local ComfyUI route)

Full steps are in **[docs/INSTALL.md](docs/INSTALL.md)**: getting the code, installing the skills into your agent, the ComfyUI node pack and model list, the Python side and local tools, your presenter's voice, earshot and placeholder audio. Afterwards run `bash ~/.claude/skills/digital-human-koubo/scripts/doctor.sh`; it lists anything missing.

---

## ComfyUI workflows

### The local route, step by step

The cloud route makes the picture first and takes the voice from the video model. The local route goes the **other way round: voice first, then picture**. The TTS clip is fed to MiniMax H3 as `<Audio 1>` with `fully_copy`, so the mouth is generated *from* the final audio. Lip sync is exact even with a cloned voice, and nothing has to be re-voiced afterwards.

```
script.json ─► comfy_batch.py --stage plan     estimate GPU time per segment
            ─► comfy_batch.py --stage tts      Qwen3-TTS clones the host's voice_ref (12–20 s dry voice + text)
                                               └► SenseVoice transcribes without the script; < 90 % match → ⚠
                                                  fix: add "seed": <n> to that segment and re-run (only it is redone)
            ─► comfy_batch.py --stage video    MiniMax H3 Reference-to-Video, 4-step Lightning LoRA
                                               <Picture 1> = host photo or scene image ("ref")
                                               <Audio 1>   = the TTS clip, fully_copy → lip sync
                                               prompt in H3 Ref2VA format → gen/prompts/<id>.txt
                                               progress in gen/state.json (resumable; only changed segments redo)
            ─► assemble.py --src 'gen/{id}.mp4' → align.py → tl.json → Remotion → loudnorm → cover
side jobs:   comfy_scene.py  (Qwen Image 2.1 t2i, host photo as reference: livestream room / shop / street, 4-view, stickers)
             comfy_broll.py  (H3 text- or image-to-video B-roll, 16:9)
             comfy_music.py  (MiniMax Music 3 instrumental BGM → check with `earshot describe`)
             cutout_video.py (BiRefNet mask for text-behind-presenter on Linux / Windows)
             face_center.py  (mediapipe face position for framing in Style A)
```

### UI-format workflows (`workflows/`)

Drag a file onto the ComfyUI canvas (or *Workflow → Open*) to inspect or run it by hand. Image / audio inputs are set to `example.png` / `example.flac`; load your own. Details and the exact changes for each API version: [`workflows/README.md`](workflows/README.md).

| Workflow | What it does | API version used by the skill |
|---|---|---|
| [`qwen3_tts_voice_clone.json`](workflows/qwen3_tts_voice_clone.json) | Qwen3-TTS voice clone from a reference clip + SenseVoice ASR | `comfy/tts_clone.api.json` |
| [`qwen3_tts_voice_design.json`](workflows/qwen3_tts_voice_design.json) | design a new voice from a text description | — (used once to make the sample voices) |
| [`video_minimax_h3_r2v_3ref.json`](workflows/video_minimax_h3_r2v_3ref.json) | MiniMax H3 Reference-to-Video, 4-step Lightning LoRA | `comfy/h3_r2v_audio.api.json` (one image + TTS audio as `<Audio 1>`) |
| [`video_minimax_h3_i2v.json`](workflows/video_minimax_h3_i2v.json) | MiniMax H3 Image-to-Video, 8-step Lightning LoRA | `comfy/h3_i2v.api.json` (text-to-video when no first frame) |
| [`image_qwen_image_2_1_t2i.json`](workflows/image_qwen_image_2_1_t2i.json) | Qwen Image 2.1 text-to-image, optional prompt enhancer | `comfy/qwen_t2i.api.json` (+ reference images) |
| [`audio_minimax_music_3.json`](workflows/audio_minimax_music_3.json) | MiniMax Music 3 song / instrumental | `comfy/music.api.json` |
| [`birefnet_remove_background.json`](workflows/birefnet_remove_background.json) | BiRefNet person / background mask | built inside `scripts/cutout_video.py` (on video, 8 s chunks) |

### API-format graphs the scripts submit (`skills/digital-human-koubo/comfy/`)

Flattened API-format graphs. The scripts load them, fill in text / images / audio / seed and submit them to ComfyUI's REST API (`/upload`, `/prompt`, `/history`, `/view`). The address is `comfy.url` in `persona.json` (default `http://127.0.0.1:8188`).

| File | Used by | Main nodes | Model files |
|---|---|---|---|
| `tts_clone.api.json` | `comfy_batch.py` | `Qwen3TTSLoader` · `Qwen3TTSVoiceClonePrompt` · `Qwen3TTSVoiceClone` | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` (downloaded by the node pack) |
| `h3_r2v_audio.api.json` | `comfy_batch.py` | `MiniMaxH3ReferenceToVideo` · `SamplerCustomAdvanced` · `CreateVideo` | `minimax_h3_ref2va_pruned_int8_convrot` · LoRA `minimax_h3_ref2v_turbo_4step_v0.1` · text encoder `qwen3vl_32b_minimax_h3_nvfp4_awq` · VAEs `minimax_h3_video_vae_int8_convrot`, `minimax_h3_audio_vae_fp32` |
| `h3_i2v.api.json` | `comfy_broll.py` | `MiniMaxH3ImageToVideo` | `minimax_h3_fl2va_pruned_int8_convrot` · LoRA `minimax_h3_fl2v_turbo_8step_v1.0` · same text encoder and VAEs |
| `qwen_t2i.api.json` | `comfy_scene.py` | `TextEncodeQwenImage21` · `QwenImage21Cache` · optional prompt enhancer `TextGenerate` | `qwen_image_2.1_int8_convrot` · `qwen3vl_8b_int8_convrot` · `qwen_image_2.1_vae_bf16` · enhancer `qwen3.5_9b_qwen_image_2.1_pe_t2i.int8_convrot` (only with `--enhance`) |
| `music.api.json` | `comfy_music.py` | `MiniMaxMusic3TextEncode` · `EmptyMiniMaxMusic3LatentAudio` · `KSampler` | `minimax_music3_dit_fp16` · `minimax_music3_text_encoder_pruned_int8_convrot` · `minimax_music3_dav` |
| *(built in script)* | `cutout_video.py` | `LoadBackgroundRemovalModel` · `RemoveBackground` | `birefnet.safetensors` |
| *(built in script)* | `comfy_batch.py` | `Qwen3TTSSenseVoiceASR` | `iic/SenseVoiceSmall` (downloaded by the node pack) |

### Presenters for the local route

`persona.json → comfy.hosts` defines each local presenter: photo (`avatar`), output size, voice sample (`voice_ref` + `voice_ref_text`), English appearance text for the prompt (`look`, plus `look_person` without the studio for use with scene images), voice description and default framing. Two are included: `tank` (the default white-tank-top host, `assets/avatar_ref.jpg`) and `girl` (`assets/host_girl_*.png`). The `girl` images and both voice samples (`assets/voice_ref_*.flac`) are AI-generated, not real people. The H3 prompt template is `comfy.prompt_template` (Ref2VA format: subject_definitions / summary / retention_analysis / detailed_description / soundscape / music).

### GPU time (RTX 3090 24 GB, real runs)

No credits; the cost is GPU time.

| Job | Setting | Time |
|---|---|---|
| Voice clone (Qwen3-TTS) | one 5–14 s line | seconds |
| Presenter segment (H3 Ref2VA) | 10 s, 672×1216 or 1216×672, 4 steps | ~8 min (4–9 min) |
| Scene image (Qwen Image 2.1) | 25 steps | 25–50 s (first one with model loading up to ~5 min) |
| B-roll (H3 T2VA / I2VA) | 5 s, 1216×672, 8 steps | 5–6 min |
| BGM (MiniMax Music 3) | 35–50 s instrumental, 30 steps | 1–2 min |

A ~40-second finished video (5–8 presenter segments) takes roughly 40–70 minutes of GPU time.

---

## Quick start

Talk to your agent in plain language. Below are a few requests per editing style; the first one in each group is how the matching [local demo](#local-demos) was made. Saying "local ComfyUI" picks the local route; if you don't, the skill still defaults to local when 127.0.0.1:8188 is up.

**A · Explainer** (16:9, finance / tech events)

```text
Use local ComfyUI for a Xiaolin-style explainer on the rule of 72 (how long until your money doubles), 16:9, 35 seconds. Open with text behind the presenter, put the worked example on a board with a presenter window, host girl.
Use local ComfyUI: explain compound vs. simple interest in the Xiaolin style, 1 minute, with two B-roll shots in the middle.
Make a local explainer: why does a 1% annual fee eat a third of your returns? Add comparison bars and a worked example, and generate the BGM with MiniMax Music.
```

**B · Influencer talking head with animated captions** (9:16, picks / reviews / rants)

```text
Use local ComfyUI for a 9:16 captioned talking head, host tank, 45 seconds: five talking-head styles from one photo and one GPU, lively captions.
Use local ComfyUI: a 40-second 9:16 talking-head video about the rule of 72, with animated captions.
Make a local 30-second vertical review: I've used these noise-cancelling earbuds for three months, three pros and one con, standard captions, end by asking viewers to comment.
```

**C · Launch breakdown** (16:9, new products / models)

```text
Use local ComfyUI for a launch breakdown: MiniMax H3 is open source and generates picture and sound together, 40 seconds, presenter at the side, with spec cards.
Make a local 45-second launch breakdown: Qwen3-TTS clones a voice from a dozen seconds of audio; three highlights and one limitation.
This model just launched. Use local ComfyUI for a 1-minute breakdown: what's new in one line, three key specs, measured speed, and who it's for.
```

**D · Step-by-step tutorial** (16:9, "how to…")

```text
Use local ComfyUI for a step-by-step tutorial: make a talking-head video on your own PC in three steps (clone the voice → generate the video → edit), 16:9, 45 seconds, host girl.
Make a local tutorial: installing the Lightning LoRA in ComfyUI in four steps, with terminal footage and a step tracker for each.
Make a 1-minute local tutorial teaching beginners to change the presenter's background with Qwen Image, with a timeline and numbered steps.
```

**E · Multi-host · multi-language · multi-scene** (16:9, relays / going global)

```text
用本地 ComfyUI 做，不花积分：两个主播接力讲双 11 的三个坑，16:9，40 秒。 (local ComfyUI, no credits: two hosts take turns on three Singles' Day shopping traps)
girl and tank take turns on three renting traps: put girl in a Qwen Image apartment-complex scene for the second one, and have tank do the third in English.
A bilingual product intro: girl opens in Chinese, tank covers three selling points in English, girl wraps up, 16:9, 50 seconds.
```

**General**

```text
用我的数字人 Skill 讲这段：……（paste your content）
Generate the BGM with MiniMax Music and redo the sound effects with earshot.
Add a map route when she mentions these countries. / Put "¥99" behind her. / Add a teaser cold open.
把包装组件图鉴发我看看  (show me the packaging gallery)
```

What happens next:
1. Setup check — anything already installed is skipped.
2. A one-line diagnosis + 2 recommended styles with preview images, and one round of questions.
3. Script + scene design + **GPU-time estimate** (local) or **credit quote** (cloud) → you approve → segment 1 → you approve → the rest.
4. QA, voice clean-up, editing with the style's default packaging → the finished MP4 with its cover as the first frame.

---

## What it does

- **Two generation engines, one pipeline** — generate locally with **ComfyUI** (Qwen3-TTS, MiniMax H3, Qwen Image 2.1, MiniMax Music 3, BiRefNet) or in the cloud with **Renoise MCP** (Grok Video 1.5, GPT Image 2.5, Wan 3.0). Scripting, QA, editing, packaging and covers are the same for both; just say *"use local ComfyUI"*.
- **Digital human from one photo** — a fixed presenter (face, outfit, voice, prompt template) stored in `persona.json`, so every video is the same person. Composite her into any scene (livestream studio, shop, classroom, street) first, then make her talk.
- **Voice-first lip sync (local)** — the cloned voice drives MiniMax H3, so the mouth matches the final audio exactly. Lines are split into ≤ 14-second segments.
- **Cost gate** — the agent always quotes segments · seconds · GPU time (or credits) first and waits for your "yes". It generates segment 1 for you to check before batching the rest.
- **Quality control** — every line is transcribed (SenseVoice / whisper) *without* the script and compared with it, so misreads are caught; 4 frames per segment are inspected.
- **Voice unification** — 1/3-octave spectral matching, de-essing, one shared small-room reverb and loudness normalisation, so separately generated clips sound like one recording (sibilance spread 13.2 dB → 5.9 dB in our tests).
- **5 editing styles, chosen for your content** — the agent diagnoses your content, recommends 2 styles with preview images and asks you everything in one go (style · ratio & length · caption intensity · presenter).
- **48 packaging components** — measured frame-by-frame from 25 videos by top creators (MrBeast, Mark Rober, Ryan Trahan, MKBHD, MediaStorm/影视飓风, 何同学, Johnny Harris, Vox, Kurzgesagt, 回形针, 半佛仙人, 差评, 毕导). Each style has a default packaging recipe; add or remove techniques by just asking.
- **Text behind the presenter** — big words / numbers between the background and the person (BiRefNet on Linux / Windows, Apple Vision on macOS → 3-layer composite).
- **Cover as the first frame** — every video gets a cover by default (16:9 / 9:16 / 3:4: presenter frame + hook headline + evidence cards), spliced in as the first 0.5 s. Platforms use the first frame as the thumbnail, so there is nothing to upload separately.
- **Multi-language** — English, Japanese, Korean, French, Spanish, Arabic tested (back-check 94–100 %).
- **Works with your agent** — a standard `SKILL.md` Agent Skill plus scripts; any agent that can load skills and run local commands can drive the local route.

## How it works

```
your content ──► 0. setup check (ComfyUI / ffmpeg / whisper — skip what you already have)
                 1. diagnose content → recommend 2 of 5 styles → ask once → brief.json
                 2. script.json (≤14 s per segment locally / ≤15 s cloud, ~5.4 Chinese chars/s)
                 3. estimate / quote → wait for "yes" → generate segment 1 → you check → batch
                 4. voice → lip-synced video (local) or download (cloud) → back-check → frame check
                 5. voice unification (spectral match + de-ess + shared room)
                 6. word-level timeline (tl.json)
                 7. edit in Remotion: style template + default packaging (+ your requests)
                 8. render → check mid-transition frames → loudness (-14 / -16 LUFS)
                 9. cover: pick a presenter frame → 16:9 / 9:16 / 3:4 → splice in as the first frame (0.5 s)
```

## Architecture

The skill is four layers. The agent reads `SKILL.md` and drives everything else through scripts; only the **generation layer** changes between the local and the cloud route.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Agent + SKILL.md     diagnose → brief.json → script.json → ask / quote   │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 2a. Local generation (ComfyUI API)   │ 2b. Cloud generation (Renoise MCP)   │
│   Qwen3-TTS        voice clone       │   Grok Video 1.5  presenter + voice  │
│   MiniMax H3 R2V   lip sync to voice │   GPT Image 2.5   scenes / 4-view    │
│   Qwen Image 2.1   scenes / 4-view   │   Wan 3.0         B-roll             │
│   MiniMax H3 T2V/I2V  B-roll         │   MiMo TTS        optional voice     │
│   MiniMax Music 3  BGM               │   make_assets.py  placeholder BGM    │
│   BiRefNet         person cutout     │   Apple Vision    person cutout      │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ 3. QA + timeline     SenseVoice / whisper back-check · frame check ·        │
│                      assemble.py (drift-safe concat) · align.py → tl.json   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Edit + finish     Remotion templates (huazi-916 · lin-169 · reference/*) │
│                      48 packaging components · earshot SFX · BGM ducking    │
│                      loudness -14/-16 LUFS · make_cover → cover_first       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Components by step

| Step | Local route | Cloud route | Script |
|---|---|---|---|
| Voice | **Qwen3-TTS 1.7B Base** voice clone | Grok native voice · optional Xiaomi MiMo TTS | `comfy_batch.py --stage tts` |
| Voice QA | **SenseVoice Small** (inside ComfyUI) + whisper.cpp | whisper.cpp | `comfy_batch.py`, `misread_check.py` |
| Presenter video | **MiniMax H3 Ref2VA** + 4-step Lightning LoRA | Grok Video 1.5 (Renoise) | `comfy_batch.py --stage video` / `build_tasks.py` |
| Scene image, 4-view, stickers | **Qwen Image 2.1** (host photo as reference) | GPT Image 2.5 (Renoise) | `comfy_scene.py` |
| B-roll | **MiniMax H3** T2VA / I2VA + 8-step Lightning LoRA | Wan 3.0 (Renoise) | `comfy_broll.py` |
| Background music | **MiniMax Music 3** | placeholder from `make_assets.py` | `comfy_music.py` |
| Sound effects | **earshot** kit | `make_assets.py` (synthesised) / earshot kit | `lin_sfx.py` |
| Person cutout | **BiRefNet** (ComfyUI) | Apple Vision (macOS) | `cutout_video.py` |
| Face position | **mediapipe** BlazeFace | Apple Vision (macOS) | `face_center.py` |
| Concat, timeline, edit, cover | ffmpeg · whisper.cpp · Remotion 4 · Playwright | same | `assemble.py` · `align.py` · templates · `make_cover.py` |

---

## Supported agents

The skill is a folder with a `SKILL.md` (the open Agent Skills format) plus Python / shell / Remotion scripts. The **local route** needs an agent that can **load Agent Skills** and **run commands on your computer**. The cloud route additionally needs a **remote MCP connection** (Renoise).

| Agent | Skills | Local commands | Renoise MCP (cloud route) | Status |
|---|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | ✅ | `/plugin` (below) | ✅ Tested — the local route was built with it |
| **Codex** (CLI / desktop) | `~/.codex/skills/` | ✅ | `codex mcp add` | ✅ Expected to work (same scripts) |
| **OpenClaw** | skills folder per OpenClaw docs | ✅ | `openclaw plugins install` | ⚙️ Should work |
| **WorkBuddy** | Skills → import the folder / zip | ✅ desktop agent | Connectors → add custom MCP | ⚙️ Should work — menu names may differ by version |
| **豆包 (Doubao)** · **千问办公 (Qwen Office)** · **纳米Work (NamiWork)** and other agent products | import if the product supports Agent Skills | needed | add as a custom / remote MCP server if supported | ⚙️ Works if the product meets the requirements above; check its docs |
| **Claude desktop / claude.ai** | upload the skill zip in Settings | ⚠️ sandbox only | Connectors → Add custom connector | Cloud route planning & generation only; local route and editing need a shell agent |

---

## Cloud route (Renoise MCP, optional)

The original cloud route still works and can be mixed with the local one per video.

<p align="center"><img src="docs/images/cover.jpg" width="820" alt="One photo + one sentence → a 27-second livestream sales ad"></p>

> This 27-second livestream ad has no real presenter. Face, voice, studio, captions and the price animation are all AI.
> The only input was one sentence: *"Use this digital human to make a 30-second livestream ad for the WorkBuddy course — 10 lessons, ¥99, was ¥999."*
> Total cost: **482 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) credits**.

### Cloud-route demos (from the original project)

| | | |
|:---:|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4"><img src="docs/gifs/workbuddy-live-ad.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4"><img src="docs/gifs/renoise-koubo-huazi.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4"><img src="docs/gifs/text-behind.gif" width="300"></a> |
| **Livestream sales ad** · 9:16 · 27 s<br>Style B + depth-text price ¥999→¥99<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4) | **Product recommendation** · 9:16 · 89 s<br>Animated captions, emoji, picture-in-picture<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4) | **Text behind the presenter** · 5 s<br>Vision person matting, 3-layer composite<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4) |

| | |
|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4"><img src="docs/gifs/tutorial-ep2.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4"><img src="docs/gifs/tutorial-digital-human-upgrade.gif" width="400"></a> |
| **Step-by-step tutorial** · 16:9 · 4:36<br>The digital human teaches how she was made (Style D)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4) | **Digital human, upgraded** · 16:9 · 5:55<br>Two presenters, 6 languages, 4 scenes, cat & dog (Style E)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4) |
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4"><img src="docs/gifs/memt-launch.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4"><img src="docs/gifs/xiaolin-style-explainer.gif" width="400"></a> |
| **Launch breakdown** · 16:9 · 39 s<br>Presenter on the side, code B-roll on the right (Style C)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4) | **Finance / tech explainer** · 16:9 · 2:21<br>Charts, documents, chapter cards (Style A)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4) |

> These presenters are AI digital humans; the male presenter is the original author's own digital twin, made from his own photo.

### Connect Renoise MCP

Create an account at **[renoise.ai](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)** first. Login is in the browser — you never paste an API key.

| Agent | How |
|---|---|
| Claude Code | `/plugin marketplace add ArcoCodes/renoise-plugins-official` then `/plugin install renoise@renoise-plugins-official` |
| Codex | `codex mcp add renoise --url https://renoise.ai/api/public/mcp` then `codex mcp login renoise` |
| OpenClaw | `openclaw plugins install renoise --marketplace ArcoCodes/renoise-plugins-official` |
| Claude desktop / claude.ai | Settings → Connectors → **Add custom connector** → name `Renoise`, URL `https://renoise.ai/api/public/mcp` |
| WorkBuddy, Cursor, Windsurf, Cline, 豆包, 千问, 纳米Work, … | add a remote MCP server with URL `https://renoise.ai/api/public/mcp` (typical config: `{"mcpServers":{"renoise":{"url":"https://renoise.ai/api/public/mcp"}}}`) |

Latest official instructions: **[renoise.ai/plugin](https://renoise.ai/plugin)**. Check it worked by asking your agent: *"查一下我的 Renoise 余额 / check my Renoise balance."*

### (Optional) Xiaomi MiMo TTS — designed or cloned voices

On the cloud route the default voice is Grok's native voice (best lip-sync). For a designed voice, your own cloned voice, or narration-only videos, the skill uses **Xiaomi MiMo TTS**:

1. Register at **[platform.xiaomimimo.com](https://platform.xiaomimimo.com/)** and create an API key. At the time of writing Xiaomi offered the TTS models free for a limited time — check the site for current pricing.
2. Put the key in an environment variable, or in `~/.config/ai-teardown/mimo.env`:
   ```bash
   mkdir -p ~/.config/ai-teardown && cat > ~/.config/ai-teardown/mimo.env <<'EOF'
   MIMO_API_KEY=your-key-here
   MIMO_BASE_URL=https://api.xiaomimimo.com/v1
   EOF
   chmod 600 ~/.config/ai-teardown/mimo.env
   ```
3. Only clone **your own** voice or a voice you have explicit permission to use.

> Note: Grok generates lip movement from its own voice. Swapping in a different voice afterwards leaves ~100 ms lip offset (fine in picture-in-picture, visible in full-screen close-ups). The local route avoids this by generating the lips from the cloned voice.

### Make your own digital human (cloud route)

1. Pick a photo: frontal face, even light, hair off the face, mouth closed. **Only your own photo or one you have permission to use.**
2. Ask the agent to generate a 4-view sheet (front, both sides, back) — GPT Image 2.5, 2k, ~23 credits (or Qwen Image 2.1 locally) — so the face stays the same from every angle.
3. Compare models with the same image and line (Grok Video 1.5 vs Wan 3.0, 8 s each) and pick one.
4. Upload the reference to Renoise and put its `material:<id>` into `skills/digital-human-koubo/persona.json` (`renoise.reference_material`, or `other_hosts.me` for a second presenter).

Details: [`references/new-avatar.md`](skills/digital-human-koubo/references/new-avatar.md). The `material:` IDs in this repo belong to the original author's account and won't work on yours — that's expected. For the local route, just add a host to `persona.json → comfy.hosts` (see [Presenters](#presenters-for-the-local-route)).

<p align="center"><img src="docs/images/scene-composite.jpg" width="720" alt="Reference photo → composited livestream studio"></p>

### Cloud cost reference (real runs)

| Video | Generation | Credits |
|---|---|---|
| Livestream ad, 9:16, 27 s | 1 scene image + 5 Grok segments (720p) | **482** |
| Tutorial Ep2, 16:9, 4:36 | 32 segments (full 720p / PiP 480p) + demos | ~3,250 |
| Tutorial Ep3, 16:9, 5:54 | 30 new segments + 7 scene images, 17 segments reused | ~3,409 |

Prices at the time of writing: Grok Video 1.5 — 720p 17 credits/s, 480p 10 credits/s; GPT Image 2.5 2k — 23 credits. Always confirm with the agent's live quote.

---

## Five editing styles

<p align="center"><img src="docs/images/five-styles.jpg" width="820" alt="The five editing styles"></p>

| Style | Ratio | Length | Best for | Template |
|---|---|---|---|---|
| **A** Finance / tech explainer (Xiaolin-style structure) | 16:9 | 3–20 min | events, data, "why…" | `templates/lin-169` (plan.json-driven: text behind presenter, boards + presenter PiP, B-roll, formulas built term by term, worked examples, charts) |
| **B** Influencer talking head with animated captions | 9:16 | 30–120 s | product picks, sales, opinions | `templates/huazi-916` (data-driven) |
| **C** Launch breakdown | 16:9 | 30–90 s | new products / models | `templates/reference/launch-169` |
| **D** Step-by-step tutorial | 16:9 | 3–8 min | "how to…", tool setup | `templates/reference/tutorial-169` |
| **E** Multi-host · multi-language · multi-scene | 16:9 | 3–7 min | capability demos, going global | `templates/reference/multihost-169` |

Style B has three caption intensities — **restrained / standard / lively**:

<p align="center"><img src="docs/images/huazi-presets.jpg" width="820" alt="Caption intensity presets"></p>

Style A learns only the *structure and editing grammar* of popular explainer channels. It never uses a real creator's face, voice, set or lines.

---

## 48 packaging components

We measured 25 videos frame by frame (shot detection, opening beats, on-screen text, sound) — full reports in [`references/research/`](skills/digital-human-koubo/references/research/).

<p align="center"><img src="docs/images/creator-pacing.jpg" width="720" alt="Cuts per minute measured on 25 creator videos"></p>

**Rules distilled from the research** ([`packaging-playbook.md`](skills/digital-human-koubo/references/packaging-playbook.md)):
- Cut count can be low, but stimulation can't stop: in the first 30 s, something new every 3–5 s.
- First 3 s: the claim or the action — no greeting, no logo.
- A BGM bed under everything; sound effects only on events (1–3 per minute in Chinese talking-head channels); 0.6–1.0 s of silence right before a reveal.
- For a single-camera digital human, the cheapest pacing is **punch-in cuts** on sentence boundaries (1.0× / 1.18× / 1.32×).

<div align="center">
<a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4"><img src="docs/gifs/packaging-gallery.gif" width="560"></a><br>
<b>Packaging component gallery</b> · 48 components · 2:40 · <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4">▶ Watch</a>
</div>

<p align="center"><img src="docs/images/packaging-gallery.jpg" width="820" alt="Packaging component gallery"></p>

| Group | Components |
|---|---|
| Opening / hooks | TeaserColdOpen · ColdOpenFreeze · SearchTyping · NumberSpike · SlamText · WordStack · TornStrip · **TextBehind** |
| Evidence / data | EvidenceCard · DocFocus · SourceDoc · ZoomFocus · Counter · Odometer · GlassPanel · SpecCard · LineDraw · BarCompare · ReviewCards · ArchiveCards · MapRoute · CompareWipe · PaperCollage |
| Annotation / people | HandDraw · CalloutPill · LeaderLabel · TypedNameTag · LowerThird · NamePlate · SourceTag · FreezeFrame |
| Rhythm / interaction | PunchInHost · KeywordStack · RetentionCaption · TiltLine · Aside · Danmaku · ReactionPop · MemeWindow · PollPop · GlitchInterstitial · HostFloaters · ProgressChapters · ProgressTracker · ChapterCard · RecapBoard · Countdown · GhostWord |

Every component is called by name in a `pack` list, with timings written as `"segment:word"` (e.g. `"3:积分"`), and adapts to 9:16 automatically:

```json
"pack": [
  { "use": "NumberSpike", "at": "1:不到十块钱", "until": "1:end", "text": "¥9.9/节", "label": "一节课" },
  { "use": "Danmaku", "items": [{ "t": "真的假的？", "at": "1:" }, { "t": "AI 还能帮我干活？", "at": "1:教你", "hot": true }] },
  { "use": "TextBehind", "src": "main.mp4", "cutout": "main_cut_s4.webm", "cutoutFrom": 17.2, "at": "4:", "until": "4:end",
    "mode": "count", "lines": [{ "t": "¥99", "font": "en", "color": "#FFE14D", "size": 0.17 }], "count": { "from": 999, "to": 99, "prefix": "¥" } }
]
```
Reference: [`references/packaging.md`](skills/digital-human-koubo/references/packaging.md). Validate before rendering: `python3 scripts/check_edit.py <project>/src`.

### Text behind the presenter

<p align="center"><img src="docs/images/text-behind-layers.jpg" width="760" alt="Original → person matte → original + big text + cut-out presenter"></p>

```bash
python3 scripts/cutout_video.py public/main.mp4 public/main_cut_s4.webm --from 17.2 --to 22.4   # matte only the seconds you need
```
On Linux / Windows the matte comes from BiRefNet in ComfyUI; on macOS from Apple Vision. It works on **medium shots with headroom**. In a selfie close-up the person fills ~89 % of the frame and hides the text — the script warns above 60 %. Mark such segments `"shot": "depth"` and they are generated as medium shots.

<p align="center"><img src="docs/images/closeup-vs-medium.jpg" width="560" alt="Close-up (89%) hides the text, medium shot (57%) shows it"></p>

---

## Repository structure

```
skills/
  digital-human-koubo/            main skill
    SKILL.md                      workflow the agent follows
    persona.json                  presenters, voice descriptions, prompt templates
                                  (comfy: local route config, hosts with voice_ref / look / look_person, H3 prompt template)
    comfy/                        ComfyUI API graphs: tts_clone · h3_r2v_audio · h3_i2v · qwen_t2i · music
    references/                   style menu · packaging · playbook · install · research reports
    scripts/                      comfy_batch (local TTS + H3 lip sync) · comfy_scene · comfy_broll · comfy_music
                                  face_center (mediapipe) · numcn (digits → Chinese reading for back-check)
                                  build_tasks · rangedl · assemble · align · check_edit · cutout_video
                                  voicefx/unify · doctor · new_edit · make_assets
                                  make_cover · cover_first (cover + first frame)
                                  lin_scenes · lin_subs · lin_sfx · lin_mix (Style A scenes, subtitles, SFX, mix)
                                  misread_check · patch_words (find mispronunciations, patch one clause, keep lip sync)
    templates/
      huazi-916/                  9:16 data-driven talking-head template (edit.json)
      packaging/                  48-component kit + gallery project
      lin-169/                    16:9 Xiaolin-style explainer template (scenes.json-driven, 13 scene types)
      reference/                  launch-169 · tutorial-169 · multihost-169
    assets/                       style previews · packaging gallery · avatar reference
                                  host_girl_*.png · voice_ref_*.flac (local-route presenters)
  finance-explainer/              chart-only finance long-form engine (episode.json beat sheet, research helpers)
workflows/                        ComfyUI workflows (UI format) behind the local route, with a map to the API files
docs/                             install guide (INSTALL.md), README images, GIF previews, posters
```

## Known pitfalls (all handled by the skill)

### Local route

- Without the Lightning LoRA, H3 at 0.8 MP needs more than 24 GB and hangs at step 0 → the workflows use the 4-step (presenter) and 8-step (B-roll) LoRAs.
- Qwen3-TTS occasionally garbles a word (e.g. "MiniMax" → "mini maxax") → every line is checked with SenseVoice *without* the script; add `"seed": <n>` to that segment and re-run, only it is redone.
- Lines longer than 14 s fail on purpose → split them; H3 quality drops on long single shots.
- With a scene image as reference, the studio described in `look` pulls the background back (a warm livestream room came out as a dark-blue wall) → `look_person` describes only the person and is used automatically when a segment has `"ref"`.
- MiniMax Music 3 tends to end early (28 s for a 60 s request) → more `[Instrumental]` tags in the lyrics make it longer (5 tags ≈ 37 s); the editors loop it anyway.
- H3 draws gibberish characters on shop signs → write "shop signs are blurred and out of focus", or pick shots without signs.
- Variables in `~/.bashrc` below the "not interactive → return" line are invisible to scripts → earshot tries to reach Hugging Face and hangs; put the `EARSHOT_*` exports above it.
- whisper / SenseVoice write spoken numbers as digits ("七十二" → "72") → `numcn.py` converts both sides to the spoken form before comparing. Digit-by-digit readings ("三零九零" for 3090) and homophones can still be flagged → listen before re-voicing.

### Both routes / cloud route

- Concatenating dozens of clips makes the voice drift behind the lips (measured: 0.38 s late by 4:43 over 44 clips) → `assemble.py` pads every clip's audio to its video length and checks audio/video durations match.
- whisper with the script as prompt "corrects" mispronounced words → `misread_check.py` transcribes pause-split clauses without the script; `patch_words.py` replaces just that clause with a voice-clone take stretched to the original length, so lip sync stays intact (don't re-voice the whole film).
- Always mute the presenter video track when a separate voice track is used; doubled audio a few ms apart sounds harsh (comb filtering).
- Expo easing never quite reaches the target (99.9 → rounds to 100) → counters snap to the exact value at the end.
- Grok occasionally **burns subtitles** into landscape clips even when told not to → frame check + re-shoot that segment.
- whisper writes Chinese numbers as digits (九百九十九 → 999), so accuracy drops but the line is correct → listen before re-shooting.
- Renoise's US CDN can truncate parallel downloads → `rangedl.py` downloads in 6 ranges with resume + decode check.
- Grok 9:16 720p is **720×1280** — never stretch it to another ratio.

## Responsible use

- Use only your own face/voice or ones you have **explicit permission** to use. Never impersonate a real person or creator.
- Every video carries an "AI digital human" label; scene and animal clips are marked "AI generated".
- No made-up numbers, prices, offers or reviews — sample data on screen must be labelled as such.
- Don't use web memes, film/TV stills or celebrity images — the meme components use original stickers generated from your own presenter.
- Credits (cloud route) are spent only after you approve the quote.

## License & third-party

- Code and docs: [MIT](LICENSE) © 2026 Berryxia (andyhuo520); local ComfyUI route © 2026 walksky.
- Local route: [ComfyUI](https://github.com/comfyanonymous/ComfyUI) (GPL-3.0, installed by you) · models MiniMax H3, MiniMax Music 3, Qwen Image 2.1, Qwen3-TTS, SenseVoice, BiRefNet (downloaded by you; each has its own license — check the model page before commercial use) · [mediapipe](https://github.com/google-ai-edge/mediapipe) (Apache-2.0) · [earshot](https://github.com/Leonxlnx/earshot) (MIT) with CLAP and AST models.
- **[Remotion](https://www.remotion.dev/)** is used for rendering and has its own license: free for individuals and companies of up to 3 people; larger companies need a [company license](https://www.remotion.pro/).
- Animated emoji: [Google Noto Emoji Animation](https://googlefonts.github.io/noto-emoji-animation/) (CC BY 4.0) — credit "Animated emoji: Google Noto" in your videos.
- Maps: [world-atlas](https://github.com/topojson/world-atlas) (ISC; data from Natural Earth, public domain) · [d3-geo](https://github.com/d3/d3-geo), [topojson-client](https://github.com/topojson/topojson-client) (ISC). For maps involving China's borders in formally published content, check against applicable local standards.
- Speech recognition: [whisper.cpp](https://github.com/ggerganov/whisper.cpp) (MIT). Cloud generation runs on [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) (your account, your credits); optional TTS by [Xiaomi MiMo](https://platform.xiaomimimo.com/).
- Course screenshots in the WorkBuddy demo come from the original author's own course. Demo videos are the authors' own work; please don't re-upload them as your own.

See [THIRD_PARTY.md](THIRD_PARTY.md) for details.

---

<div align="center">

Original by **Berryxia** ([andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo)) · local ComfyUI route by **walksky** · built with Claude Code · if this helped, a ⭐ helps others find it.

</div>
