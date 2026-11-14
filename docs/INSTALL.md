# Install (local ComfyUI route)

[中文](INSTALL.zh-CN.md) · [Back to README](../README.en.md)

Once it's installed, see [Quick start](../README.en.md#quick-start) in the README.

**Tested setup:** RTX 3090 (24 GB VRAM) + 34 GB RAM. ComfyUI Desktop on Windows; the skill and agent run in WSL2 Ubuntu and reach ComfyUI at `127.0.0.1:8188`. A native Linux ComfyUI works the same way. The local route needs **no MCP server** — the scripts call ComfyUI's HTTP API directly, so any agent that can run local commands can drive it.

## 1 · Get the code

```bash
git clone https://github.com/walkskysu/digital-human-koubo-comfyui.git
cd digital-human-koubo-comfyui
```

## 2 · Install the skills into your agent

The repo contains two skills: `digital-human-koubo` (main) and `finance-explainer` (an optional engine for chart-only finance long-forms; Style A uses `templates/lin-169` in the main skill).

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.claude/skills/
# Codex
mkdir -p ~/.codex/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.codex/skills/
# WorkBuddy / OpenClaw / other agents: import this zip on the product's Skills page
cd skills && zip -r ../digital-human-skills.zip digital-human-koubo finance-explainer && cd ..
```

## 3 · ComfyUI, node pack and models

**ComfyUI 0.44 or newer.** MiniMax H3, MiniMax Music 3, Qwen Image 2.1 and BiRefNet background removal are built-in nodes. One custom node pack is needed:

- **Qwen3-TTS** node pack (`Qwen3TTSLoader`, `Qwen3TTSVoiceClone`, `Qwen3TTSSenseVoiceASR`, …) — install it from ComfyUI Manager. It downloads `Qwen/Qwen3-TTS-12Hz-1.7B-Base` and `iic/SenseVoiceSmall` on first use.

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
| | `qwen3.5_9b_qwen_image_2.1_pe_t2i.int8_convrot.safetensors` | Qwen Image 2.1 prompt enhancer (optional, `--enhance`) |
| | `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` | Music 3 |
| `vae/` | `minimax_h3_video_vae_int8_convrot.safetensors`, `minimax_h3_audio_vae_fp32.safetensors` | H3 |
| | `qwen_image_2.1_vae_bf16.safetensors` | Qwen Image 2.1 |
| | `minimax_music3_dav.safetensors` | Music 3 |
| `background_removal/` | `birefnet.safetensors` | text-behind-presenter cutout |

The easiest way to get them is to open the matching ComfyUI templates (*MiniMax H3 Reference to Video*, *MiniMax H3 Image to Video*, *Qwen Image 2.1 Text to Image*, *MiniMax Music 3*), which offer to download missing models. If a file name differs in your install, change it in the JSON under `skills/digital-human-koubo/comfy/`.

> The **Lightning LoRAs are required on 24 GB.** Without them H3 at 0.8 MP runs out of memory and hangs at step 0.

## 4 · Python side and local tools

Where the skill runs (WSL2 / Linux / macOS):

```bash
python3 -m venv ~/.venvs/koubo && source ~/.venvs/koubo/bin/activate
pip install av numpy pillow playwright mediapipe && python -m playwright install chromium
curl -L -o ~/models/blaze_face_short_range.tflite \
  https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite
curl -s http://127.0.0.1:8188/system_stats   # ComfyUI reachable?
```

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

## 5 · Your presenter's voice

Record 12–20 s of clean, dry speech of **your own** voice (or one you're licensed to use), save it under `assets/`, and set `voice_ref` and `voice_ref_text` (the exact words) for the host in `persona.json → comfy.hosts`. Two AI-generated sample presenters are included (see [Presenters](WORKFLOWS.md#presenters-for-the-local-route)).

## 6 · earshot — sound effects and BGM check

[Leonxlnx/earshot](https://github.com/Leonxlnx/earshot), MIT:
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

## 7 · Placeholder sound effects & music (optional)

The repo ships **no third-party audio**. Generate an original set of 30 sound effects and a placeholder background track (pure code, no copyright):
```bash
python3 ~/.claude/skills/digital-human-koubo/scripts/make_assets.py
```
`new_edit.sh` also runs this automatically for every new project. With the local route, MiniMax Music 3 replaces the placeholder track.
