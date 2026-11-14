# Local route: ComfyUI workflows, scripts and architecture

[中文](WORKFLOWS.zh-CN.md) · [Back to README](../README.en.md) · [Install](INSTALL.md) · [Troubleshooting](TROUBLESHOOTING.md)

This is reference material: which script runs at each step, which ComfyUI graph it submits and which model files it needs. You don't need to read it to make a video; one sentence to your agent is enough.

## The local route, step by step

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

## UI-format workflows (`workflows/`)

Drag a file onto the ComfyUI canvas (or *Workflow → Open*) to inspect or run it by hand. Image / audio inputs are set to `example.png` / `example.flac`; load your own. Details and the exact changes for each API version: [`workflows/README.md`](../workflows/README.md).

| Workflow | What it does | API version used by the skill |
|---|---|---|
| [`qwen3_tts_voice_clone.json`](../workflows/qwen3_tts_voice_clone.json) | Qwen3-TTS voice clone from a reference clip + SenseVoice ASR | `comfy/tts_clone.api.json` |
| [`qwen3_tts_voice_design.json`](../workflows/qwen3_tts_voice_design.json) | design a new voice from a text description | — (used once to make the sample voices) |
| [`video_minimax_h3_r2v_3ref.json`](../workflows/video_minimax_h3_r2v_3ref.json) | MiniMax H3 Reference-to-Video, 4-step Lightning LoRA | `comfy/h3_r2v_audio.api.json` (one image + TTS audio as `<Audio 1>`) |
| [`video_minimax_h3_i2v.json`](../workflows/video_minimax_h3_i2v.json) | MiniMax H3 Image-to-Video, 8-step Lightning LoRA | `comfy/h3_i2v.api.json` (text-to-video when no first frame) |
| [`image_qwen_image_2_1_t2i.json`](../workflows/image_qwen_image_2_1_t2i.json) | Qwen Image 2.1 text-to-image, optional prompt enhancer | `comfy/qwen_t2i.api.json` (+ reference images) |
| [`audio_minimax_music_3.json`](../workflows/audio_minimax_music_3.json) | MiniMax Music 3 song / instrumental | `comfy/music.api.json` |
| [`birefnet_remove_background.json`](../workflows/birefnet_remove_background.json) | BiRefNet person / background mask | built inside `scripts/cutout_video.py` (on video, 8 s chunks) |

## API-format graphs the scripts submit (`skills/digital-human-koubo/comfy/`)

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

## Presenters for the local route

`persona.json → comfy.hosts` defines each local presenter: photo (`avatar`), output size, voice sample (`voice_ref` + `voice_ref_text`), English appearance text for the prompt (`look`, plus `look_person` without the studio for use with scene images), voice description and default framing. Two are included: `tank` (the default white-tank-top host, `assets/avatar_ref.jpg`) and `girl` (`assets/host_girl_*.png`). The `girl` images and both voice samples (`assets/voice_ref_*.flac`) are AI-generated, not real people. The H3 prompt template is `comfy.prompt_template` (Ref2VA format: subject_definitions / summary / retention_analysis / detailed_description / soundscape / music).

## GPU time (RTX 3090 24 GB, real runs)

No credits; the cost is GPU time.

| Job | Setting | Time |
|---|---|---|
| Voice clone (Qwen3-TTS) | one 5–14 s line | seconds |
| Presenter segment (H3 Ref2VA) | 10 s, 672×1216 or 1216×672, 4 steps | ~8 min (4–9 min) |
| Scene image (Qwen Image 2.1) | 25 steps | 25–50 s (first one with model loading up to ~5 min) |
| B-roll (H3 T2VA / I2VA) | 5 s, 1216×672, 8 steps | 5–6 min |
| BGM (MiniMax Music 3) | 35–50 s instrumental, 30 steps | 1–2 min |

A ~40-second finished video (5–8 presenter segments) takes roughly 40–70 minutes of GPU time.

## Components by step

Only the **generation** layer differs between the local and the cloud route; scripting, QA, timeline, editing and covers are identical.

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
