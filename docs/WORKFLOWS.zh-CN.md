# 本地路线：ComfyUI 工作流、脚本与架构

[English](WORKFLOWS.md) · [返回 README](../README.md) · [安装](INSTALL.zh-CN.md) · [排错](TROUBLESHOOTING.zh-CN.md)

这份是查阅用的参考：每一步跑哪个脚本、提交哪张 ComfyUI 图、用到哪些模型文件。只想出片的话不用读，跟 Agent 说一句话就行。

## 本地路线逐步说明

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

## 界面格式工作流（`workflows/`）

把文件拖进 ComfyUI 画布（或「工作流 → 打开」）就能看、能手动跑。图片 / 音频输入都换成了 `example.png` / `example.flac`，用时换成你自己的。每个 API 版本具体改了什么，见 [`workflows/README.md`](../workflows/README.md)。

| 工作流 | 用途 | Skill 实际提交的 API 版本 |
|---|---|---|
| [`qwen3_tts_voice_clone.json`](../workflows/qwen3_tts_voice_clone.json) | Qwen3-TTS 声音克隆 + SenseVoice 回听 | `comfy/tts_clone.api.json` |
| [`qwen3_tts_voice_design.json`](../workflows/qwen3_tts_voice_design.json) | 用文字描述设计新音色 | —（只用来做示例声音样本） |
| [`video_minimax_h3_r2v_3ref.json`](../workflows/video_minimax_h3_r2v_3ref.json) | MiniMax H3 参考生视频，4 步 Lightning LoRA | `comfy/h3_r2v_audio.api.json`（1 张参考图 + 配音当 `<Audio 1>`） |
| [`video_minimax_h3_i2v.json`](../workflows/video_minimax_h3_i2v.json) | MiniMax H3 图生视频，8 步 Lightning LoRA | `comfy/h3_i2v.api.json`（没首帧时变文生视频） |
| [`image_qwen_image_2_1_t2i.json`](../workflows/image_qwen_image_2_1_t2i.json) | Qwen Image 2.1 文生图，可选提示词增强 | `comfy/qwen_t2i.api.json`（可接参考图） |
| [`audio_minimax_music_3.json`](../workflows/audio_minimax_music_3.json) | MiniMax Music 3 歌曲 / 纯音乐 | `comfy/music.api.json` |
| [`birefnet_remove_background.json`](../workflows/birefnet_remove_background.json) | BiRefNet 人像 / 背景遮罩 | `scripts/cutout_video.py` 里拼（视频输入，按 8 秒分块） |

## 脚本提交的 API 格式图（`skills/digital-human-koubo/comfy/`）

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

## 本地路线的主播

`persona.json → comfy.hosts` 定义每个本地主播：照片（`avatar`）、输出尺寸、声音样本（`voice_ref` + `voice_ref_text`）、给提示词用的英文外形描述（`look`；另有只写人物、不写布景的 `look_person`，配场景图时用）、声音描述、默认构图。自带两个：`annie`（默认主播，演播室中景，`assets/host_annie_*.png`；默认出 16:9，给 `comfy_batch.py` 加 `--ratio 9:16` 时换用竖屏形象图 `host_annie_vertical.png`）和 `ella`（9:16 自拍特写的白背心主播，`assets/avatar_ref.jpg`）。段落里不写 `host` 时用 `annie`。`annie` 的形象图和两个声音样本（`assets/voice_ref_*.flac`）都是 AI 生成的，不是真人。H3 提示词模板在 `comfy.prompt_template`（Ref2VA 格式：subject_definitions / summary / retention_analysis / detailed_description / soundscape / music）。

## GPU 用时（RTX 3090 24 GB，实测）

不花积分，花的是 GPU 时间。

| 任务 | 设置 | 用时 |
|---|---|---|
| 克隆配音（Qwen3-TTS） | 一句 5–14 秒 | 几秒 |
| 主播一段（H3 Ref2VA） | 10 秒，672×1216 或 1216×672，4 步 | 约 8 分钟（4–9 分钟） |
| 场景图（Qwen Image 2.1） | 25 步 | 25–50 秒（第一张含加载最多约 5 分钟） |
| B-roll（H3 T2VA / I2VA） | 5 秒，1216×672，8 步 | 5–6 分钟 |
| 配乐（MiniMax Music 3） | 35–50 秒纯音乐，30 步 | 1–2 分钟 |

一条 40 秒左右的成片（5–8 段口播）约占 40–70 分钟 GPU 时间。

## 每一步用到的组件

本地和云端两条路线只差在**生成**这一层；写稿、质检、时间轴、剪辑、封面完全一样。

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
                                  host_annie_*.png · voice_ref_*.flac（本地路线主播）
  finance-explainer/              纯图表财经长片引擎（episode.json 拍表、检索工具）
workflows/                        本地路线用到的 ComfyUI 工作流（界面格式），附与 API 文件的对照
docs/                             安装说明（INSTALL.zh-CN.md）、README 用的图片、GIF 预览、封面帧
```
