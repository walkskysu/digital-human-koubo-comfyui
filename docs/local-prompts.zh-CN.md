# 本地路线提示词示例

这里收的是 [README 里五条成片](../README.zh-CN.md#本地路线成片示例) 真正跑过的提示词，原样照录，没有改写。每种风格挑三段，再附上同一条片子用到的场景图、B-roll 和配乐提示词。

## 提示词是怎么来的

主播段落的 H3 提示词不用手写。`scripts/comfy_batch.py` 读 `script.json` 的每一段，套进 `persona.json → comfy.hosts.<主播>` 的字段，拼成 MiniMax H3 Ref2VA 的格式：

| 提示词里的位置 | 来自哪里 |
|---|---|
| `subject_definitions` 的人物描述 | 主播的 `who` + `look`（段落用场景图当参考时换成 `look_person`） |
| `<Audio 1>` 的声音描述 | 主播的 `voice`，语言跟着段落的 `lang` |
| `[Shot 1]` 的构图 | 主播的 `shot_desc`（用场景图时改成「照参考图构图」） |
| `<d>[Chinese] ...</d>` 台词 | 段落的 `t`，和 Qwen3-TTS 配音一字不差 |
| `summary` 里「在讲什么」 | 段落的 `purpose`，没写就用命令行 `--purpose` |
| `While talking:` 表演提示 | `persona.json → acts`，按段落的 `shot` 选（`full` / `pip` / `vlog` / `depth` 各一句） |
| 运镜 | 主播的 `camera` |

`<Audio 1>` 是这段的 TTS 配音，标成 `fully_copy`，H3 就照着它对口型。所以想改效果，一般改 `persona.json` 里主播的字段和 `script.json` 的台词，不用逐段改提示词。下面每段都标了 `script.json` 里的 `shot`（剪辑时的版式）和 `host`。

配乐提示词末尾的 `sec=… seed=… steps=…` 是生成参数的记录，不是提示词的一部分。

**目录：**

- [风格 A · 小林式解说](#style-a)
- [风格 B · 网红花字口播](#style-b)
- [风格 C · 发布解读](#style-c)
- [风格 D · 保姆级教程](#style-d)
- [风格 E · 双主播接力](#style-e)

---

<a id="style-a"></a>

## 风格 A · 小林式解说

**片子：** 「72 法则」财经解说，主播 `girl`，16:9 · [▶ 看成片](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4) · 项目目录 `lin_test/`（下面的文件路径都相对这里，主播段的提示词存在 `gen/prompts/`）

### 1. 段 `s01` · 景深字 · 主播 `girl`

> 台词：存一笔钱，多久能翻一倍？有个特别好用的心算方法。

开场用景深字（`depth`）：表演提示要求头顶和两侧留出背景，好把大字放在人身后。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top, standing in a calm knowledge-explainer studio with a dark blue-gray wall, softly blurred bookshelf and plants, soft frontal lighting.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, explaining a personal-finance idea calmly and clearly, like a friendly knowledge vlogger, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A locked-off medium shot of <Subject 1> standing at the center of the studio, framed from the waist up exactly as in <Picture 1>, with generous headroom and background visible on both sides. She looks straight into the lens with calm, friendly eye contact. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 存一笔钱，多久能翻一倍？有个特别好用的心算方法。</d> While talking: Medium shot with generous headroom and plain background visible on both sides of the head and shoulders (for text-behind-subject graphics), calm confident delivery. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 2. 段 `s03` · 题板 + 主播小窗 · 主播 `girl`

> 台词：比如年化百分之六，七十二除以六，等于十二，大约十二年翻一倍。

算例段（`pip`）：讲解语气，点头，偶尔低头看屏幕。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top, standing in a calm knowledge-explainer studio with a dark blue-gray wall, softly blurred bookshelf and plants, soft frontal lighting.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, explaining a personal-finance idea calmly and clearly, like a friendly knowledge vlogger, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A locked-off medium shot of <Subject 1> standing at the center of the studio, framed from the waist up exactly as in <Picture 1>, with generous headroom and background visible on both sides. She looks straight into the lens with calm, friendly eye contact. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 比如年化百分之六，七十二除以六，等于十二，大约十二年翻一倍。</d> While talking: Calm explaining tone, small nods, occasionally glancing down as if reading a screen, small pointing gestures. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 3. 段 `s06` · 主播全屏 · 主播 `girl`

> 台词：你的钱现在按什么速度在长？评论区聊聊。

结尾互动（`full`）：看镜头，表情和手势更多。`summary` 里的「personal-finance idea」来自这条片子的 `--purpose`。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top, standing in a calm knowledge-explainer studio with a dark blue-gray wall, softly blurred bookshelf and plants, soft frontal lighting.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, explaining a personal-finance idea calmly and clearly, like a friendly knowledge vlogger, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A locked-off medium shot of <Subject 1> standing at the center of the studio, framed from the waist up exactly as in <Picture 1>, with generous headroom and background visible on both sides. She looks straight into the lens with calm, friendly eye contact. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 你的钱现在按什么速度在长？评论区聊聊。</d> While talking: Warm eye contact, expressive face, natural hand gestures. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 同一条片子的其他提示词

**Qwen Image 2.1 场景图：把定妆照放进演播室（scenes.json）** · `lin_test/scenes.json`

```text
Picture 1 中的年轻女生站在一间简洁的知识讲解演播室里，正面对着镜头，中景构图（腰部以上），人物在画面正中，头顶上方和左右两侧都留出大片背景。同一张脸、同样的齐刘海黑色长直发、同样的米白色罗纹背心。背景是深蓝灰色的墙面，带柔和的渐变光和轻微虚化的书架与绿植，柔和的正面柔光，干净专业的知识类视频质感。画面里不要出现任何文字、字幕或标志。
```

**H3 B-roll（T2VA，8 步）** · `lin_test/broll/prompts/B01.txt`

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic documentary B-roll, close-up of a young Chinese woman's hands at a wooden desk at home, tapping a calculator next to a small stack of red 100-yuan banknotes, a ceramic coffee mug and a plain notebook, warm late-afternoon window light. The camera pushes in with small amplitude at slow speed toward the calculator and banknotes. Natural color grading, shallow depth of field, a single continuous shot with no cuts. No readable text, no logos, no watermarks, no subtitles, no on-screen captions.

overall_soundscape: Soft calculator key taps and quiet room tone.

non_diegetic_music: None.
```

**Music 3 配乐** · `lin_test/edit/public/music/bgm.prompt.txt`

```text
caption:
Global Metadata: Light corporate lo-fi / soft pop instrumental, 92 BPM, C major. Warm, optimistic, calm and focused, like a friendly explainer video about personal finance. Steady energy from start to end with no big drops or build-ups, clean modern mix, leaves plenty of space in the mid range for a spoken voice-over.

Vocal Details: Pure instrumental, no vocals, no humming, no vocal chops, no spoken words.

Arrangement: Soft electric piano chords as the bed, gentle plucked synth and muted guitar playing a light repeating motif, round warm bass, tight soft kick and light finger-snap backbeat with shaker. Intro: piano alone for two bars then the beat comes in. Main body: the same groove loops evenly with small melodic variations, never busy. Outro: elements drop out and the piano ends on a soft resolved chord.

lyrics:
[Intro]

[Instrumental]

[Instrumental]

[Outro]

sec=60.0 seed=7 steps=30
```

---

<a id="style-b"></a>

## 风格 B · 网红花字口播

**片子：** 「一张照片做出五种口播」，主播 `tank`，9:16 · [▶ 看成片](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4) · 项目目录 `b_huazi/`（下面的文件路径都相对这里，主播段的提示词存在 `gen/prompts/`）

### 1. 段 `b1` · 主播全屏 · 主播 `tank`

> 台词：一张照片，一台显卡，我做出了五种风格的口播视频。而且，一分钱接口费都没花。

开场钩子：竖屏自拍特写，手机轻微手持晃动。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 一张照片，一台显卡，我做出了五种风格的口播视频。而且，一分钱接口费都没花。</d> While talking: Warm eye contact, expressive face, natural hand gestures. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 2. 段 `b5` · 自拍 vlog · 主播 `tank`

> 台词：最惊艳的是口型：给它一张照片、一段配音，嘴型就自己对上了，不用抽卡。

vlog 段（`vlog`）：「分享心头好」的轻松表演，歪头、点头、抬手。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 最惊艳的是口型：给它一张照片、一段配音，嘴型就自己对上了，不用抽卡。</d> While talking: Relaxed lifestyle vlogger sharing a favorite tool, natural small head tilts and nods, one hand comes up briefly in a casual gesture. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 3. 段 `b8` · 主播全屏 · 主播 `tank`

> 台词：想要这套流程的，评论区扣一，我把步骤整理给你。

结尾要互动（评论区扣一）。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 想要这套流程的，评论区扣一，我把步骤整理给你。</d> While talking: Warm eye contact, expressive face, natural hand gestures. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 同一条片子的其他提示词

**Music 3 配乐** · `b_huazi/edit/public/music/bgm.prompt.txt`

```text
caption:
Global Metadata: Trendy upbeat social-media vlog pop instrumental, 124 BPM, E major. Bright, confident and fun, like a viral short-video product recommendation, punchy energy that stays light under a fast spoken voice-over. Clean, modern, loud-but-not-busy mix.

Vocal Details: Pure instrumental, no vocals, no humming, no vocal chops, no spoken words.

Arrangement: Bouncy plucked synth hook, snappy kick and claps with crisp hi-hats, groovy synth bass, short brass stabs and playful percussion fills. Intro: the pluck hook alone, then the beat drops in. Main body: steady catchy groove looping with small variations, leaving the mid range clear. Outro: elements cut out, ending on a final stab.

lyrics:
[Intro]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Outro]

sec=60.0 seed=21 steps=30
```

---

<a id="style-c"></a>

## 风格 C · 发布解读

**片子：** 「MiniMax H3：画面和声音一起出」，主播 `tank`，16:9（主播在侧边） · [▶ 看成片](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4) · 项目目录 `c_launch/`（下面的文件路径都相对这里，主播段的提示词存在 `gen/prompts/`）

### 1. 段 `c1` · 主播全屏 · 主播 `tank`

> 台词：文生图、图生视频，你都见过了。但今天这个模型，画面和声音是一起生成的。

开场：一句话说清这次发布新在哪。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 文生图、图生视频，你都见过了。但今天这个模型，画面和声音是一起生成的。</d> While talking: Warm eye contact, expressive face, natural hand gestures. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 2. 段 `c3` · 题板 + 主播小窗 · 主播 `tank`

> 台词：最实用的是参考生视频：给它一张照片、一段配音，人物的口型就跟着配音走。

功能讲解段（`pip`）：讲解语气，偶尔看屏幕、小幅指点。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 最实用的是参考生视频：给它一张照片、一段配音，人物的口型就跟着配音走。</d> While talking: Calm explaining tone, small nods, occasionally glancing down as if reading a screen, small pointing gestures. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 3. 段 `c5` · 主播全屏 · 主播 `tank`

> 台词：不花一分钱接口费，代价是电费和耐心。你会拿它做什么？评论区告诉我。

结尾：讲代价，再抛问题给观众。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 不花一分钱接口费，代价是电费和耐心。你会拿它做什么？评论区告诉我。</d> While talking: Warm eye contact, expressive face, natural hand gestures. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 同一条片子的其他提示词

**Music 3 配乐** · `c_launch/edit/public/music/bgm.prompt.txt`

```text
caption:
Global Metadata: Modern tech product launch instrumental, electronic future-pop, 118 BPM, A minor. Sleek, confident and forward-looking, like a keynote reveal of a new AI model, with a steady pulse that leaves room for a spoken voice-over. Clean, polished, wide stereo mix.

Vocal Details: Pure instrumental, no vocals, no humming, no vocal chops, no spoken words.

Arrangement: Pulsing arpeggiated synth bass, crisp electronic kick and claps, shimmering pads and a bright plucked synth motif, subtle risers between sections. Intro: filtered arpeggio and pads, then the beat drops in. Main body: steady driving groove with the pluck motif repeating, small variations, never busy. Outro: elements fall away to a final airy pad chord.

lyrics:
[Intro]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Outro]

sec=60.0 seed=11 steps=30
```

---

<a id="style-d"></a>

## 风格 D · 保姆级教程

**片子：** 「三步做出本地数字人口播」，主播 `girl`，16:9 · [▶ 看成片](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4) · 项目目录 `d_tutorial/`（下面的文件路径都相对这里，主播段的提示词存在 `gen/prompts/`）

### 1. 段 `d1` · 主播全屏 · 主播 `girl`

> 台词：想做数字人口播，又不想花钱买接口？今天三步，在自己电脑上跑通。

开场：痛点 + 承诺「今天三步」。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top, standing in a calm knowledge-explainer studio with a dark blue-gray wall, softly blurred bookshelf and plants, soft frontal lighting.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A locked-off medium shot of <Subject 1> standing at the center of the studio, framed from the waist up exactly as in <Picture 1>, with generous headroom and background visible on both sides. She looks straight into the lens with calm, friendly eye contact. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 想做数字人口播，又不想花钱买接口？今天三步，在自己电脑上跑通。</d> While talking: Warm eye contact, expressive face, natural hand gestures. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 2. 段 `d2` · 题板 + 主播小窗 · 主播 `girl`

> 台词：第一步，克隆声音。录一段十几秒的干声，交给千问的语音模型，再输入新台词，就能配出同一个声音。

步骤段（`pip`，配终端 / 时间线画面）：最长的一段，约 10 秒。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top, standing in a calm knowledge-explainer studio with a dark blue-gray wall, softly blurred bookshelf and plants, soft frontal lighting.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A locked-off medium shot of <Subject 1> standing at the center of the studio, framed from the waist up exactly as in <Picture 1>, with generous headroom and background visible on both sides. She looks straight into the lens with calm, friendly eye contact. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 第一步，克隆声音。录一段十几秒的干声，交给千问的语音模型，再输入新台词，就能配出同一个声音。</d> While talking: Calm explaining tone, small nods, occasionally glancing down as if reading a screen, small pointing gestures. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 3. 段 `d5` · 主播全屏 · 主播 `girl`

> 台词：整套流程不花一分接口费。想要完整的命令清单，评论区留言。

结尾：总结 + 留言领清单。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top, standing in a calm knowledge-explainer studio with a dark blue-gray wall, softly blurred bookshelf and plants, soft frontal lighting.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A locked-off medium shot of <Subject 1> standing at the center of the studio, framed from the waist up exactly as in <Picture 1>, with generous headroom and background visible on both sides. She looks straight into the lens with calm, friendly eye contact. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 整套流程不花一分接口费。想要完整的命令清单，评论区留言。</d> While talking: Warm eye contact, expressive face, natural hand gestures. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 同一条片子的其他提示词

**Music 3 配乐** · `d_tutorial/edit/public/music/bgm.prompt.txt`

```text
caption:
Global Metadata: Light, friendly lo-fi tutorial background music, 88 BPM, F major. Relaxed, focused and encouraging, like a step-by-step how-to video, steady energy with no big changes, soft warm mix that sits under a spoken voice.

Vocal Details: Pure instrumental, no vocals, no humming, no vocal chops, no spoken words.

Arrangement: Soft electric piano chords, gentle muted guitar plucks, warm round bass, soft boom-bap kick and brushed snare with light shaker, a little vinyl warmth. Intro: piano alone for two bars, then the beat. Main body: the same mellow groove loops evenly. Outro: instruments drop out and the piano ends on a resolved chord.

lyrics:
[Intro]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Outro]

sec=60.0 seed=12 steps=30
```

---

<a id="style-e"></a>

## 风格 E · 双主播接力

**片子：** 「双 11 先别急着付款：3 个坑」，主播 `girl` + `tank`，16:9 · [▶ 看成片](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4) · 项目目录 `e_relay/`（下面的文件路径都相对这里，主播段的提示词存在 `gen/prompts/`）

### 1. 段 `e2` · 自拍 vlog · 主播 `tank`

> 台词：第一个坑，分期免息。免的是利息，手续费可一分没少，先算清楚再下单。

第二位主播 `tank` 接棒：换成她的定妆照、声音和自拍 vlog 构图。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 第一个坑，分期免息。免的是利息，手续费可一分没少，先算清楚再下单。</d> While talking: Relaxed lifestyle vlogger sharing a favorite tool, natural small head tilts and nods, one hand comes up briefly in a casual gesture. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 2. 段 `e3` · 主播全屏 · 主播 `girl`

> 台词：第二个坑，先涨价再打折。加购之前，记下最近三十天的价格，一对比就知道。

用场景图当参考（段落写了 `"ref": "scene/live.png"`）：人物描述换成 `look_person`，构图和布景都照参考图。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long straight black hair with full bangs, a cream-white ribbed tank top.
<Audio 1> is the complete spoken Mandarin Chinese vocal track of <Subject 1> (S1), a gentle, clear, intellectual young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous locked-off medium talking-head shot of <Subject 1> speaking straight into the camera, hosting a shopping livestream, explaining a money-saving tip to viewers, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A shot of <Subject 1> framed exactly as in <Picture 1>, in the same environment, background, lighting and outfit as <Picture 1>. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks Mandarin Chinese with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[Chinese] 第二个坑，先涨价再打折。加购之前，记下最近三十天的价格，一对比就知道。</d> While talking: Warm eye contact, expressive face, natural hand gestures. Locked-off camera on a tripod, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 3. 段 `e4` · 自拍 vlog · 主播 `tank`

> 台词：Third trap: don't buy extra stuff just to hit the discount threshold. If you don't need it, it's not a deal.

中途切英文：台词标签换成 `<d>[English] ...</d>`，配音也用英文生成。

```text
subject_definitions:
<Subject 1> is the young East Asian woman in <Picture 1>: long black hair with loose strands framing her face, pink lips, a small mole on her chest, a white ribbed tank top, close selfie framing under warm natural indoor light against a plain dark ceiling.
<Audio 1> is the complete spoken English vocal track of <Subject 1> (S1), a clear, lively young female voice.

summary:
[reference generation + audio reuse] The target video is a single continuous vertical handheld selfie talking-head shot of <Subject 1> speaking straight into the camera, like a friendly Chinese tech vlogger explaining clearly, with lip movements precisely synchronized to <Audio 1>, which is reused as the complete final audio track.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - face, hairstyle, outfit, framing and lighting stay identical to <Picture 1>.
<Audio 1>: fully_copy - <Audio 1> is reused 1:1 as the target video's complete final audio track, and every syllable drives the matching mouth shape of <Subject 1>.

detailed_description:
[Shot 1] A vertical handheld selfie close-up of <Subject 1>, framed from the top of her head to her chest exactly as in <Picture 1>, warm sunlight across her face, plain dark ceiling behind her. She looks straight into the lens with warm eye contact and a relaxed, friendly smile. <Subject 1> (S1) speaks English with lips, jaw and tongue clearly lip-synced to every syllable of <Audio 1>: <d>[English] Third trap: don't buy extra stuff just to hit the discount threshold. If you don't need it, it's not a deal.</d> While talking: Relaxed lifestyle vlogger sharing a favorite tool, natural small head tilts and nods, one hand comes up briefly in a casual gesture. The phone camera has only a very slight natural handheld sway, no zoom, no cuts. During any silent pause in <Audio 1> her lips rest gently closed. After the last word she closes her lips into a soft smile and holds eye contact until the final frame. No subtitles, no captions, no on-screen text.

overall_soundscape: Only <Audio 1> is heard, with quiet indoor room tone underneath; no added sound effects.

non_diegetic_music: None.
```

### 同一条片子的其他提示词

**Qwen Image 2.1 场景图：直播间（scenes.json）** · `e_relay/scenes.json`

```text
Picture 1 中的女生站在一间明亮温馨的电商直播间里，正对镜头，从腰部以上的中景，头顶留出背景空间。同样的脸、同样的齐刘海黑长直发、同样的米白色罗纹背心。她身后是暖色灯光照亮的货架，摆着包装好的礼盒和日用品，旁边有一个环形补光灯和一个绿植，背景轻微虚化。横屏构图，人物在画面正中间，左右两侧都能看到背景。画面里不要任何文字、标志、价格牌或字幕。
```

**Music 3 配乐** · `e_relay/edit/public/music/bgm.prompt.txt`

```text
caption:
Global Metadata: Upbeat festive shopping-season pop instrumental, 120 BPM, D major. Bright, cheerful and playful, like a lively online shopping festival promo, energetic but light so a spoken voice stays clear. Punchy, clean modern mix.

Vocal Details: Pure instrumental, no vocals, no humming, no vocal chops, no spoken words.

Arrangement: Bouncy plucked synths and marimba motif, tight four-on-the-floor kick with hand claps, funky muted guitar, round synth bass, sparkly bell accents. Intro: marimba motif alone, then the beat comes in. Main body: steady bouncy groove repeating with small variations. Outro: elements drop out, ending on a bright bell hit.

lyrics:
[Intro]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Instrumental]

[Outro]

sec=60.0 seed=13 steps=30
```

---

## 自己写的时候

- 主播段落让 `comfy_batch.py` 生成就好，先跑 `--stage tts` 听配音，再跑 `--stage video`。它会把每段提示词存进 `gen/prompts/`，出问题时先看这里。
- 手写 H3 提示词时按 `h3-prompt-writing` Skill 的 Ref2VA 格式：`subject_definitions / summary / retention_analysis / detailed_description`，再加 `overall_soundscape` 和 `non_diegetic_music`。
- 台词要和配音逐字一致，口型才准。数字写成汉字（「七十二」而不是「72」），TTS 读得更稳。
- 配音停顿时写明「lips rest gently closed」，结尾写「closes her lips into a soft smile」，可以避免收尾时嘴还在动。
- 结尾都带 `No subtitles, no captions, no on-screen text.`，字幕和花字统一在 Remotion 里加。
