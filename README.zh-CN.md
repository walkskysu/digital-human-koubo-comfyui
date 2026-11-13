<div align="center">

# Digital Human Koubo · 本地 ComfyUI 版

**一张照片 + 一段稿子 → 一条对好口型的数字人口播成片，全部在你自己的显卡上生成。**
声音克隆、对口型、场景图、B-roll、配乐、字幕、头部博主级包装，由你的 AI Agent 通过**本地 ComfyUI** 自动完成。不花积分，不要 API Key。

[English](README.md) · **简体中文**

<sub>基于 Berryxia 的 <a href="https://github.com/andyhuo520/digital-human-koubo">andyhuo520/digital-human-koubo</a>，本版本新增全本地 ComfyUI 路线。</sub>

[![Local ComfyUI](https://img.shields.io/badge/generation-local%20ComfyUI-3b5bdb)](https://github.com/comfyanonymous/ComfyUI)
![Tested on RTX 3090](https://img.shields.io/badge/tested-RTX%203090%2024GB-76b900)
![Open models](https://img.shields.io/badge/models-MiniMax%20H3%20·%20Qwen3--TTS%20·%20Qwen%20Image%202.1-6e40c9)
[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](LICENSE)
![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-orange)
![Remotion](https://img.shields.io/badge/edit-Remotion%204-0b84f3)

<img src="docs/images/local-cover.jpg" width="880" alt="本地 ComfyUI 路线做的五条成片封面">

</div>

> **上面五条片子全部在一张 RTX 3090 上生成**：配音、对口型主播、场景图、B-roll、配乐、音效。
> **Qwen3-TTS** 克隆主播声音 → **MiniMax H3** *照着这段配音*生成主播画面，口型自然对上 → **Qwen Image 2.1** 出场景 → **MiniMax Music 3** 出配乐 → **earshot** 做音效 → **Remotion** 剪辑包装。
> 直达：[成片示例](#本地路线成片示例) · [安装](#安装本地-comfyui-路线) · [ComfyUI 工作流](#comfyui-工作流) · [快速开始](#快速开始)
>
> 原来的云端路线（[Renoise MCP](#云端路线renoise-mcp可选)：Grok Video、GPT Image、Wan）仍然保留，每条片子可以自己选。

---

## 本地路线成片示例

每种剪辑风格各做了一条短片，全部用本地路线在 RTX 3090 上从头做到成片（40 秒左右的成片约占 40–70 分钟 GPU 时间）。点 GIF 或「播放」看完整视频。

<div align="center">
<a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4"><img src="docs/gifs/local-b-five-styles.gif" width="270"></a><br>
<b>风格 B · 网红花字口播</b> · 9:16 · 44 秒 · 8 段<br>
「一张照片做出五种口播」：自拍 vlog 和全身镜头交替，花字、表情、画中画<br>
<a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4">▶ 播放</a>
</div>

| | |
|:---:|:---:|
| <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4"><img src="docs/gifs/local-a-72-rule.gif" width="400"></a> | <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4"><img src="docs/gifs/local-c-h3-launch.gif" width="400"></a> |
| **风格 A · 财经解说** · 16:9 · 35 秒<br>「72 法则」：景深字、题板 + 主播小窗、对比条、H3 B-roll<br>[▶ 播放](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4) | **风格 C · 发布解读** · 16:9 · 41 秒<br>「MiniMax H3：画面和声音一起出」：主播在侧边，参数卡<br>[▶ 播放](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4) |
| <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4"><img src="docs/gifs/local-d-tutorial.gif" width="400"></a> | <a href="https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4"><img src="docs/gifs/local-e-relay.gif" width="400"></a> |
| **风格 D · 保姆级教程** · 16:9 · 44 秒<br>「三步做出本地数字人口播」：终端、时间线、步骤追踪<br>[▶ 播放](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4) | **风格 E · 双主播接力** · 16:9 · 37 秒<br>「双 11 先别急着付款：3 个坑」：两位主播、Qwen Image 场景、一句英文<br>[▶ 播放](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4) |

> 主播全部是 AI 数字人（`assets/host_girl_*.png` 和声音样本都是 AI 生成的，不是真人），每条片子都标了「内容由 AI 数字人演绎」。原项目云端路线的示例在下面的[云端路线](#云端路线renoise-mcp可选)。
>
> 每条片子用的提示词（每种风格三段）见 [docs/local-prompts.zh-CN.md](docs/local-prompts.zh-CN.md)。

---

## 安装（本地 ComfyUI 路线）

**实测环境**：RTX 3090（24 GB 显存）+ 34 GB 内存。Windows 上跑 ComfyUI Desktop；Skill 和 Agent 在 WSL2 Ubuntu 里，通过 `127.0.0.1:8188` 连过去。Linux 原生 ComfyUI 一样用。本地路线**不需要 MCP**：脚本直接调 ComfyUI 的 HTTP API，只要 Agent 能在本机跑命令就能驱动。

### 1 · 下载代码

```bash
git clone https://github.com/walkskysu/digital-human-koubo-comfyui.git
cd digital-human-koubo-comfyui
```

### 2 · 把 Skill 装进你的 Agent

仓库里有两个 Skill：`digital-human-koubo`（主 Skill）和 `finance-explainer`（纯图表、不出镜的财经长片引擎，可选；风格 A 用主 Skill 里的 `templates/lin-169`）。

```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.claude/skills/
# Codex
mkdir -p ~/.codex/skills && cp -R skills/digital-human-koubo skills/finance-explainer ~/.codex/skills/
# WorkBuddy / OpenClaw / 其他 Agent：打成压缩包，在产品的「技能」页面导入
cd skills && zip -r ../digital-human-skills.zip digital-human-koubo finance-explainer && cd ..
```

### 3 · ComfyUI、节点包和模型

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

### 4 · Python 环境和本机工具

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

### 5 · 主播的声音

录 12–20 秒干净、无混响的**你自己的**声音（或你有授权的声音），放进 `assets/`，在 `persona.json → comfy.hosts` 里给这个主播填 `voice_ref` 和 `voice_ref_text`（逐字文本）。仓库自带两个 AI 生成的示例主播（见[本地路线的主播](#本地路线的主播)）。

### 6 · earshot：音效 + 配乐检查

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

### 7 ·（可选）占位音效与配乐

仓库**不带任何第三方音频**。用代码合成一套原创音效（30 个）和一条占位配乐（无版权）：
```bash
python3 ~/.claude/skills/digital-human-koubo/scripts/make_assets.py
```
`new_edit.sh` 每次起新工程也会自动跑。走本地路线时，配乐由 MiniMax Music 3 生成，替换掉占位曲。

---

## ComfyUI 工作流

### 本地路线逐步说明

云端路线是先出画面、声音用视频模型自带的。本地路线**反过来：先配音，再出画面**。配音作为 `<Audio 1>`（fully_copy）喂给 MiniMax H3，嘴型是**照着最终音频**生成的，所以用克隆声音口型也是准的，事后不用再换声音。

```
script.json ─► comfy_batch.py --stage plan     估每段要多少 GPU 时间
            ─► comfy_batch.py --stage tts      Qwen3-TTS 克隆主播的 voice_ref（12–20 秒干声 + 逐字文本）
                                               └► SenseVoice 不带原文转写，准确率 < 90% 打 ⚠
                                                  念错：在 script.json 那段加 "seed": 新数 再跑（只重配那一段）
            ─► comfy_batch.py --stage video    MiniMax H3 参考生视频，4 步 Lightning LoRA
                                               <Picture 1> = 主播照片或场景图（"ref"）
                                               <Audio 1>   = 配音，fully_copy → 对口型
                                               提示词用 H3 Ref2VA 格式 → gen/prompts/<id>.txt
                                               进度存 gen/state.json（可续跑，只重做改过的段）
            ─► assemble.py --src 'gen/{id}.mp4' → align.py → tl.json → Remotion → 响度 → 封面
旁支任务：   comfy_scene.py  （Qwen Image 2.1 文生图，主播照当参考图：直播间 / 门店 / 街景，四视图，贴纸）
             comfy_broll.py  （H3 文生 / 图生视频 B-roll，16:9）
             comfy_music.py  （MiniMax Music 3 纯音乐配乐 → 用 `earshot describe` 检查）
             cutout_video.py （BiRefNet 抠像，Linux / Windows 上做景深字）
             face_center.py  （mediapipe 量脸，风格 A 构图用）
```

### 界面格式工作流（`workflows/`）

把文件拖进 ComfyUI 画布（或「工作流 → 打开」）就能看、能手动跑。图片 / 音频输入都换成了 `example.png` / `example.flac`，用时换成你自己的。每个 API 版本具体改了什么，见 [`workflows/README.md`](workflows/README.md)。

| 工作流 | 用途 | Skill 实际提交的 API 版本 |
|---|---|---|
| [`qwen3_tts_voice_clone.json`](workflows/qwen3_tts_voice_clone.json) | Qwen3-TTS 声音克隆 + SenseVoice 回听 | `comfy/tts_clone.api.json` |
| [`qwen3_tts_voice_design.json`](workflows/qwen3_tts_voice_design.json) | 用文字描述设计新音色 | —（只用来做示例声音样本） |
| [`video_minimax_h3_r2v_3ref.json`](workflows/video_minimax_h3_r2v_3ref.json) | MiniMax H3 参考生视频，4 步 Lightning LoRA | `comfy/h3_r2v_audio.api.json`（1 张参考图 + 配音当 `<Audio 1>`） |
| [`video_minimax_h3_i2v.json`](workflows/video_minimax_h3_i2v.json) | MiniMax H3 图生视频，8 步 Lightning LoRA | `comfy/h3_i2v.api.json`（没首帧时变文生视频） |
| [`image_qwen_image_2_1_t2i.json`](workflows/image_qwen_image_2_1_t2i.json) | Qwen Image 2.1 文生图，可选提示词增强 | `comfy/qwen_t2i.api.json`（可接参考图） |
| [`audio_minimax_music_3.json`](workflows/audio_minimax_music_3.json) | MiniMax Music 3 歌曲 / 纯音乐 | `comfy/music.api.json` |
| [`birefnet_remove_background.json`](workflows/birefnet_remove_background.json) | BiRefNet 人像 / 背景遮罩 | `scripts/cutout_video.py` 里拼（视频输入，按 8 秒分块） |

### 脚本提交的 API 格式图（`skills/digital-human-koubo/comfy/`）

都是展平的 API 格式图。脚本读进来，填上文字 / 图片 / 音频 / 种子，通过 ComfyUI 的 REST API（`/upload`、`/prompt`、`/history`、`/view`）提交和取回。地址在 `persona.json` 的 `comfy.url`（默认 `http://127.0.0.1:8188`）。

| 文件 | 谁在用 | 主要节点 | 模型文件 |
|---|---|---|---|
| `tts_clone.api.json` | `comfy_batch.py` | `Qwen3TTSLoader` · `Qwen3TTSVoiceClonePrompt` · `Qwen3TTSVoiceClone` | `Qwen/Qwen3-TTS-12Hz-1.7B-Base`（节点包自动下载） |
| `h3_r2v_audio.api.json` | `comfy_batch.py` | `MiniMaxH3ReferenceToVideo` · `SamplerCustomAdvanced` · `CreateVideo` | `minimax_h3_ref2va_pruned_int8_convrot` · LoRA `minimax_h3_ref2v_turbo_4step_v0.1` · 文本编码器 `qwen3vl_32b_minimax_h3_nvfp4_awq` · VAE `minimax_h3_video_vae_int8_convrot`、`minimax_h3_audio_vae_fp32` |
| `h3_i2v.api.json` | `comfy_broll.py` | `MiniMaxH3ImageToVideo` | `minimax_h3_fl2va_pruned_int8_convrot` · LoRA `minimax_h3_fl2v_turbo_8step_v1.0` · 文本编码器和 VAE 同上 |
| `qwen_t2i.api.json` | `comfy_scene.py` | `TextEncodeQwenImage21` · `QwenImage21Cache` · 可选提示词增强 `TextGenerate` | `qwen_image_2.1_int8_convrot` · `qwen3vl_8b_int8_convrot` · `qwen_image_2.1_vae_bf16` · 增强器 `qwen3.5_9b_qwen_image_2.1_pe_t2i.int8_convrot`（只在 `--enhance` 时用） |
| `music.api.json` | `comfy_music.py` | `MiniMaxMusic3TextEncode` · `EmptyMiniMaxMusic3LatentAudio` · `KSampler` | `minimax_music3_dit_fp16` · `minimax_music3_text_encoder_pruned_int8_convrot` · `minimax_music3_dav` |
| *（脚本里拼）* | `cutout_video.py` | `LoadBackgroundRemovalModel` · `RemoveBackground` | `birefnet.safetensors` |
| *（脚本里拼）* | `comfy_batch.py` | `Qwen3TTSSenseVoiceASR` | `iic/SenseVoiceSmall`（节点包自动下载） |

### 本地路线的主播

`persona.json → comfy.hosts` 定义每个本地主播：照片（`avatar`）、输出尺寸、声音样本（`voice_ref` + `voice_ref_text`）、给提示词用的英文外形描述（`look`；另有只写人物、不写布景的 `look_person`，配场景图时用）、声音描述、默认构图。自带两个：`tank`（默认的白背心主播，`assets/avatar_ref.jpg`）和 `girl`（`assets/host_girl_*.png`）。`girl` 的形象图和两个声音样本（`assets/voice_ref_*.flac`）都是 AI 生成的，不是真人。H3 提示词模板在 `comfy.prompt_template`（Ref2VA 格式：subject_definitions / summary / retention_analysis / detailed_description / soundscape / music）。

### GPU 用时（RTX 3090 24 GB，实测）

不花积分，花的是 GPU 时间。

| 任务 | 设置 | 用时 |
|---|---|---|
| 克隆配音（Qwen3-TTS） | 一句 5–14 秒 | 几秒 |
| 主播一段（H3 Ref2VA） | 10 秒，672×1216 或 1216×672，4 步 | 约 8 分钟（4–9 分钟） |
| 场景图（Qwen Image 2.1） | 25 步 | 25–50 秒（第一张含加载最多约 5 分钟） |
| B-roll（H3 T2VA / I2VA） | 5 秒，1216×672，8 步 | 5–6 分钟 |
| 配乐（MiniMax Music 3） | 35–50 秒纯音乐，30 步 | 1–2 分钟 |

一条 40 秒左右的成片（5–8 段口播）约占 40–70 分钟 GPU 时间。

---

## 快速开始

直接用大白话跟 Agent 说：

```text
用本地 ComfyUI 做，不花积分：两个主播接力讲双 11 的三个坑，16:9，40 秒。
用本地 ComfyUI 做一条 40 秒 9:16 花字口播，讲 72 法则。
用我的数字人 Skill 讲这段：……（粘贴你的内容）
用 MiniMax Music 生成配乐，用 earshot 重做音效再混音。
讲到这几个国家的时候加地图航线 / 把「¥99」放在她身后 / 开场加个预告闪回。
把包装组件图鉴发我看看
```

接下来会发生：
1. 环境检查：已经装好的直接跳过。
2. 一行诊断 + 推荐 2 种风格（附预览图），一次问完。
3. 稿子 + 场景设计 + **GPU 用时估算**（本地）或**积分报价**（云端）→ 你确认 → 先做第 1 段 → 你确认 → 批量。
4. 质检、修音，按风格默认包装剪辑 → 出成片 MP4，封面接成第一帧。

---

## 能做什么

- **两套生成引擎，同一条流水线**：本地用 **ComfyUI**（Qwen3-TTS、MiniMax H3、Qwen Image 2.1、MiniMax Music 3、BiRefNet），云端用 **Renoise MCP**（Grok Video 1.5、GPT Image 2.5、Wan 3.0）。写稿、质检、剪辑、包装、封面两边完全一样；跟 Agent 说「用本地 ComfyUI」就行。
- **一张照片做出固定的数字人**：脸、服装、声音、提示词模板都存在 `persona.json`，每条片子都是同一个人。想进什么场景（直播间、门店、教室、街头），先合成场景图，再让她开口。
- **先配音再出画面（本地）**：克隆的声音直接驱动 MiniMax H3，口型和最终音频完全对上。每段 ≤ 14 秒。
- **先报价，再开工**：每次生成前，Agent 先报「段数 · 秒数 · GPU 时间（或积分）」，你点头才开始；先做第 1 段给你看，满意再批量。
- **两道质检**：每句用 SenseVoice / whisper **不带原文**回听、和稿子比对，念错能抓出来；每段抽 4 帧检查。
- **声音统一**：1/3 倍频程频谱匹配 + 去齿音 + 同一个小房间混响 + 响度统一，分开生成的片段听起来像一次录完（实测齿音段间差 13.2 dB → 5.9 dB）。
- **按内容推荐剪辑风格**：Agent 先诊断内容，推荐 2 种风格并附预览图，一次问完（风格 · 比例时长 · 花字强度 · 主播）。
- **48 个包装组件**：逐帧拆了 25 支头部博主视频（MrBeast、Mark Rober、Ryan Trahan、MKBHD、影视飓风、何同学、Johnny Harris、Vox、Kurzgesagt、回形针、半佛仙人、差评、毕导）。每种风格自带默认包装，想加减直接说。
- **景深字**：大字 / 数字放在背景和人之间（Linux / Windows 用 BiRefNet，macOS 用 Apple Vision → 三层合成）。
- **封面即首帧**：每条片子默认出封面（16:9 / 9:16 / 3:4：主播帧 + 钩子大字 + 证据卡），并接成成片第一帧停 0.5 秒。平台默认拿首帧当封面，不用再单独上传。
- **多语言**：英、日、韩、法、西、阿拉伯语实测，回听准确率 94–100%。
- **多种 Agent 都能用**：标准 `SKILL.md` Agent Skill + 脚本，只要能装 Skill、能在本机跑命令，就能驱动本地路线。

## 工作流程

```
你的内容 ──► 0. 环境检查（ComfyUI / ffmpeg / whisper，已经有的直接跳过）
              1. 诊断内容 → 5 种风格里推荐 2 种 → 一次问完 → brief.json
              2. 写稿 script.json（本地每段 ≤14 秒 / 云端 ≤15 秒，中文约 5.4 字/秒）
              3. 估时 / 报价 → 等你确认 → 先做第 1 段 → 你看过 → 批量
              4. 配音 → 对口型视频（本地）或下载（云端）→ 回听 → 抽帧检查
              5. 声音统一（频谱匹配 + 去齿音 + 同一房间混响）
              6. 逐字时间轴（tl.json）
              7. Remotion 剪辑：风格模板 + 默认包装（+ 你点名的手法）
              8. 渲染 → 看过渡中间帧 → 响度（-14 / -16 LUFS）
              9. 封面：挑主播帧 → 16:9 / 9:16 / 3:4 → 接成首帧（停 0.5 秒）
```

## 架构

整个 Skill 分四层。Agent 读 `SKILL.md`，其余都通过脚本驱动；本地和云端两条路线只差在**生成层**。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Agent + SKILL.md     诊断内容 → brief.json → script.json → 一次问完/报价 │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 2a. 本地生成（ComfyUI API）          │ 2b. 云端生成（Renoise MCP）          │
│   Qwen3-TTS        克隆配音          │   Grok Video 1.5  主播画面 + 原生声音│
│   MiniMax H3 R2V   跟着配音对口型    │   GPT Image 2.5   场景图 / 四视图    │
│   Qwen Image 2.1   场景图 / 四视图   │   Wan 3.0         B-roll             │
│   MiniMax H3 T2V/I2V  B-roll         │   MiMo TTS        可选换声音         │
│   MiniMax Music 3  配乐              │   make_assets.py  占位配乐           │
│   BiRefNet         人像抠图          │   Apple Vision    人像抠图           │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ 3. 质检 + 时间轴   SenseVoice / whisper 回听 · 抽帧检查 ·                   │
│                    assemble.py（防音画漂移拼接）· align.py → tl.json        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. 剪辑 + 收尾     Remotion 模板（huazi-916 · lin-169 · reference/*）       │
│                    48 个包装组件 · earshot 音效 · 配乐随人声压低            │
│                    响度 -14/-16 LUFS · make_cover → cover_first             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 每一步用到的组件

| 步骤 | 本地路线 | 云端路线 | 脚本 |
|---|---|---|---|
| 配音 | **Qwen3-TTS 1.7B Base** 声音克隆 | Grok 原生声音 · 可选小米 MiMo TTS | `comfy_batch.py --stage tts` |
| 配音质检 | **SenseVoice Small**（在 ComfyUI 里）+ whisper.cpp | whisper.cpp | `comfy_batch.py`、`misread_check.py` |
| 主播画面 | **MiniMax H3 Ref2VA** + 4 步 Lightning LoRA | Grok Video 1.5（Renoise） | `comfy_batch.py --stage video` / `build_tasks.py` |
| 场景图、四视图、贴纸 | **Qwen Image 2.1**（主播照当参考图） | GPT Image 2.5（Renoise） | `comfy_scene.py` |
| B-roll | **MiniMax H3** T2VA / I2VA + 8 步 Lightning LoRA | Wan 3.0（Renoise） | `comfy_broll.py` |
| 配乐 | **MiniMax Music 3** | `make_assets.py` 占位曲 | `comfy_music.py` |
| 音效 | **earshot** 音效包 | `make_assets.py`（代码合成）/ earshot 音效包 | `lin_sfx.py` |
| 人像抠图 | **BiRefNet**（ComfyUI） | Apple Vision（macOS） | `cutout_video.py` |
| 量脸 | **mediapipe** BlazeFace | Apple Vision（macOS） | `face_center.py` |
| 拼接、时间轴、剪辑、封面 | ffmpeg · whisper.cpp · Remotion 4 · Playwright | 同左 | `assemble.py` · `align.py` · 模板 · `make_cover.py` |

---

## 支持哪些 Agent

这个 Skill 是一个带 `SKILL.md`（开放的 Agent Skills 格式）的文件夹，加上 Python / Shell / Remotion 脚本。**本地路线**只要 Agent **能装 Agent Skills**、**能在你电脑上执行命令**；云端路线还需要**能接远程 MCP**（Renoise）。

| Agent | 装 Skill | 本机执行命令 | 接 Renoise MCP（云端路线） | 状态 |
|---|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | ✅ | `/plugin`（见下文） | ✅ 已实测，本地路线就是用它做的 |
| **Codex**（CLI / 桌面） | `~/.codex/skills/` | ✅ | `codex mcp add` | ✅ 预期可用（同一套脚本） |
| **OpenClaw** | 放进 OpenClaw 的技能目录（见其文档） | ✅ | `openclaw plugins install` | ⚙️ 应可用 |
| **WorkBuddy** | 技能 → 导入文件夹 / 压缩包 | ✅ 桌面端 Agent | 连接器 → 添加自定义 MCP | ⚙️ 应可用，菜单名以 App 当前版本为准 |
| **豆包** · **千问办公** · **纳米Work** 等 Agent 产品 | 产品支持 Agent Skills 就导入 | 需要 | 支持自定义 / 远程 MCP 就添加 | ⚙️ 满足上面的能力即可，具体入口以各产品文档为准 |
| **Claude 桌面端 / claude.ai** | 设置里上传技能包 | ⚠️ 只有沙盒 | 连接器 → Add custom connector | 只能做云端路线的写稿、报价、生成；本地路线和剪辑需要能跑命令的 Agent |

---

## 云端路线（Renoise MCP，可选）

原来的云端路线照样能用，每条片子可以和本地路线混着选。

<p align="center"><img src="docs/images/cover.jpg" width="820" alt="一张照片 + 一句话，27 秒直播带货广告"></p>

> 这条 27 秒的直播间广告里，主播不存在。脸、声音、直播间、花字、价格动画，全是 AI 做的。
> 输入只有一句话：「用这个数字人做一条 30 秒直播间广告，卖 WorkBuddy 上手课，10 节课 99 元，原价 999。」
> 总共花了 **482 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) 积分**。

### 云端路线示例（来自原项目）

| | | |
|:---:|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4"><img src="docs/gifs/workbuddy-live-ad.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4"><img src="docs/gifs/renoise-koubo-huazi.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4"><img src="docs/gifs/text-behind.gif" width="300"></a> |
| **直播间带货广告** · 9:16 · 27 秒<br>风格 B + 景深价格 ¥999→¥99<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4) | **产品推荐口播** · 9:16 · 89 秒<br>花字、动态表情、画中画<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4) | **文字在人身后（景深字）** · 5 秒<br>Vision 人像抠图，三层合成<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4) |

| | |
|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4"><img src="docs/gifs/tutorial-ep2.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4"><img src="docs/gifs/tutorial-digital-human-upgrade.gif" width="400"></a> |
| **保姆级教程** · 16:9 · 4 分 36 秒<br>数字人亲自讲「我是怎么被做出来的」（风格 D）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4) | **数字人升级版** · 16:9 · 5 分 55 秒<br>两位主播、六种语言、四个场景、猫狗角色（风格 E）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4) |
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4"><img src="docs/gifs/memt-launch.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4"><img src="docs/gifs/xiaolin-style-explainer.gif" width="400"></a> |
| **发布解读** · 16:9 · 39 秒<br>主播在侧边，右侧代码动效（风格 C）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4) | **财经 / 科技解说** · 16:9 · 2 分 21 秒<br>图表、文件标黄、章节卡（风格 A）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4) |

> 这些主播都是 AI 数字人；男主播是原作者用本人照片做的数字分身。

### 接入 Renoise MCP

先去 **[renoise.ai](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)** 注册账号。登录都在浏览器里完成，不用复制任何 API key。

| Agent | 怎么接 |
|---|---|
| Claude Code | `/plugin marketplace add ArcoCodes/renoise-plugins-official`，再 `/plugin install renoise@renoise-plugins-official` |
| Codex | `codex mcp add renoise --url https://renoise.ai/api/public/mcp`，再 `codex mcp login renoise` |
| OpenClaw | `openclaw plugins install renoise --marketplace ArcoCodes/renoise-plugins-official` |
| Claude 桌面端 / claude.ai | 设置 → 连接器 → **Add custom connector** → 名称 `Renoise`，地址 `https://renoise.ai/api/public/mcp` |
| WorkBuddy、Cursor、Windsurf、Cline、豆包、千问、纳米Work…… | 添加远程 MCP 服务器，地址 `https://renoise.ai/api/public/mcp`（常见配置：`{"mcpServers":{"renoise":{"url":"https://renoise.ai/api/public/mcp"}}}`） |

官方最新装法：**[renoise.ai/plugin](https://renoise.ai/plugin)**。装好后问 Agent 一句「查一下我的 Renoise 余额」，能查到就连上了。

### （可选）小米 MiMo 语音：音色设计 / 声音克隆

云端路线默认用 Grok 自带的声音（口型最准）。想要设计一个新音色、用你自己的克隆声音，或者做纯旁白视频，Skill 会调用 **小米 MiMo TTS**：

1. 去 **[platform.xiaomimimo.com](https://platform.xiaomimimo.com/)** 注册并创建 API Key。写这份文档时小米的 TTS 模型是限时免费的，具体以官网当前价格为准。
2. 把 Key 放进环境变量，或写到 `~/.config/ai-teardown/mimo.env`：
   ```bash
   mkdir -p ~/.config/ai-teardown && cat > ~/.config/ai-teardown/mimo.env <<'EOF'
   MIMO_API_KEY=你的key
   MIMO_BASE_URL=https://api.xiaomimimo.com/v1
   EOF
   chmod 600 ~/.config/ai-teardown/mimo.env
   ```
3. 只克隆**你本人**的声音，或明确授权给你的声音。

> 注意：Grok 的口型跟的是它自己生成的声音。事后换成别的声音，口型会差约 100 毫秒（画中画看不出，全屏特写看得出）。本地路线是照着克隆声音生成嘴型的，没有这个问题。

### 做你自己的数字人（云端路线）

1. 选一张照片：正脸、光线均匀、头发不挡脸、嘴闭着。**只用你本人或明确授权的照片。**
2. 让 Agent 生成四视图（正面、两个侧面、背面）：GPT Image 2.5，2k，约 23 积分（本地可用 Qwen Image 2.1），保证换角度不变脸。
3. 同一张图、同一句台词做多模型对比（Grok Video 1.5 vs Wan 3.0，各 8 秒），选一个。
4. 把参考图上传到 Renoise，把 `material:<id>` 写进 `skills/digital-human-koubo/persona.json`（`renoise.reference_material`；第二位主播写在 `other_hosts.me`）。

详细步骤见 [`references/new-avatar.md`](skills/digital-human-koubo/references/new-avatar.md)。仓库里的 `material:` ID 属于原作者的账号，你的账号用不了，这是正常的。本地路线只要在 `persona.json → comfy.hosts` 里加一个主播（见[本地路线的主播](#本地路线的主播)）。

<p align="center"><img src="docs/images/scene-composite.jpg" width="720" alt="参考照 → 合成直播间"></p>

### 云端成本参考（真实跑过的数）

| 视频 | 生成内容 | 积分 |
|---|---|---|
| 直播间广告 9:16 27 秒 | 1 张场景图 + 5 段 Grok 口播（720p） | **482** |
| 教程第二期 16:9 4 分 36 秒 | 32 段口播（全屏 720p / 画中画 480p）+ 演示素材 | 约 3250 |
| 数字人升级版 16:9 5 分 55 秒 | 30 段新片段 + 7 张场景图，复用 17 段 | 约 3409 |

写文档时的价格：Grok Video 1.5 720p 17 积分/秒、480p 10 积分/秒；GPT Image 2.5 2k 23 积分/张。以 Agent 实时报价为准。

---

## 五种剪辑风格

<p align="center"><img src="docs/images/five-styles.jpg" width="820" alt="五种剪辑风格"></p>

| 风格 | 比例 | 时长 | 适合 | 模板 |
|---|---|---|---|---|
| **A** 小林式解说（财经 / 科技事件） | 16:9 | 3–20 分钟 | 事件、数据、「为什么」 | `templates/lin-169`（plan.json 驱动：景深字、题板+主播小窗、B-roll、公式逐项长出、算例、图表） |
| **B** 网红花字口播 | 9:16 | 30–120 秒 | 安利、带货、种草、吐槽 | `templates/huazi-916`（数据驱动） |
| **C** 发布解读 | 16:9 | 30–90 秒 | 新品、新模型发布 | `templates/reference/launch-169` |
| **D** 保姆级教程 | 16:9 | 3–8 分钟 | 几步做出 XX、工具上手 | `templates/reference/tutorial-169` |
| **E** 多主播 · 多语言 · 多场景 | 16:9 | 3–7 分钟 | 能力展示、出海 | `templates/reference/multihost-169` |

风格 B 有三档花字强度：**克制 / 标准 / 热闹**。

<p align="center"><img src="docs/images/huazi-presets.jpg" width="820" alt="三档花字强度"></p>

风格 A 只学解说频道的**结构和剪辑语法**，不用真实创作者的脸、声音、布景和原话。

### 提示词示例（本地实跑）

五条[本地成片](#本地路线成片示例)每种风格挑了三段，H3 提示词、场景图、B-roll 和配乐提示词都原样收在 **[docs/local-prompts.zh-CN.md](docs/local-prompts.zh-CN.md)**，点风格字母直接跳过去。主播段的提示词由 `comfy_batch.py` 按 `persona.json` 和 `script.json` 自动拼出来，一般不用手写，那份文档也讲了每个字段对应提示词的哪一部分。

| 风格 | 段 · 主播 | 台词 | 看点 |
|---|---|---|---|
| [**A**](docs/local-prompts.zh-CN.md#style-a) | `s01` · `girl` | 存一笔钱，多久能翻一倍？有个特别好用的心算方法。 | 景深字开场，头顶和两侧留背景 |
| [**A**](docs/local-prompts.zh-CN.md#style-a) | `s03` · `girl` | 比如年化百分之六，七十二除以六，等于十二，大约十二年翻一倍。 | 讲解段：点头、低头看屏幕 |
| [**A**](docs/local-prompts.zh-CN.md#style-a) | `s06` · `girl` | 你的钱现在按什么速度在长？评论区聊聊。 | 结尾互动：看镜头、手势 |
| [**B**](docs/local-prompts.zh-CN.md#style-b) | `b1` · `tank` | 一张照片，一台显卡，我做出了五种风格的口播视频。而且，一分钱接口费都没花。 | 竖屏自拍开场钩子 |
| [**B**](docs/local-prompts.zh-CN.md#style-b) | `b5` · `tank` | 最惊艳的是口型：给它一张照片、一段配音，嘴型就自己对上了，不用抽卡。 | vlog 表演：歪头、点头、抬手 |
| [**B**](docs/local-prompts.zh-CN.md#style-b) | `b8` · `tank` | 想要这套流程的，评论区扣一，我把步骤整理给你。 | 结尾要互动 |
| [**C**](docs/local-prompts.zh-CN.md#style-c) | `c1` · `tank` | 文生图、图生视频，你都见过了。但今天这个模型，画面和声音是一起生成的。 | 一句话说清新在哪 |
| [**C**](docs/local-prompts.zh-CN.md#style-c) | `c3` · `tank` | 最实用的是参考生视频：给它一张照片、一段配音，人物的口型就跟着配音走。 | 功能讲解 |
| [**C**](docs/local-prompts.zh-CN.md#style-c) | `c5` · `tank` | 不花一分钱接口费，代价是电费和耐心。你会拿它做什么？评论区告诉我。 | 讲代价 + 抛问题 |
| [**D**](docs/local-prompts.zh-CN.md#style-d) | `d1` · `girl` | 想做数字人口播，又不想花钱买接口？今天三步，在自己电脑上跑通。 | 痛点 + 「今天三步」 |
| [**D**](docs/local-prompts.zh-CN.md#style-d) | `d2` · `girl` | 第一步，克隆声音。录一段十几秒的干声，交给千问的语音模型，再输入新台词，就能配出同一个声音。 | 步骤段（约 10 秒） |
| [**D**](docs/local-prompts.zh-CN.md#style-d) | `d5` · `girl` | 整套流程不花一分接口费。想要完整的命令清单，评论区留言。 | 总结 + 留言领清单 |
| [**E**](docs/local-prompts.zh-CN.md#style-e) | `e2` · `tank` | 第一个坑，分期免息。免的是利息，手续费可一分没少，先算清楚再下单。 | 第二位主播 `tank` 接棒 |
| [**E**](docs/local-prompts.zh-CN.md#style-e) | `e3` · `girl` | 第二个坑，先涨价再打折。加购之前，记下最近三十天的价格，一对比就知道。 | Qwen Image 直播间场景图当参考 |
| [**E**](docs/local-prompts.zh-CN.md#style-e) | `e4` · `tank` | Third trap: don't buy extra stuff just to hit the discount threshold. If you don't need it, it's not a deal. | 中途切英文 |

---

## 48 个包装组件

逐帧拆了 25 支视频（镜头切分、开场逐拍、屏幕文字、声音），完整报告在 [`references/research/`](skills/digital-human-koubo/references/research/)。

<p align="center"><img src="docs/images/creator-pacing.jpg" width="720" alt="25 支头部博主视频每分钟切数"></p>

**从研究里提炼的规则**（[`packaging-playbook.md`](skills/digital-human-koubo/references/packaging-playbook.md)）：
- 切数可以低，刺激不能断：前 30 秒每 3–5 秒要有一个新东西出现。
- 前 3 秒直接给命题或动作，不问好、不放 Logo。
- BGM 从头铺到尾；音效只给事件（中文口播头部每分钟 1–3 个）；揭晓前刻意静音 0.6–1.0 秒。
- 单机位数字人最便宜的节奏来源：按句子边界跳切推近（1.0× / 1.18× / 1.32×）。

<div align="center">
<a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4"><img src="docs/gifs/packaging-gallery.gif" width="560"></a><br>
<b>包装组件图鉴</b> · 48 个组件 · 2 分 40 秒 · <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4">▶ 播放</a>
</div>

<p align="center"><img src="docs/images/packaging-gallery.jpg" width="820" alt="包装组件图鉴"></p>

| 分组 | 组件 |
|---|---|
| 开场 / 钩子 | TeaserColdOpen 预告闪回 · ColdOpenFreeze 定格片名卡 · SearchTyping 搜索框打字 · NumberSpike 数字钉子 · SlamText 砸字 · WordStack 逐词堆叠 · TornStrip 撕纸标题 · **TextBehind 景深字** |
| 证据 / 数据 | EvidenceCard 证据截图 · DocFocus 文档聚焦 · SourceDoc 官方文档 · ZoomFocus 截图聚焦 · Counter 数字滚动 · Odometer 里程表 · GlassPanel 玻璃面板 · SpecCard 参数卡 · LineDraw 折线图 · BarCompare 对比条 · ReviewCards 评论卡 · ArchiveCards 档案卡 · MapRoute 地图航线 · CompareWipe 前后对比 · PaperCollage 纸张拼贴 |
| 标注 / 人物 | HandDraw 手绘圈注 · CalloutPill 指针胶囊 · LeaderLabel 引线标注 · TypedNameTag 打字名牌 · LowerThird 人名条 · NamePlate 名牌语录 · SourceTag 出处角标 · FreezeFrame 定格「等等！」 |
| 节奏 / 互动 | PunchInHost 跳切推近 · KeywordStack 关键词三连 · RetentionCaption 留存大字幕 · TiltLine 倾斜金句 · Aside 括号旁白 · Danmaku 弹幕 · ReactionPop 反应贴纸 · MemeWindow 梗图窗 · PollPop 投票 · GlitchInterstitial 故障插屏 · HostFloaters 悬浮窗 · ProgressChapters 进度条 · ProgressTracker 步骤追踪 · ChapterCard 章节卡 · RecapBoard 复盘板 · Countdown 倒计时 · GhostWord 鬼影大字 |

每个组件都在 `pack` 列表里按名字调用，时间写成「段:词」（如 `"3:积分"`），9:16 自动适配：

```json
"pack": [
  { "use": "NumberSpike", "at": "1:不到十块钱", "until": "1:end", "text": "¥9.9/节", "label": "一节课" },
  { "use": "Danmaku", "items": [{ "t": "真的假的？", "at": "1:" }, { "t": "AI 还能帮我干活？", "at": "1:教你", "hot": true }] },
  { "use": "TextBehind", "src": "main.mp4", "cutout": "main_cut_s4.webm", "cutoutFrom": 17.2, "at": "4:", "until": "4:end",
    "mode": "count", "lines": [{ "t": "¥99", "font": "en", "color": "#FFE14D", "size": 0.17 }], "count": { "from": 999, "to": 99, "prefix": "¥" } }
]
```
参数说明：[`references/packaging.md`](skills/digital-human-koubo/references/packaging.md)。渲染前先检查：`python3 scripts/check_edit.py <工程>/src`。

### 景深字：文字在人身后

<p align="center"><img src="docs/images/text-behind-layers.jpg" width="760" alt="原视频 → 人像遮罩 → 原视频 + 大字 + 人像"></p>

```bash
python3 scripts/cutout_video.py public/main.mp4 public/main_cut_s4.webm --from 17.2 --to 22.4   # 只抠用到的那几秒
```
Linux / Windows 上遮罩来自 ComfyUI 里的 BiRefNet，macOS 上来自 Apple Vision。适合**中景、头顶留白**的画面。自拍特写里人占了约 89% 的画面，字会被挡住，脚本在超过 60% 时会提醒。把这类段落标成 `"shot": "depth"`，生成时就会出中景。

<p align="center"><img src="docs/images/closeup-vs-medium.jpg" width="560" alt="特写 89% 挡字，中景 57% 露字"></p>

---

## 目录结构

```
skills/
  digital-human-koubo/            主 Skill
    SKILL.md                      Agent 照着执行的流程
    persona.json                  主播形象、声音描述、提示词模板
                                  （comfy：本地路线配置、主播的 voice_ref / look / look_person、H3 提示词模板）
    comfy/                        ComfyUI API 流程：tts_clone · h3_r2v_audio · h3_i2v · qwen_t2i · music
    references/                   风格菜单 · 包装组件 · 手法库 · 安装 · 拆解报告
    scripts/                      comfy_batch（本地配音 + H3 对口型）· comfy_scene · comfy_broll · comfy_music
                                  face_center（mediapipe 量脸）· numcn（数字转中文读法，回听比对用）
                                  build_tasks · rangedl · assemble · align · check_edit · cutout_video
                                  voicefx/unify · doctor · new_edit · make_assets
                                  make_cover · cover_first（封面 + 首帧）
                                  lin_scenes · lin_subs · lin_sfx · lin_mix（风格 A 分镜、字幕、音效、混音）
                                  misread_check · patch_words（查念错字、只换错句保口型）
    templates/
      huazi-916/                  9:16 数据驱动花字口播模板（edit.json）
      packaging/                  48 个组件 + 图鉴工程
      lin-169/                    16:9 小林式解说模板（scenes.json 驱动，13 种场景）
      reference/                  launch-169 · tutorial-169 · multihost-169
    assets/                       风格预览图 · 包装图鉴 · 数字人参考图
                                  host_girl_*.png · voice_ref_*.flac（本地路线主播）
  finance-explainer/              纯图表财经长片引擎（episode.json 拍表、检索工具）
workflows/                        本地路线用到的 ComfyUI 工作流（界面格式），附与 API 文件的对照
docs/                             README 用的图片、GIF 预览、封面帧，本地路线提示词示例（local-prompts.zh-CN.md）
```

## 踩过的坑（Skill 里都处理了）

### 本地路线

- 不开 Lightning LoRA，H3 在 0.8MP 下超过 24 GB，卡在第 0 步 → 流程里主播用 4 步、B-roll 用 8 步 LoRA。
- Qwen3-TTS 偶尔会念糊一个词（比如 MiniMax 念成 mini maxax）→ 每句都用 SenseVoice **不带原文**回听；在那段加 `"seed": 新数` 重跑，只重配那一段。
- 单句超过 14 秒会直接报错 → 拆短；H3 单镜头太长质量会掉。
- 用场景图当参考时，`look` 里写的演播室会把背景拉回去（暖白直播间被画成深蓝墙）→ `look_person` 只写人物，段落有 `"ref"` 时自动用它。
- MiniMax Music 3 容易提前收尾（要 60 秒只给 28 秒）→ lyrics 里 `[Instrumental]` 标签越多越长（5 个约 37 秒）；剪辑模板本来就会循环。
- H3 画招牌会出乱码字 → 写 "shop signs are blurred and out of focus"，或者挑没有招牌的画面。
- `~/.bashrc` 里写在「非交互就 return」那行之后的变量，脚本读不到 → earshot 去连 Hugging Face 卡住；`EARSHOT_*` 要写在那行之前。
- whisper / SenseVoice 会把念出来的数字写成阿拉伯数字（七十二 → 72）→ `numcn.py` 比对前两边都转成读法。逐位念法（「三零九零」对 3090）和同音字仍可能被标出来 → 先听再决定重配。

### 两条路线通用 / 云端路线

- 几十段口播直接拼接，声音会一段段累积落后口型（实测 44 段到 4:43 晚 0.38 秒）→ `assemble.py` 拼接前把每段音频补齐到画面长度，并校验音画等长。
- whisper 带原文提示会把念错的字「纠正」回去 → `misread_check.py` 按停顿切句、不带原文转写；念错的用 `patch_words.py` 只换那一句（克隆音拉到原句长度），口型不受影响，不用整片换音色。
- 另配声音轨时，主播视频轨一定要静音；两条声音差几毫秒叠在一起会刺耳（梳状滤波）。
- expo 缓动到不了终点（99.9 四舍五入成 100）→ 计数动画结束时强制落在精确值。
- Grok 横屏口播偶尔**自己烧字幕**，提示词写了也挡不住 → 抽帧检查，重拍那段。
- whisper 会把中文数字写成阿拉伯数字（九百九十九 → 999），准确率会掉，但其实没念错 → 先听再决定重拍。
- Renoise 美国 CDN 并行下载会断成半截 → `rangedl.py` 6 段 Range 续传 + 解码校验。
- Grok 9:16 720p 是 **720×1280**，别拉成别的比例。

## 使用红线

- 只用你本人或**明确授权**的脸和声音，不冒充任何真人或创作者。
- 每条片子标「内容由 AI 数字人演绎」，场景和动物片段标「AI 生成」。
- 不编数字、价格、优惠、评价；画面上的示意数据要标「示意」。
- 不用网络梗图、影视剧截图、明星照片；梗图类组件用你自己数字人生成的原创贴纸。
- 积分（云端路线）只在你确认报价之后才花。

## 许可与第三方

- 代码和文档：[MIT](LICENSE) © 2026 Berryxia（andyhuo520）；本地 ComfyUI 路线 © 2026 walksky。
- 本地路线：[ComfyUI](https://github.com/comfyanonymous/ComfyUI)（GPL-3.0，自行安装）· 模型 MiniMax H3、MiniMax Music 3、Qwen Image 2.1、Qwen3-TTS、SenseVoice、BiRefNet（自行下载，各有各的许可，商用前请看模型页）· [mediapipe](https://github.com/google-ai-edge/mediapipe)（Apache-2.0）· [earshot](https://github.com/Leonxlnx/earshot)（MIT）及其 CLAP、AST 模型。
- 渲染用的 **[Remotion](https://www.remotion.dev/)** 有自己的许可：个人和 3 人以内的公司免费，更大的公司需要购买[公司授权](https://www.remotion.pro/)。
- 动态表情：[Google Noto Emoji Animation](https://googlefonts.github.io/noto-emoji-animation/)（CC BY 4.0），视频里请署名「Animated emoji: Google Noto」。
- 地图：[world-atlas](https://github.com/topojson/world-atlas)（ISC，数据来自 Natural Earth，公有领域）、[d3-geo](https://github.com/d3/d3-geo)、[topojson-client](https://github.com/topojson/topojson-client)（ISC）。涉及中国边界的正式发布内容，请按国内相关规范另行核对。
- 语音识别：[whisper.cpp](https://github.com/ggerganov/whisper.cpp)（MIT）。云端生成走 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)（用你自己的账号和积分）；可选 TTS 用 [小米 MiMo](https://platform.xiaomimimo.com/)。
- WorkBuddy 示例里的课程截图来自原作者自己的课程。示例视频是各自作者的作品，请不要当成自己的作品二次上传。

详见 [THIRD_PARTY.md](THIRD_PARTY.md)。

---

<div align="center">

原作者 **Berryxia**（[andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo)）· 本地 ComfyUI 路线 **walksky** · 用 Claude Code 做的 · 有帮助的话点个 ⭐，让更多人看到。

</div>
