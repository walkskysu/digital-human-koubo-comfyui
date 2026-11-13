# ComfyUI workflows · ComfyUI 工作流

The ComfyUI workflows behind the local route, in the normal UI format: drag a file onto the ComfyUI canvas (or *Workflow → Open*) to inspect or run it by hand. Image / audio inputs are set to `example.png` / `example.flac`; load your own.

The skill itself does not read this folder. Its scripts submit the flattened **API-format** versions in [`skills/digital-human-koubo/comfy/`](../skills/digital-human-koubo/comfy/) (those can be dragged into ComfyUI too). The table shows which API file came from which workflow and what was changed.

本地路线用到的 ComfyUI 工作流（界面格式）：把文件拖进 ComfyUI 画布（或「工作流 → 打开」）就能看、能手动跑。图片 / 音频输入都换成了 `example.png` / `example.flac`，用时换成你自己的。Skill 本身不读这个目录，脚本提交的是 [`skills/digital-human-koubo/comfy/`](../skills/digital-human-koubo/comfy/) 里展平后的 API 格式版本（也能直接拖进 ComfyUI）。

| Workflow (UI) | What it does · 用途 | API version used by the skill | Changes in the API version · 改动 |
|---|---|---|---|
| `qwen3_tts_voice_clone.json` | Qwen3-TTS voice clone from a reference clip, plus SenseVoice ASR · 声音克隆 + 回听 | `comfy/tts_clone.api.json` (`comfy_batch.py --stage tts`) | Clone path only; the ASR node is submitted separately by `comfy_batch.py` after each line · 只留克隆；回听节点由脚本单独提交 |
| `qwen3_tts_voice_design.json` | Design a new voice from a text description · 用文字描述设计音色 | — (one-off) | Used once to make `assets/voice_ref_*.flac`; not called by scripts · 只用来做示例声音样本 |
| `video_minimax_h3_r2v_3ref.json` | MiniMax H3 Reference-to-Video, 4-step Lightning LoRA · 参考生视频 | `comfy/h3_r2v_audio.api.json` (`comfy_batch.py --stage video`) | One reference image + a `LoadAudio` as `<Audio 1>` (fully_copy → lip sync); size, length, seed and prompt filled per segment · 1 张参考图 + 配音当参考音频，口型跟配音走 |
| `video_minimax_h3_i2v.json` | MiniMax H3 Image-to-Video, 8-step Lightning LoRA · 图生视频 | `comfy/h3_i2v.api.json` (`comfy_broll.py`) | Resolution selector removed (size set by script); without a first frame the `LoadImage` is dropped → text-to-video · 去掉分辨率选择；没首帧时变文生视频 |
| `image_qwen_image_2_1_t2i.json` | Qwen Image 2.1 text-to-image with optional prompt enhancer · 文生图（可选提示词增强） | `comfy/qwen_t2i.api.json` (`comfy_scene.py`) | Resolution selector removed; with `refs` the script connects reference images + VAE to `TextEncodeQwenImage21`; enhancer branch removed unless `--enhance` · 有参考图时脚本接上参考图和 VAE；不开增强就拿掉增强分支 |
| `audio_minimax_music_3.json` | MiniMax Music 3 song / instrumental · 配乐 | `comfy/music.api.json` (`comfy_music.py`) | Subgraph flattened; caption, lyrics (`[Instrumental]` tags), seed, length filled by script; output flac → mp3 · 展平；脚本填风格、歌词标签、种子、时长 |
| `birefnet_remove_background.json` | BiRefNet person / background mask on one image · 单张去背景 | built inside `scripts/cutout_video.py` | Same nodes on video: `LoadVideo` → `RemoveBackground` → `MaskToImage` → `SaveVideo`, in 8 s chunks · 同样节点换成视频输入，按 8 秒分块 |

Models, node packs and where to put the files: see [Local ComfyUI setup](../README.md#install-local-comfyui-route) / [本地 ComfyUI 安装](../README.zh-CN.md#安装本地-comfyui-路线). Most of these started from ComfyUI's built-in templates (*Browse Templates*); the Qwen3-TTS ones come with the Qwen3-TTS node pack.
