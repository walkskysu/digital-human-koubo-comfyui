# 安装（本地 ComfyUI 路线）

[English](INSTALL.md) · [返回 README](../README.md)

装好后看 README 的[快速开始](../README.md#快速开始)。

**实测环境**：RTX 3090（24 GB 显存）+ 34 GB 内存。Windows 上跑 ComfyUI Desktop；Skill 和 Agent 在 WSL2 Ubuntu 里，通过 `127.0.0.1:8188` 连过去。Linux 原生 ComfyUI 一样用。本地路线**不需要 MCP**：脚本直接调 ComfyUI 的 HTTP API，只要 Agent 能在本机跑命令就能驱动。

## 1 · 下载代码

```bash
git clone https://github.com/walkskysu/digital-human-koubo-comfyui.git
cd digital-human-koubo-comfyui
```

## 2 · 把 Skill 装进你的 Agent

仓库里有两个 Skill：`digital-human-koubo`（主 Skill）和 `finance-explainer`（纯图表、不出镜的财经长片引擎，可选；风格 A 用主 Skill 里的 `templates/lin-169`）。

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.claude/skills/
# Codex
mkdir -p ~/.codex/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.codex/skills/
# WorkBuddy / OpenClaw / 其他 Agent：打成压缩包，在产品的「技能」页面导入
cd skills && zip -r ../digital-human-skills.zip digital-human-koubo finance-explainer && cd ..
```

## 3 · ComfyUI、节点包和模型

**ComfyUI 0.44 或更新**。MiniMax H3、MiniMax Music 3、Qwen Image 2.1、BiRefNet 去背景都是内置节点。另外要装一个自定义节点包：

- **Qwen3-TTS** 节点包（`Qwen3TTSLoader`、`Qwen3TTSVoiceClone`、`Qwen3TTSSenseVoiceASR` 等）：在 ComfyUI Manager 里装。第一次用时会自动下载 `Qwen/Qwen3-TTS-12Hz-1.7B-Base` 和 `iic/SenseVoiceSmall`。

**模型文件**（放进 ComfyUI `models/` 下对应的子目录）：

| 目录 | 文件 | 用途 |
|---|---|---|
| `diffusion_models/` | `minimax_h3_ref2va_pruned_int8_convrot.safetensors` | 主播对口型 |
| | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` | B-roll |
| | `qwen_image_2.1_int8_convrot.safetensors` | 场景图 |
| | `minimax_music3_dit_fp16.safetensors` | 配乐 |
| `loras/` | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16.safetensors` | 主播 4 步 |
| | `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` | B-roll 8 步 |
| `text_encoders/` | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | H3 |
| | `qwen3vl_8b_int8_convrot.safetensors` | Qwen Image 2.1 |
| | `qwen3.5_9b_qwen_image_2.1_pe_t2i.int8_convrot.safetensors` | Qwen Image 2.1 提示词增强（可选，`--enhance`） |
| | `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` | Music 3 |
| `vae/` | `minimax_h3_video_vae_int8_convrot.safetensors`、`minimax_h3_audio_vae_fp32.safetensors` | H3 |
| | `qwen_image_2.1_vae_bf16.safetensors` | Qwen Image 2.1 |
| | `minimax_music3_dav.safetensors` | Music 3 |
| `background_removal/` | `birefnet.safetensors` | 景深字抠像 |

最省事的办法是在 ComfyUI 里打开对应模板（*MiniMax H3 Reference to Video*、*MiniMax H3 Image to Video*、*Qwen Image 2.1 Text to Image*、*MiniMax Music 3*），缺模型时它会提示下载。如果你那边文件名不一样，改 `skills/digital-human-koubo/comfy/` 下的 JSON 即可。

> 24 GB 显存**必须**开 Lightning LoRA。不开的话 H3 在 0.8MP 下会爆显存，卡在第 0 步。

## 4 · Python 环境和本机工具

Skill 跑的那台机器（WSL2 / Linux / macOS）：

```bash
python3 -m venv ~/.venvs/koubo && source ~/.venvs/koubo/bin/activate
pip install av numpy pillow playwright mediapipe && python -m playwright install chromium
curl -L -o ~/models/blaze_face_short_range.tflite \
  https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite
curl -s http://127.0.0.1:8188/system_stats   # 能连上 ComfyUI 吗？
```

| 工具 | macOS | Windows | Linux |
|---|---|---|---|
| ffmpeg | `brew install ffmpeg` | `winget install Gyan.FFmpeg` | `sudo apt install ffmpeg` |
| Python 3 + numpy + Pillow | `brew install python` 后 `python3 -m pip install numpy pillow` | `winget install Python.Python.3.12` | `sudo apt install python3-pip` |
| Playwright + Chromium（封面排版） | `python3 -m pip install playwright && python3 -m playwright install chromium` | 同左 | 同左 |
| Node.js 18+（Remotion） | `brew install node` | `winget install OpenJS.NodeJS.LTS` | `nvm install --lts` |
| whisper.cpp（`whisper-cli`） | `brew install whisper-cpp` | [Releases 下载](https://github.com/ggerganov/whisper.cpp/releases) | [源码编译](https://github.com/ggerganov/whisper.cpp) |
| whisper 模型 | 下载 [`ggml-medium-q5_0.bin`](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium-q5_0.bin) 放到 `~/models/`（或 `export WHISPER_MODEL=模型路径`） | 同左 | 同左 |

一条命令检查：已经装好的打勾跳过，缺什么列出多种装法：
```bash
bash ~/.claude/skills/digital-human-koubo/scripts/doctor.sh
```

## 5 · 主播的声音

录 12–20 秒干净、无混响的**你自己的**声音（或你有授权的声音），放进 `assets/`，在 `persona.json → comfy.hosts` 里给这个主播填 `voice_ref` 和 `voice_ref_text`（逐字文本）。仓库自带两个 AI 生成的示例主播（见[本地路线的主播](WORKFLOWS.zh-CN.md#本地路线的主播)）。

## 6 · earshot：音效 + 配乐检查

[Leonxlnx/earshot](https://github.com/Leonxlnx/earshot)，MIT：
```bash
git clone https://github.com/Leonxlnx/earshot ~/tools/earshot && cd ~/tools/earshot
python3 -m venv .venv && .venv/bin/pip install -e . && sudo ln -s ~/tools/earshot/.venv/bin/earshot /usr/local/bin/earshot
earshot doctor --fetch     # 下载 CLAP（laion/larger_clap_general）+ AST（MIT/ast-finetuned-audioset-10-10-0.4593），约 1.1 GB
```
`lin_sfx.py` 只用 `earshot kit init/render`，不需要模型；`earshot describe`（检查生成的配乐没有人声、曲风对不对）要这两个模型。想放在自己的目录、只从本地读，把下面几行写进 `~/.bashrc`，而且要写在 `case $- in *i*) ;; *) return;; esac` 那行**之前**，否则 Agent 起的脚本读不到：
```bash
export EARSHOT_CLAP=~/models/earshot/larger_clap_general
export EARSHOT_AST=~/models/earshot/ast-audioset
export EARSHOT_HOME=~/models/earshot/cache
export EARSHOT_OFFLINE=1
```

## 7 ·（可选）占位音效与配乐

仓库**不带任何第三方音频**。用代码合成一套原创音效（30 个）和一条占位配乐（无版权）：
```bash
python3 ~/.claude/skills/digital-human-koubo/scripts/make_assets.py
```
`new_edit.sh` 每次起新工程也会自动跑。走本地路线时，配乐由 MiniMax Music 3 生成，替换掉占位曲。
