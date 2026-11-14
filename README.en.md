<div align="center">

# Digital Human Koubo · Local ComfyUI Talking-Head Videos

**One photo + one sentence → a lip-synced digital-human talking-head video, generated entirely on your own GPU.**
Voice cloning, lip sync, scene images, B-roll, music, captions and the edit are all done by your AI agent through local ComfyUI.

[简体中文](README.md) · **English**

[![Local ComfyUI](https://img.shields.io/badge/generation-local%20ComfyUI-3b5bdb)](https://github.com/comfyanonymous/ComfyUI)
![Tested on RTX 3090](https://img.shields.io/badge/tested-RTX%203090%2024GB-76b900)
[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](LICENSE)

<img src="docs/images/local-cover.jpg" width="880" alt="Covers of the five digital-human videos made with the local ComfyUI route">

| 🖥️ Fully local | 🔑 No credits · no API keys | 💬 One sentence per video |
|:---:|:---:|:---:|
| Voice, picture, music and edit all run on your GPU | Generation calls no cloud API; the only cost is GPU time | No prompts to write, no nodes to wire, no editing software |

<sub>Based on <a href="https://github.com/andyhuo520/digital-human-koubo">andyhuo520/digital-human-koubo</a> by Berryxia. This repository adds a fully local ComfyUI route.</sub>

</div>

---

## One sentence, one finished video

You tell your agent:

```text
Make a talking-head video locally: 9:16 with animated captions, host ella, 45 seconds, about five talking-head styles from one photo and one GPU, lively captions.
```

One RTX 3090 later, you get this 44-second video (click the image for the full video with sound):

<div align="center">
<!-- To play the video inline with sound: edit this file on github.com, drag the MP4 into the editor, and replace the <a> block below with the generated user-attachments link -->
<a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4"><img src="docs/gifs/local-b-five-styles.gif" width="270" alt="Preview of the Style B captioned talking-head video"></a><br>
<a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4">▶ Watch (with sound)</a>
</div>

Along the way you only say "yes" twice: once to the GPU-time estimate, once after seeing segment 1.

**Contents**: [Quick start](#quick-start) · [Who it's for](#who-its-for--who-its-not-for) · [Demos](#demos) · [What you don't have to do](#what-you-dont-have-to-do) · [Example requests](#example-requests) · [Pipeline](#from-one-sentence-to-a-finished-video) · [Local vs cloud](#local-vs-cloud) · [Styles and packaging](#five-editing-styles) · [Docs](#docs) · [Responsible use](#responsible-use) · [License](#license--third-party)

---

## Quick start

**You need**: an NVIDIA GPU with 24 GB of VRAM, [ComfyUI](https://github.com/comfyanonymous/ComfyUI) 0.44 or newer, and an agent that can run commands on your machine (tested with Claude Code).

**① Download and install the skills into your agent**

```bash
git clone https://github.com/walkskysu/digital-human-koubo-comfyui.git
cd digital-human-koubo-comfyui
mkdir -p ~/.claude/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.claude/skills/
```

**② Check the setup with one command**

```bash
bash ~/.claude/skills/digital-human-koubo/scripts/doctor.sh
```

It ticks off what is already installed and lists what is missing (ffmpeg, Node.js, whisper, ComfyUI models…) with ways to install each. You don't have to hunt for models: open the matching built-in template in ComfyUI and it offers to download the missing ones. The full list is in the **[install guide](docs/INSTALL.md)**.

**③ Start ComfyUI and tell your agent one sentence**

```text
Make a talking-head video locally about the rule of 72, 40 seconds, 9:16.
```

The skill uses the local route whenever `127.0.0.1:8188` is up. Two sample AI digital-human presenters and their voice samples are included, so you can make a first video without preparing a photo or a recording:

| Presenter | Look | Aspect ratio |
|---|---|---|
| `annie` (default) | studio medium shot | portraits for both 16:9 and 9:16 |
| `ella` | selfie close-up | 9:16 |

Without a named presenter the skill uses `annie`; to switch, say "host ella" in your request.

<details>
<summary>Not using Claude Code? Setup for other agents</summary>

The local route needs an agent that can **load Agent Skills** (the standard `SKILL.md` format) and **run commands on your computer**. No MCP is required.

| Agent | Skills | Status |
|---|---|---|
| **Claude Code** | `~/.claude/skills/` | ✅ Tested; the demo videos were made with it |
| **Codex** (CLI / desktop) | `~/.codex/skills/` | ✅ Expected to work (same scripts) |
| **OpenClaw** | skills folder per OpenClaw docs | ⚙️ Should work |
| **WorkBuddy** | Skills → import the folder / zip | ⚙️ Should work; menu names may differ by version |
| **豆包 (Doubao)** · **千问办公 (Qwen Office)** · **纳米Work (NamiWork)** and others | import if the product supports Agent Skills | ⚙️ Must be able to run local commands |
| **Claude desktop / claude.ai** | upload the skill zip in Settings | ⚠️ Sandbox only, so the local route won't run; scripting and generation for the [cloud route](docs/CLOUD.md) only |

</details>

---

## Who it's for / who it's not for

| ✅ A good fit | ❌ Not yet a good fit |
|---|---|
| You have an NVIDIA GPU with 24 GB of VRAM (tested on an RTX 3090 with 34 GB of RAM) | No discrete GPU, or you want a video within minutes → use the [cloud route](docs/CLOUD.md) |
| You're fine letting the GPU work for a while: a 40-second video takes about **40–70 minutes** of GPU time | Less than 24 GB of VRAM: untested, no promise it runs |
| You'd rather not pay credits per second or upload your photo and voice to a generation service | Videos several minutes long: possible, but GPU time grows with the segment count (about 8 minutes per 10 seconds of speech) |
| Windows (ComfyUI Desktop) + WSL2, or native Linux | You never want to touch a command line: setup takes a few commands |

Measured times (RTX 3090):

| Job | Time |
|---|---|
| One cloned voice line (5–14 s) | seconds |
| One lip-synced presenter segment (10 s) | ~8 min |
| One scene image | 25–50 s |
| One B-roll shot (5 s) | 5–6 min |
| One music track (35–50 s) | 1–2 min |

---

## Demos

One video per editing style, each made end to end on a single RTX 3090. Under each is a sentence you could say to make that kind of video. Click an image or "Watch" for the full video with sound.

| | |
|:---:|:---:|
| <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4"><img src="docs/gifs/local-a-72-rule.gif" width="400"></a> | <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4"><img src="docs/gifs/local-c-h3-launch.gif" width="400"></a> |
| **Style A · Xiaolin-style explainer** · 16:9 · 35 s · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4)<br><sub>"Make a talking-head video locally, Xiaolin-style explainer: the rule of 72 (how long until your money doubles), 16:9, 35 seconds. Open with text behind the presenter, put the worked example on a board with a presenter window."</sub> | **Style C · Launch breakdown** · 16:9 · 41 s · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4)<br><sub>"Make a talking-head video locally, launch breakdown: MiniMax H3 is open source and generates picture and sound together, 40 seconds, presenter at the side, with spec cards."</sub> |
| <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4"><img src="docs/gifs/local-d-tutorial.gif" width="400"></a> | <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4"><img src="docs/gifs/local-e-relay.gif" width="400"></a> |
| **Style D · Step-by-step tutorial** · 16:9 · 44 s · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4)<br><sub>"Make a talking-head video locally, step-by-step tutorial: a talking-head video on your own PC in three steps (clone the voice → generate the video → edit), 16:9, 45 seconds."</sub> | **Style E · Two-host relay** · 16:9 · 37 s · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4)<br><sub>"Make a talking-head video locally: annie and ella take turns on three Singles' Day shopping traps, 16:9, 40 seconds."</sub> |

Style B (9:16 talking head with animated captions) is [the one at the top of this page](#one-sentence-one-finished-video).

> All presenters are AI digital humans (`assets/host_annie_*.png` and the voice samples are AI-generated, not real people), and every video carries the label "内容由 AI 数字人演绎" (performed by an AI digital human). The demo videos are in Chinese.

---

## What you don't have to do

| | What the skill does for you |
|---|---|
| **Generation** | No prompts to write and no ComfyUI nodes to wire. The agent writes the script, clones the voice, generates a lip-synced presenter from that voice, and adds scene images, B-roll and music where needed. The presenter's face, outfit and voice live in `persona.json`, so every video is the same person. |
| **Cost control** | No wasted GPU time. Before anything runs you get "segments · seconds · GPU time" and it waits for your "yes"; it makes segment 1 for you to check before batching the rest. Interrupted runs resume, and only changed segments are redone. |
| **QA** | No listening through every line yourself. Each voice line is transcribed and compared with the script, and a misread line is re-voiced on its own; frames from every segment are checked; separately generated clips are processed to sound like one recording. |
| **Editing** | No editing software. The agent recommends an editing style for your content, adds captions, graphics, sound effects and music, normalises loudness and splices the cover in as the first frame. Ask for anything you want added or removed. |

It also handles multiple presenters taking turns, other languages (English, Japanese, Korean, French, Spanish and Arabic tested), and placing the presenter in a generated scene (livestream studio, shop, street).

---

## Example requests

Talk to your agent in plain language; "make a talking-head video locally" is enough to start (in Chinese: 「在本地做个口播」). Saying "locally" picks the local route; if you don't, it still defaults to local whenever ComfyUI is running.

```text
# A · Xiaolin-style explainer (16:9, finance / tech events)
Make a talking-head video locally: compound vs. simple interest in the Xiaolin style, 1 minute, with two B-roll shots in the middle.

# B · Talking head with animated captions (9:16, picks / reviews / rants)
Make a local 30-second vertical review: I've used these noise-cancelling earbuds for three months, three pros and one con, standard captions, end by asking viewers to comment.

# C · Launch breakdown (16:9, new products / models)
Make a local 45-second launch breakdown: Qwen3-TTS clones a voice from a dozen seconds of audio; three highlights and one limitation.

# D · Step-by-step tutorial (16:9, "how to…")
Make a local tutorial: installing the Lightning LoRA in ComfyUI in four steps, with terminal footage and a step tracker for each.

# E · Multi-host · multi-language · multi-scene (16:9)
annie and ella take turns on three renting traps: put annie in a Qwen Image apartment-complex scene for the second one, and have ella do the third in English.

# General
Use my digital human skill to present this: … (paste your content)
Generate the BGM with MiniMax Music and redo the sound effects with earshot.
Add a map route when she mentions these countries. / Put "¥99" behind her. / Add a teaser cold open.
Show me the packaging gallery.
```

**Use your own presenter**: record 12–20 seconds of clean speech, add a frontal photo, and add one entry to `persona.json → comfy.hosts` ([details](docs/WORKFLOWS.md#presenters-for-the-local-route)). Use only your own face and voice, or ones you have explicit permission to use.

---

## From one sentence to a finished video

```
your sentence
  │
  ├─ agent diagnoses the content, recommends a style, writes the script, estimates GPU time   ◄ you approve ①
  │
  ├─ Qwen3-TTS        clones the presenter's voice → auto back-check, misread lines re-voiced alone
  ├─ MiniMax H3       generates the presenter from that audio (lips match by construction)   ◄ segment 1 first, you approve ②
  ├─ Qwen Image 2.1   scene images       ┐
  ├─ MiniMax H3       B-roll             ├ as needed
  ├─ MiniMax Music 3  BGM · earshot SFX  ┘
  │
  ├─ voice unification → word-level timeline → Remotion edit and packaging → loudness
  └─ cover spliced in as the first frame → finished MP4
```

The local route goes **voice first, then picture**: the mouth is generated from the final audio, so lip sync holds even with a cloned voice and nothing is re-voiced afterwards. Every model runs inside your ComfyUI; the scripts submit jobs through its local HTTP API (default `http://127.0.0.1:8188`).

Which script, workflow and model files each step uses: see [Workflows and architecture](docs/WORKFLOWS.md). To run a step by hand, drag a file from [`workflows/`](workflows/) onto the ComfyUI canvas.

---

## Local vs cloud

The local route is what this repository adds to the original project. The original cloud route (Renoise MCP) is still included; choose per video.

| | **Local ComfyUI (added here)** | Cloud Renoise MCP (original project) |
|---|---|---|
| Cost | 0 credits; GPU time and electricity | Credits per second (a 27-second livestream ad took 482) |
| Accounts / keys | None needed for generation | A Renoise account and credits |
| Where your material goes | Photo, voice and video are generated on your machine and not uploaded to a generation service ¹ | Reference image and script are uploaded for cloud generation |
| Hardware | NVIDIA GPU with 24 GB of VRAM | No GPU needed |
| Time | ~40–70 min for a 40-second video (3090) | Doesn't use your GPU |
| Lip sync | Generated from the final voice, cloned voices included | Follows the model's own voice; swapping the voice later leaves ~100 ms offset |
| Models | Qwen3-TTS · MiniMax H3 · Qwen Image 2.1 · MiniMax Music 3 · BiRefNet | Grok Video 1.5 · GPT Image 2.5 · Wan 3.0 |

<sub>¹ Generation happens on your machine. If your agent runs on a cloud LLM, the script and the frames it inspects still pass through that model.</sub>

Setup, demos and costs for the cloud route: [docs/CLOUD.md](docs/CLOUD.md).

---

## Five editing styles

<p align="center"><img src="docs/images/five-styles.jpg" width="820" alt="The five editing styles"></p>

| Style | Ratio | Best for |
|---|---|---|
| **A** Xiaolin-style explainer | 16:9 | finance / tech events, data, "why…" |
| **B** Talking head with animated captions | 9:16 | product picks, sales, reviews, rants (three caption intensities: restrained / standard / lively) |
| **C** Launch breakdown | 16:9 | new products / models |
| **D** Step-by-step tutorial | 16:9 | "how to…", tool setup |
| **E** Multi-host · multi-language · multi-scene | 16:9 | capability demos, going global |

You don't have to choose: the agent reads your content and recommends two, with preview images. On the local route, start with 30–60 seconds.

Each style comes with default packaging drawn from **48 packaging components**, distilled from a frame-by-frame study of 25 videos by top creators (text behind the presenter, number spikes, comparison bars, map routes, bullet comments, step trackers…). Add or remove any of them by name or by describing the effect.

<div align="center">
<a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4"><img src="docs/gifs/packaging-gallery.gif" width="560" alt="Gallery of the 48 packaging components"></a><br>
<b>Packaging component gallery</b> · 48 components · 2:40 · <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4">▶ Watch</a>
</div>

Templates, the component list and parameters: [docs/PACKAGING.md](docs/PACKAGING.md).

---

## Known pitfalls

The skill already handles all of these. Three representative ones:

- **Without the Lightning LoRA, H3 runs out of memory on 24 GB and hangs at step 0** → the presenter always uses the 4-step LoRA and B-roll the 8-step one.
- **Qwen3-TTS occasionally garbles a word** (e.g. "MiniMax" → "mini maxax") → every line is transcribed without the script and compared; a misread line gets a new seed and is re-voiced alone.
- **Concatenating dozens of clips makes the voice drift behind the lips** (0.38 s late after 44 clips) → each clip's audio is padded to its video length before concatenation, and audio/video durations are checked.

The other dozen or so, with fixes: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

---

## Docs

| Doc | Contents |
|---|---|
| [Install](docs/INSTALL.md) | ComfyUI node pack and model list, Python side, local tools, presenter voice, earshot |
| [Workflows and architecture](docs/WORKFLOWS.md) | Script pipeline, ComfyUI workflows and API graphs, model files, presenter config, GPU time, repository structure |
| [Styles and packaging](docs/PACKAGING.md) | Templates for the five styles, the 48 components, `pack` syntax, text behind the presenter |
| [Cloud route](docs/CLOUD.md) | Renoise MCP setup, cloud demos, MiMo TTS, credit costs |
| [Known pitfalls](docs/TROUBLESHOOTING.md) | Known issues on the local and cloud routes and how they are handled |
| [`workflows/`](workflows/README.md) | UI-format workflows you can drag straight into ComfyUI |

---

## Responsible use

- Use only your own face/voice or ones you have **explicit permission** to use. Never impersonate a real person or creator.
- Every video carries an "AI digital human" label; scene and animal clips are marked "AI generated".
- No made-up numbers, prices, offers or reviews; sample data on screen must be labelled as such.
- Don't use web memes, film/TV stills or celebrity images; the meme components use original stickers generated from your own presenter.
- Credits (cloud route) are spent only after you approve the quote.

## License & third-party

- Code and docs: [MIT](LICENSE) © 2026 Berryxia (andyhuo520); local ComfyUI route © 2026 walksky.
- Local route: [ComfyUI](https://github.com/comfyanonymous/ComfyUI) (GPL-3.0, installed by you) · models MiniMax H3, MiniMax Music 3, Qwen Image 2.1, Qwen3-TTS, SenseVoice, BiRefNet (downloaded by you; each has its own license, so check the model page before commercial use) · [mediapipe](https://github.com/google-ai-edge/mediapipe) (Apache-2.0) · [earshot](https://github.com/Leonxlnx/earshot) (MIT) with CLAP and AST models.
- **[Remotion](https://www.remotion.dev/)** is used for rendering and has its own license: free for individuals and companies of up to 3 people; larger companies need a [company license](https://www.remotion.pro/).
- Animated emoji: [Google Noto Emoji Animation](https://googlefonts.github.io/noto-emoji-animation/) (CC BY 4.0); credit "Animated emoji: Google Noto" in your videos.
- Maps: [world-atlas](https://github.com/topojson/world-atlas) (ISC; data from Natural Earth, public domain) · [d3-geo](https://github.com/d3/d3-geo), [topojson-client](https://github.com/topojson/topojson-client) (ISC). For maps involving China's borders in formally published content, check against applicable local standards.
- Speech recognition: [whisper.cpp](https://github.com/ggerganov/whisper.cpp) (MIT). Cloud generation runs on [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) (your account, your credits); optional TTS by [Xiaomi MiMo](https://platform.xiaomimimo.com/).
- Course screenshots in the WorkBuddy demo come from the original author's own course. Demo videos are the authors' own work; please don't re-upload them as your own.

See [THIRD_PARTY.md](THIRD_PARTY.md) for details.

---

<div align="center">

Original by **Berryxia** ([andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo)) · local ComfyUI route by **walksky** · built with Claude Code · if this helped, a ⭐ helps others find it.

</div>
