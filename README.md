<div align="center">

# Digital Human Koubo · AI 数字人口播

**One photo + one sentence → a finished talking-head video with a digital human.**
Script, lip-synced AI presenter, voice clean-up, captions, and pro-YouTuber-style packaging — fully automated by your AI agent.

**English** · [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](LICENSE)
![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-orange)
[![Renoise MCP](https://img.shields.io/badge/video-Renoise%20MCP-ff7a1a)](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)
![Remotion](https://img.shields.io/badge/edit-Remotion%204-0b84f3)
![Local ComfyUI](https://img.shields.io/badge/local-ComfyUI-3b5bdb)

<img src="docs/images/cover.jpg" width="820" alt="One photo + one sentence → a 27-second livestream sales ad">

</div>

> This 27-second livestream ad has no real presenter. Face, voice, studio, captions and the price animation are all AI.
> The only input was one sentence: *"Use this digital human to make a 30-second livestream ad for the WorkBuddy course — 10 lessons, ¥99, was ¥999."*
> Total cost: **482 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) credits**.

> **New in this fork — a fully local route.** Everything that used to be generated in the cloud — voice, lip-synced presenter, scene images, B-roll, background music, person cutout — can now run on your own GPU through **[ComfyUI](https://github.com/comfyanonymous/ComfyUI)**, with no credits and no API keys: **Qwen3-TTS** voice cloning → **MiniMax H3** audio-driven lip sync → **Qwen Image 2.1** scenes → **MiniMax Music 3** BGM → **earshot** sound design. All five editing styles have been produced end-to-end on one RTX 3090. See [Architecture](#architecture) and [Local ComfyUI setup](#3b--or-run-generation-locally-with-comfyui-no-credits).

---

## Demos

Click a GIF (or "Watch") to play the full video. Every demo below was produced with this repo.

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

<div align="center">
<a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4"><img src="docs/gifs/packaging-gallery.gif" width="560"></a><br>
<b>Packaging component gallery</b> · 48 components · 2:40 · <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4">▶ Watch</a>
</div>

> All presenters in the demos are AI digital humans and every video is labelled "内容由 AI 数字人演绎" (performed by an AI digital human). The male presenter is the author's own digital twin, made from his own photo.

---

## What it does

- **Two generation engines, one pipeline** — generate in the cloud with **Renoise MCP** (Grok Video 1.5, GPT Image 2.5, Wan 3.0) or locally with **ComfyUI** (Qwen3-TTS, MiniMax H3, Qwen Image 2.1, MiniMax Music 3, BiRefNet). Scripting, QA, editing, packaging and covers are the same for both; just say *"use local ComfyUI"*.
- **Digital human from one photo** — a fixed presenter (face, outfit, voice description, prompt template) stored in `persona.json`, so every video is the same person. Composite her into any scene (livestream studio, shop, classroom, Kyoto street) with GPT Image first, then make her talk.
- **Lip-synced talking clips** — the script is split into ≤ 15-second segments and generated with **Grok Video 1.5** through **[Renoise MCP](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)**. Other models (Wan 3.0, OmniHuman for your own recording) are documented.
- **Cost gate** — the agent always quotes *segments · seconds · credits · balance* first and waits for your "yes". It generates segment 1 for you to check before batching the rest.
- **Quality control** — every segment is transcribed with whisper and compared with the script, and 4 frames per segment are inspected (Grok sometimes burns subtitles into the picture; those segments get re-shot).
- **Voice unification** — 1/3-octave spectral matching, de-essing, one shared small-room reverb and loudness normalisation, so 30 separately-generated clips sound like one recording (sibilance spread 13.2 dB → 5.9 dB in our tests).
- **5 editing styles, chosen for your content** — the agent diagnoses your content, recommends 2 styles with preview images and asks you everything in one go (style · ratio & length · caption intensity · presenter).
- **48 packaging components** — measured frame-by-frame from 25 videos by top creators (MrBeast, Mark Rober, Ryan Trahan, MKBHD, MediaStorm/影视飓风, 何同学, Johnny Harris, Vox, Kurzgesagt, 回形针, 半佛仙人, 差评, 毕导). Each style has a default packaging recipe; add or remove techniques by just asking.
- **Text behind the presenter** — big words / numbers between the background and the person (macOS Vision person segmentation → transparent video → 3-layer composite).
- **Cover as the first frame** — every video gets a cover by default (16:9 / 9:16 / 3:4: presenter frame + hook headline + evidence cards), spliced in as the first 0.5 s. Platforms use the first frame as the thumbnail, so there is nothing to upload separately.
- **Multi-language** — English, Japanese, Korean, French, Spanish, Arabic tested (whisper back-check 94–100 %).
- **Works with your agent** — a standard `SKILL.md` Agent Skill plus scripts; any agent that can load skills, connect a remote MCP server and run local commands can drive it.

## How it works

```
your content ──► 0. setup check (Renoise MCP / ffmpeg / whisper — skip what you already have)
                 1. diagnose content → recommend 2 of 5 styles → ask once → brief.json
                 2. script.json (≤15 s per segment, ~5.4 Chinese chars/s)
                 3. quote credits → wait for "yes" → generate segment 1 → you check → batch
                 4. range-download (CDN-safe) → whisper back-check → frame check
                 5. voice unification (spectral match + de-ess + shared room)
                 6. word-level timeline (tl.json)
                 7. edit in Remotion: style template + default packaging (+ your requests)
                 8. render → check mid-transition frames → loudness (-14 / -16 LUFS)
                 9. cover: pick a presenter frame → 16:9 / 9:16 / 3:4 → splice in as the first frame (0.5 s)
```

<p align="center"><img src="docs/images/ad-breakdown.jpg" width="820" alt="The 5 segments of the livestream ad and the packaging used in each"></p>

---

## Architecture

The skill is four layers. The agent reads `SKILL.md` and drives everything else through scripts; only the **generation layer** changes between the cloud and the local route.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Agent + SKILL.md     diagnose → brief.json → script.json → ask / quote   │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 2a. Cloud generation (Renoise MCP)   │ 2b. Local generation (ComfyUI API)   │
│   Grok Video 1.5  presenter + voice  │   Qwen3-TTS        voice clone       │
│   GPT Image 2.5   scenes / 4-view    │   MiniMax H3 R2V   lip sync to voice │
│   Wan 3.0         B-roll             │   Qwen Image 2.1   scenes / 4-view   │
│   MiMo TTS        optional voice     │   MiniMax H3 T2V/I2V  B-roll         │
│   make_assets.py  placeholder BGM    │   MiniMax Music 3  BGM               │
│   Apple Vision    person cutout      │   BiRefNet         person cutout     │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ 3. QA + timeline     whisper / SenseVoice back-check · frame check ·        │
│                      assemble.py (drift-safe concat) · align.py → tl.json   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Edit + finish     Remotion templates (huazi-916 · lin-169 · reference/*) │
│                      48 packaging components · earshot SFX · BGM ducking    │
│                      loudness -14/-16 LUFS · make_cover → cover_first       │
└─────────────────────────────────────────────────────────────────────────────┘
```

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
side jobs:   comfy_scene.py  (Qwen Image 2.1 edit: host into a livestream room / shop / street, 4-view, stickers)
             comfy_broll.py  (H3 text- or image-to-video B-roll, 16:9)
             comfy_music.py  (MiniMax Music 3 instrumental BGM → check with `earshot describe`)
             cutout_video.py (BiRefNet mask for text-behind-presenter on Linux / Windows)
             face_center.py  (mediapipe face position for framing in Style A)
```

### Components by step

| Step | Cloud route | Local route | Script |
|---|---|---|---|
| Voice | Grok native voice · optional Xiaomi MiMo TTS | **Qwen3-TTS 1.7B Base** voice clone | `comfy_batch.py --stage tts` |
| Voice QA | whisper.cpp | **SenseVoice Small** (inside ComfyUI) + whisper.cpp | `comfy_batch.py`, `misread_check.py` |
| Presenter video | Grok Video 1.5 (Renoise) | **MiniMax H3 Ref2VA** + 4-step Lightning LoRA | `build_tasks.py` / `comfy_batch.py --stage video` |
| Scene image, 4-view, stickers | GPT Image 2.5 (Renoise) | **Qwen Image 2.1** image edit | `comfy_scene.py` |
| B-roll | Wan 3.0 (Renoise) | **MiniMax H3** T2VA / I2VA + 8-step Lightning LoRA | `comfy_broll.py` |
| Background music | placeholder from `make_assets.py` | **MiniMax Music 3** | `comfy_music.py` |
| Sound effects | `make_assets.py` (synthesised) / **earshot** kit | **earshot** kit | `lin_sfx.py` |
| Person cutout | Apple Vision (macOS) | **BiRefNet** (ComfyUI) | `cutout_video.py` |
| Face position | Apple Vision (macOS) | **mediapipe** BlazeFace | `face_center.py` |
| Concat, timeline, edit, cover | ffmpeg · whisper.cpp · Remotion 4 · Playwright | same | `assemble.py` · `align.py` · templates · `make_cover.py` |

### ComfyUI workflows (`skills/digital-human-koubo/comfy/`)

Flattened API-format graphs. The scripts load them, fill in text / images / audio / seed and submit them to ComfyUI's REST API (`/upload`, `/prompt`, `/history`, `/view`). The address is `comfy.url` in `persona.json` (default `http://127.0.0.1:8188`).

| File | Used by | Main nodes | Model files |
|---|---|---|---|
| `tts_clone.api.json` | `comfy_batch.py` | `Qwen3TTSLoader` · `Qwen3TTSVoiceClonePrompt` · `Qwen3TTSVoiceClone` | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` (downloaded by the node pack) |
| `h3_r2v_audio.api.json` | `comfy_batch.py` | `MiniMaxH3ReferenceToVideo` · `SamplerCustomAdvanced` · `CreateVideo` | `minimax_h3_ref2va_pruned_int8_convrot` · LoRA `minimax_h3_ref2v_turbo_4step_v0.1` · text encoder `qwen3vl_32b_minimax_h3_nvfp4_awq` · VAEs `minimax_h3_video_vae_int8_convrot`, `minimax_h3_audio_vae_fp32` |
| `h3_i2v.api.json` | `comfy_broll.py` | `MiniMaxH3ImageToVideo` | `minimax_h3_fl2va_pruned_int8_convrot` · LoRA `minimax_h3_fl2v_turbo_8step_v1.0` · same text encoder and VAEs |
| `qwen_edit.api.json` | `comfy_scene.py` | `TextEncodeQwenImage21` · `QwenImage21Cache` | `qwen_image_2.1_int8_convrot` · `qwen3vl_8b_int8_convrot` · `qwen_image_2.1_vae_bf16` |
| `music.api.json` | `comfy_music.py` | `MiniMaxMusic3TextEncode` · `EmptyMiniMaxMusic3LatentAudio` · `KSampler` | `minimax_music3_dit_fp16` · `minimax_music3_text_encoder_pruned_int8_convrot` · `minimax_music3_dav` |
| *(built in script)* | `cutout_video.py` | `LoadBackgroundRemovalModel` · `RemoveBackground` | `birefnet.safetensors` |
| *(built in script)* | `comfy_batch.py` | `Qwen3TTSSenseVoiceASR` | `iic/SenseVoiceSmall` (downloaded by the node pack) |

### Presenters for the local route

`persona.json → comfy.hosts` defines each local presenter: photo (`avatar`), output size, voice sample (`voice_ref` + `voice_ref_text`), English appearance text for the prompt (`look`, plus `look_person` without the studio for use with scene images), voice description and default framing. Two are included: `tank` (the default white-tank-top host, `assets/avatar_ref.jpg`) and `girl` (`assets/host_girl_*.png`). The H3 prompt template is `comfy.prompt_template` (Ref2VA format: subject_definitions / summary / retention_analysis / detailed_description / soundscape / music).

---

## Supported agents

The skill is a folder with a `SKILL.md` (the open Agent Skills format) plus Python / shell / Remotion scripts. To run the **whole** pipeline an agent needs three things:

1. **Load Agent Skills** (a skills folder or skill upload),
2. **Connect a remote MCP server** (Renoise — streamable HTTP, browser login, no API key),
3. **Run commands on your computer** (ffmpeg, Python, Node — for downloading, QA and editing).

| Agent | Skills | Renoise MCP | Local commands | Status |
|---|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `/plugin` (below) | ✅ | ✅ Tested — this repo was built with it |
| **Codex** (CLI / desktop) | `~/.codex/skills/` | `codex mcp add` | ✅ | ✅ Expected to work (same scripts) |
| **OpenClaw** | skills folder per OpenClaw docs | `openclaw plugins install` | ✅ | ⚙️ Should work |
| **WorkBuddy** | Skills → import the folder / zip | Connectors → add custom MCP | ✅ desktop agent | ⚙️ Should work — menu names may differ by version |
| **豆包 (Doubao)** · **千问办公 (Qwen Office)** · **纳米Work (NamiWork)** and other agent products | import if the product supports Agent Skills | add as a custom / remote MCP server if supported | needed for editing | ⚙️ Works if the product supports the 3 requirements above; check its docs |
| **Claude desktop / claude.ai** | upload the skill zip in Settings | Connectors → Add custom connector | ⚠️ sandbox only | Script writing, scene design, generation & quoting work; local editing needs a shell agent |

> The **local ComfyUI route** needs no MCP server: the scripts call ComfyUI's HTTP API directly, so any agent that can run local commands can drive it.

> If your agent can only do MCP + chat (no local commands), you can still use it to **plan, quote and generate** the clips through Renoise; then run the editing steps with Claude Code / Codex, or by hand with the commands in [`SKILL.md`](skills/digital-human-koubo/SKILL.md).

---

## Installation

### 1 · Get the code

```bash
git clone https://github.com/walkskysu/digital-human-koubo-comfyui.git
cd digital-human-koubo-comfyui
```

This is a fork of [andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo) with the local ComfyUI route added.

### 2 · Install the two skills into your agent

The repo contains two skills: `digital-human-koubo` (main) and `finance-explainer` (an optional engine for chart-only finance long-forms; Style A now uses `templates/lin-169` in the main skill).

**Claude Code**
```bash
mkdir -p ~/.claude/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.claude/skills/
```
**Codex**
```bash
mkdir -p ~/.codex/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.codex/skills/
```
**WorkBuddy / OpenClaw / other agents** — zip the two folders and import them in the product's *Skills* page, or copy them into its skills directory (see the product's docs):
```bash
cd skills && zip -r ../digital-human-skills.zip digital-human-koubo finance-explainer && cd ..
```

### 3 · Connect Renoise MCP (AI video / image generation)

Create an account at **[renoise.ai](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)** first. Login is in the browser — you never paste an API key.

| Agent | How |
|---|---|
| Claude Code | `/plugin marketplace add ArcoCodes/renoise-plugins-official` then `/plugin install renoise@renoise-plugins-official` |
| Codex | `codex mcp add renoise --url https://renoise.ai/api/public/mcp` then `codex mcp login renoise` |
| OpenClaw | `openclaw plugins install renoise --marketplace ArcoCodes/renoise-plugins-official` |
| Claude desktop / claude.ai | Settings → Connectors → **Add custom connector** → name `Renoise`, URL `https://renoise.ai/api/public/mcp` |
| WorkBuddy, Cursor, Windsurf, Cline, 豆包, 千问, 纳米Work, … | add a remote MCP server with URL `https://renoise.ai/api/public/mcp` (typical config: `{"mcpServers":{"renoise":{"url":"https://renoise.ai/api/public/mcp"}}}`) |

Latest official instructions: **[renoise.ai/plugin](https://renoise.ai/plugin)**. Check it worked by asking your agent: *"查一下我的 Renoise 余额 / check my Renoise balance."*

### 3b · Or: run generation locally with ComfyUI (no credits)

Skip step 3 if you only want the local route (you can also set up both and choose per video).

**Hardware.** Tested on an RTX 3090 (24 GB VRAM) with 34 GB RAM: ComfyUI Desktop on Windows, the skill in WSL2 Ubuntu reaching it at `127.0.0.1:8188`. A native Linux ComfyUI works the same way. The Lightning LoRAs are **required** on 24 GB; without them H3 runs out of memory and hangs at step 0.

**ComfyUI.** Version **0.44 or newer**. MiniMax H3, MiniMax Music 3, Qwen Image 2.1 and BiRefNet background removal are built-in nodes. One custom node pack is needed:

- **Qwen3-TTS** node pack (`Qwen3TTSLoader`, `Qwen3TTSVoiceClone`, `Qwen3TTSSenseVoiceASR`, …): install it from ComfyUI Manager. It downloads `Qwen/Qwen3-TTS-12Hz-1.7B-Base` and `iic/SenseVoiceSmall` on first use.

**Model files** (put each in the ComfyUI `models/` sub-folder shown):

| Folder | Files | For |
|---|---|---|
| `diffusion_models/` | `minimax_h3_ref2va_pruned_int8_convrot.safetensors` | presenter lip sync |
| | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` | B-roll |
| | `qwen_image_2.1_int8_convrot.safetensors` | scene images |
| | `minimax_music3_dit_fp16.safetensors` | BGM |
| `loras/` | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` | 4-step presenter |
| | `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` | 8-step B-roll |
| `text_encoders/` | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | H3 |
| | `qwen3vl_8b_int8_convrot.safetensors` | Qwen Image 2.1 |
| | `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` | Music 3 |
| `vae/` | `minimax_h3_video_vae_int8_convrot.safetensors`, `minimax_h3_audio_vae_fp32.safetensors` | H3 |
| | `qwen_image_2.1_vae_bf16.safetensors` | Qwen Image 2.1 |
| | `minimax_music3_dav.safetensors` | Music 3 |
| `background_removal/` | `birefnet.safetensors` | text-behind-presenter cutout |

The easiest way to get them is to open the matching ComfyUI templates (*MiniMax H3 Reference to Video*, *MiniMax H3 Image to Video*, *Qwen Image 2.1 Edit*, *MiniMax Music 3*), which offer to download missing models. If a file name differs in your install, change it in the JSON under `skills/digital-human-koubo/comfy/`.

**Python side** (where the skill runs):
```bash
python3 -m venv ~/.venvs/koubo && source ~/.venvs/koubo/bin/activate
pip install av numpy pillow playwright mediapipe && python -m playwright install chromium
curl -L -o ~/models/blaze_face_short_range.tflite \
  https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite
curl -s http://127.0.0.1:8188/system_stats   # ComfyUI reachable?
```

**Your presenter's voice.** Record 12–20 s of clean, dry speech of **your own** voice (or one you're licensed to use), save it under `assets/`, and set `voice_ref` and `voice_ref_text` (the exact words) for the host in `persona.json → comfy.hosts`.

**earshot** (sound effects and BGM check) — [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot), MIT:
```bash
git clone https://github.com/Leonxlnx/earshot ~/tools/earshot && cd ~/tools/earshot
python3 -m venv .venv && .venv/bin/pip install -e . && sudo ln -s ~/tools/earshot/.venv/bin/earshot /usr/local/bin/earshot
earshot doctor --fetch     # downloads CLAP (laion/larger_clap_general) + AST (MIT/ast-finetuned-audioset-10-10-0.4593), ~1.1 GB
```
`lin_sfx.py` only needs `earshot kit init/render` (no models). `earshot describe` (checking that generated BGM has no vocals and the right genre) needs the two models. To keep them in your own folder and read them offline, put these lines in `~/.bashrc` **above** the `case $- in *i*) ;; *) return;; esac` line, otherwise scripts started by the agent won't see them:
```bash
export EARSHOT_CLAP=~/models/earshot/larger_clap_general
export EARSHOT_AST=~/models/earshot/ast-audioset
export EARSHOT_HOME=~/models/earshot/cache
export EARSHOT_OFFLINE=1
```

### 4 · Local tools (for downloading, QA and editing)

| Tool | macOS | Windows | Linux |
|---|---|---|---|
| ffmpeg | `brew install ffmpeg` | `winget install Gyan.FFmpeg` | `sudo apt install ffmpeg` |
| Python 3 + numpy + Pillow | `brew install python` then `python3 -m pip install numpy pillow` | `winget install Python.Python.3.12` | `sudo apt install python3-pip` |
| Playwright + Chromium (cover layout) | `python3 -m pip install playwright && python3 -m playwright install chromium` | same | same |
| Node.js 18+ (Remotion) | `brew install node` | `winget install OpenJS.NodeJS.LTS` | `nvm install --lts` |
| whisper.cpp (`whisper-cli`) | `brew install whisper-cpp` | [Releases](https://github.com/ggerganov/whisper.cpp/releases) | build from [source](https://github.com/ggerganov/whisper.cpp) |
| whisper model | [`ggml-medium-q5_0.bin`](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium-q5_0.bin) → `~/models/` (or `export WHISPER_MODEL=/path/to/model.bin`) | same | same |

One-command check — it skips what you have and lists install options for what's missing:
```bash
bash ~/.claude/skills/digital-human-koubo/scripts/doctor.sh
```

The **text-behind-presenter** effect uses Apple Vision on **macOS**; on Linux / Windows `cutout_video.py` uses BiRefNet in ComfyUI instead. Everything else is cross-platform.

### 5 · Sound effects & placeholder music

The repo ships **no third-party audio**. Generate an original set of 30 sound effects and a placeholder background track (pure code, no copyright):
```bash
python3 ~/.claude/skills/digital-human-koubo/scripts/make_assets.py
```
`new_edit.sh` also runs this automatically for every new project. For a better soundtrack, drop any track you have the rights to at `<project>/public/music/bgm.mp3`.

### 6 · (Optional) Xiaomi MiMo TTS — designed or cloned voices

The default voice is Grok's native voice (best lip-sync). For a designed voice, your own cloned voice, or narration-only videos, the skill uses **Xiaomi MiMo TTS**:

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

> Note: Grok generates lip movement from its own voice. Swapping in a different voice afterwards leaves ~100 ms lip offset (fine in picture-in-picture, visible in full-screen close-ups). For your own recording with exact lip-sync, use an audio-driven model such as OmniHuman (documented in the skill).

---

## Quick start

Talk to your agent in plain language:

```text
用我的数字人 Skill 讲这段：……（paste your content）
Use my digital human skill to make a 30-second livestream ad: WorkBuddy course, 10 lessons, ¥99 (was ¥999).
Make a 3-minute explainer about why Silicon Valley Bank collapsed, Xiaolin-style.
用本地 ComfyUI 做，不花积分：两个主播接力讲双 11 的三个坑，16:9，40 秒。 (local route, two hosts)
Generate the BGM with MiniMax Music and redo the sound effects with earshot.
Add a map route when she mentions these countries. / Put "¥99" behind her. / Add a teaser cold open.
把包装组件图鉴发我看看  (show me the packaging gallery)
```

What happens next:
1. Setup check — anything already installed is skipped.
2. A one-line diagnosis + 2 recommended styles with preview images, and one round of questions.
3. Script + scene design + **credit quote** → you approve → segment 1 → you approve → the rest.
4. QA, voice clean-up, editing with the style's default packaging → the finished MP4.

---

## Make your own digital human

1. Pick a photo: frontal face, even light, hair off the face, mouth closed. **Only your own photo or one you have permission to use.**
2. Ask the agent to generate a 4-view sheet (front, both sides, back) — GPT Image 2.5, 2k, ~23 credits — so the face stays the same from every angle.
3. Compare models with the same image and line (Grok Video 1.5 vs Wan 3.0, 8 s each) and pick one.
4. Upload the reference to Renoise and put its `material:<id>` into `skills/digital-human-koubo/persona.json` (`renoise.reference_material`, or `other_hosts.me` for a second presenter).

Details: [`references/new-avatar.md`](skills/digital-human-koubo/references/new-avatar.md). The `material:` IDs in this repo belong to the author's account and won't work on yours — that's expected.

<p align="center"><img src="docs/images/scene-composite.jpg" width="720" alt="Reference photo → composited livestream studio"></p>

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

<p align="center"><img src="docs/images/text-behind-layers.jpg" width="760" alt="Original → Vision matte → original + big text + cut-out presenter"></p>

```bash
python3 scripts/cutout_video.py public/main.mp4 public/main_cut_s4.webm --from 17.2 --to 22.4   # matte only the seconds you need
```
It works on **medium shots with headroom**. In a selfie close-up the person fills ~89 % of the frame and hides the text — the script warns above 60 %. Mark such segments `"shot": "depth"` and they are generated as medium shots.

<p align="center"><img src="docs/images/closeup-vs-medium.jpg" width="560" alt="Close-up (89%) hides the text, medium shot (57%) shows it"></p>

---

## Cost reference (real runs)

| Video | Generation | Credits |
|---|---|---|
| Livestream ad, 9:16, 27 s | 1 scene image + 5 Grok segments (720p) | **482** |
| Tutorial Ep2, 16:9, 4:36 | 32 segments (full 720p / PiP 480p) + demos | ~3,250 |
| Tutorial Ep3, 16:9, 5:54 | 30 new segments + 7 scene images, 17 segments reused | ~3,409 |

### Local ComfyUI route (RTX 3090 24 GB, real runs)

No credits; the cost is GPU time.

| Job | Setting | Time |
|---|---|---|
| Voice clone (Qwen3-TTS) | one 5–14 s line | seconds |
| Presenter segment (H3 Ref2VA) | 10 s, 672×1216 or 1216×672, 4 steps | ~8 min (4–9 min) |
| Scene image (Qwen Image 2.1 edit) | 25 steps | 2–5 min |
| B-roll (H3 T2VA / I2VA) | 5 s, 1216×672, 8 steps | 5–6 min |
| BGM (MiniMax Music 3) | 35–50 s instrumental, 30 steps | 1–2 min |

One short test video per style, all made locally: **A** finance explainer (16:9, 35 s) · **B** talking head with animated captions (9:16, 44 s, 8 segments) · **C** launch breakdown (16:9, 41 s) · **D** step-by-step tutorial (16:9, 44 s) · **E** two-host relay with an English line (16:9, 37 s). Each ~40-second video took roughly 40–70 minutes of GPU time.

Prices at the time of writing: Grok Video 1.5 — 720p 17 credits/s, 480p 10 credits/s; GPT Image 2.5 2k — 23 credits. Always confirm with the agent's live quote.

## Repository structure

```
skills/
  digital-human-koubo/            main skill
    SKILL.md                      workflow the agent follows
    persona.json                  presenters, voice descriptions, prompt templates
                                  (comfy: local route config, hosts with voice_ref / look / look_person, H3 prompt template)
    comfy/                        ComfyUI API graphs: tts_clone · h3_r2v_audio · h3_i2v · qwen_edit · music
    references/                   style menu · packaging · playbook · install · research reports
    scripts/                      build_tasks · rangedl · assemble · align · check_edit · cutout_video
                                  voicefx/unify · doctor · new_edit · make_assets
                                  make_cover · cover_first (cover + first frame)
                                  lin_scenes · lin_subs · lin_sfx · lin_mix (Style A scenes, subtitles, SFX, mix)
                                  misread_check · patch_words (find mispronunciations, patch one clause, keep lip sync)
                                  comfy_batch (local TTS + H3 lip sync) · comfy_scene · comfy_broll · comfy_music
                                  face_center (mediapipe) · numcn (digits → Chinese reading for back-check)
    templates/
      huazi-916/                  9:16 data-driven talking-head template (edit.json)
      packaging/                  48-component kit + gallery project
      lin-169/                    16:9 Xiaolin-style explainer template (scenes.json-driven, 13 scene types)
      reference/                  launch-169 · tutorial-169 · multihost-169
    assets/                       style previews · packaging gallery · avatar reference
                                  host_girl_*.png · voice_ref_*.flac (local-route presenters)
  finance-explainer/              chart-only finance long-form engine (episode.json beat sheet, research helpers)
docs/                             README images, GIF previews, posters
```

## Known pitfalls (all handled by the skill)

- Grok occasionally **burns subtitles** into landscape clips even when told not to → frame check + re-shoot that segment.
- whisper writes Chinese numbers as digits (九百九十九 → 999), so accuracy drops but the line is correct → listen before re-shooting.
- Renoise's US CDN can truncate parallel downloads → `rangedl.py` downloads in 6 ranges with resume + decode check.
- Grok 9:16 720p is **720×1280** — never stretch it to another ratio.
- Expo easing never quite reaches the target (99.9 → rounds to 100) → counters snap to the exact value at the end.
- Always mute the presenter video track; doubled audio a few ms apart sounds harsh (comb filtering).
- Concatenating dozens of clips makes the voice drift behind the lips (measured: 0.38 s late by 4:43 over 44 clips) → `assemble.py` pads every clip's audio to its video length and checks audio/video durations match.
- whisper with the script as prompt "corrects" mispronounced words → `misread_check.py` transcribes pause-split clauses without the script; `patch_words.py` replaces just that clause with a voice-clone take stretched to the original length, so lip sync stays intact (don't re-voice the whole film).

### Local route

- Without the Lightning LoRA, H3 at 0.8 MP needs more than 24 GB and hangs at step 0 → the workflows use the 4-step (presenter) and 8-step (B-roll) LoRAs.
- Qwen3-TTS occasionally garbles a word (e.g. "MiniMax" → "mini maxax") → every line is checked with SenseVoice *without* the script; add `"seed": <n>` to that segment and re-run, only it is redone.
- Lines longer than 14 s fail on purpose → split them; H3 quality drops on long single shots.
- With a scene image as reference, the studio described in `look` pulls the background back (a warm livestream room came out as a dark-blue wall) → `look_person` describes only the person and is used automatically when a segment has `"ref"`.
- MiniMax Music 3 tends to end early (28 s for a 60 s request) → more `[Instrumental]` tags in the lyrics make it longer (5 tags ≈ 37 s); the editors loop it anyway.
- H3 draws gibberish characters on shop signs → write "shop signs are blurred and out of focus", or pick shots without signs.
- Variables in `~/.bashrc` below the "not interactive → return" line are invisible to scripts → earshot tries to reach Hugging Face and hangs; put the `EARSHOT_*` exports above it.
- whisper / SenseVoice write spoken numbers as digits ("七十二" → "72") → `numcn.py` converts both sides to the spoken form before comparing. Digit-by-digit readings ("三零九零" for 3090) and homophones can still be flagged → listen before re-voicing.

## Responsible use

- Use only your own face/voice or ones you have **explicit permission** to use. Never impersonate a real person or creator.
- Every video carries an "AI digital human" label; scene and animal clips are marked "AI generated".
- No made-up numbers, prices, offers or reviews — sample data on screen must be labelled as such.
- Don't use web memes, film/TV stills or celebrity images — the meme components use original stickers generated from your own presenter.
- Credits are spent only after you approve the quote.

## License & third-party

- Code and docs: [MIT](LICENSE) © 2026 Berryxia (andyhuo520); local ComfyUI route © 2026 walksky.
- **[Remotion](https://www.remotion.dev/)** is used for rendering and has its own license: free for individuals and companies of up to 3 people; larger companies need a [company license](https://www.remotion.pro/).
- Animated emoji: [Google Noto Emoji Animation](https://googlefonts.github.io/noto-emoji-animation/) (CC BY 4.0) — credit "Animated emoji: Google Noto" in your videos.
- Maps: [world-atlas](https://github.com/topojson/world-atlas) (ISC; data from Natural Earth, public domain) · [d3-geo](https://github.com/d3/d3-geo), [topojson-client](https://github.com/topojson/topojson-client) (ISC). For maps involving China's borders in formally published content, check against applicable local standards.
- Speech recognition: [whisper.cpp](https://github.com/ggerganov/whisper.cpp) (MIT). Generation runs on [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) (your account, your credits); optional TTS by [Xiaomi MiMo](https://platform.xiaomimimo.com/).
- Local route: [ComfyUI](https://github.com/comfyanonymous/ComfyUI) (GPL-3.0, installed by you) · models MiniMax H3, MiniMax Music 3, Qwen Image 2.1, Qwen3-TTS, SenseVoice, BiRefNet (downloaded by you; each has its own license — check the model page before commercial use) · [mediapipe](https://github.com/google-ai-edge/mediapipe) (Apache-2.0) · [earshot](https://github.com/Leonxlnx/earshot) (MIT) with CLAP and AST models.
- Course screenshots in the WorkBuddy demo come from the author's own course. Demo videos are the author's own work; please don't re-upload them as your own.

See [THIRD_PARTY.md](THIRD_PARTY.md) for details.

---

<div align="center">

Original by **Berryxia** ([andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo)) · local ComfyUI route by **walksky** · built with Claude Code · if this helped, a ⭐ helps others find it.

</div>
