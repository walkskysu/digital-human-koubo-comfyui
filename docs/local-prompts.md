# Local-route prompt examples

These are the prompts the [five demo videos in the README](../README.md#local-demos) actually ran with, copied verbatim. Three segments per style, plus the scene, B-roll and music prompts the same video used.

## Where the prompts come from

You don't write the H3 prompts for presenter segments by hand. `scripts/comfy_batch.py` reads each segment of `script.json`, fills in the fields from `persona.json → comfy.hosts.<host>`, and assembles a MiniMax H3 Ref2VA prompt:

| Part of the prompt | Comes from |
|---|---|
| Person in `subject_definitions` | the host's `who` + `look` (`look_person` when the segment uses a scene image as reference) |
| Voice description of `<Audio 1>` | the host's `voice`; the language follows the segment's `lang` |
| Framing in `[Shot 1]` | the host's `shot_desc` ("framed exactly as the reference" when a scene image is used) |
| The `<d>[Chinese] ...</d>` line | the segment's `t`, identical to the Qwen3-TTS voice-over |
| What the `summary` says she is doing | the segment's `purpose`, or `--purpose` on the command line |
| `While talking:` acting cue | `persona.json → acts`, picked by the segment's `shot` (one line each for `full` / `pip` / `vlog` / `depth`) |
| Camera | the host's `camera` |

`<Audio 1>` is the segment's TTS clip, marked `fully_copy`, so H3 lip-syncs to it. To change the result you usually edit the host fields in `persona.json` and the lines in `script.json`, not each prompt. Each segment below lists its `shot` (the edit layout in `script.json`) and `host`.

The `sec=… seed=… steps=…` line at the end of the music prompts records the generation settings; it is not part of the prompt.

**Contents:**

- [Style A · Explainer](#style-a)
- [Style B · Caption-heavy vlog](#style-b)
- [Style C · Launch breakdown](#style-c)
- [Style D · Step-by-step tutorial](#style-d)
- [Style E · Two-host relay](#style-e)

---

<a id="style-a"></a>

## Style A · Explainer

**Video:** "The rule of 72" finance explainer, host `girl`, 16:9 · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-a-72-rule.mp4) · project folder `lin_test/` (file paths below are relative to it; presenter prompts are saved in `gen/prompts/`)

### 1. Segment `s01` · text behind presenter · host `girl`

> Line: 存一笔钱，多久能翻一倍？有个特别好用的心算方法。

Opening with text behind the presenter (`depth`): the acting cue asks for headroom and background on both sides so the big title can sit behind her.

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

### 2. Segment `s03` · board + presenter window · host `girl`

> Line: 比如年化百分之六，七十二除以六，等于十二，大约十二年翻一倍。

Worked-example segment (`pip`): explaining tone, nods, the odd glance down at a screen.

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

### 3. Segment `s06` · presenter full frame · host `girl`

> Line: 你的钱现在按什么速度在长？评论区聊聊。

Closing call to comment (`full`): eye contact, more expression and gestures. The 'personal-finance idea' in `summary` comes from this video's `--purpose`.

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

### Other prompts from the same video

**Qwen Image 2.1 scene: put the master photo into a studio (scenes.json)** · `lin_test/scenes.json`

```text
Picture 1 中的年轻女生站在一间简洁的知识讲解演播室里，正面对着镜头，中景构图（腰部以上），人物在画面正中，头顶上方和左右两侧都留出大片背景。同一张脸、同样的齐刘海黑色长直发、同样的米白色罗纹背心。背景是深蓝灰色的墙面，带柔和的渐变光和轻微虚化的书架与绿植，柔和的正面柔光，干净专业的知识类视频质感。画面里不要出现任何文字、字幕或标志。
```

**H3 B-roll (T2VA, 8 steps)** · `lin_test/broll/prompts/B01.txt`

```text
integrated_multimodal_description: [Shot 1] Live-action, cinematic documentary B-roll, close-up of a young Chinese woman's hands at a wooden desk at home, tapping a calculator next to a small stack of red 100-yuan banknotes, a ceramic coffee mug and a plain notebook, warm late-afternoon window light. The camera pushes in with small amplitude at slow speed toward the calculator and banknotes. Natural color grading, shallow depth of field, a single continuous shot with no cuts. No readable text, no logos, no watermarks, no subtitles, no on-screen captions.

overall_soundscape: Soft calculator key taps and quiet room tone.

non_diegetic_music: None.
```

**Music 3 background music** · `lin_test/edit/public/music/bgm.prompt.txt`

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

## Style B · Caption-heavy vlog

**Video:** "Five talking-head styles from one photo", host `tank`, 9:16 · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-b-five-styles.mp4) · project folder `b_huazi/` (file paths below are relative to it; presenter prompts are saved in `gen/prompts/`)

### 1. Segment `b1` · presenter full frame · host `tank`

> Line: 一张照片，一台显卡，我做出了五种风格的口播视频。而且，一分钱接口费都没花。

Opening hook: vertical selfie close-up with a slight handheld sway.

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

### 2. Segment `b5` · selfie vlog · host `tank`

> Line: 最惊艳的是口型：给它一张照片、一段配音，嘴型就自己对上了，不用抽卡。

Vlog segment (`vlog`): relaxed "sharing a favorite tool" acting with head tilts, nods and a hand gesture.

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

### 3. Segment `b8` · presenter full frame · host `tank`

> Line: 想要这套流程的，评论区扣一，我把步骤整理给你。

Closing ask ("comment 1 and I'll send the steps").

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

### Other prompts from the same video

**Music 3 background music** · `b_huazi/edit/public/music/bgm.prompt.txt`

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

## Style C · Launch breakdown

**Video:** "MiniMax H3: picture and sound together", host `tank`, 16:9 (presenter at the side) · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-c-h3-launch.mp4) · project folder `c_launch/` (file paths below are relative to it; presenter prompts are saved in `gen/prompts/`)

### 1. Segment `c1` · presenter full frame · host `tank`

> Line: 文生图、图生视频，你都见过了。但今天这个模型，画面和声音是一起生成的。

Opening: one line on what is new about the launch.

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

### 2. Segment `c3` · board + presenter window · host `tank`

> Line: 最实用的是参考生视频：给它一张照片、一段配音，人物的口型就跟着配音走。

Feature segment (`pip`): explaining tone, glances at a screen, small pointing gestures.

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

### 3. Segment `c5` · presenter full frame · host `tank`

> Line: 不花一分钱接口费，代价是电费和耐心。你会拿它做什么？评论区告诉我。

Closing: states the cost, then asks the viewer a question.

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

### Other prompts from the same video

**Music 3 background music** · `c_launch/edit/public/music/bgm.prompt.txt`

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

## Style D · Step-by-step tutorial

**Video:** "Three steps to a local talking-head video", host `girl`, 16:9 · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-d-tutorial.mp4) · project folder `d_tutorial/` (file paths below are relative to it; presenter prompts are saved in `gen/prompts/`)

### 1. Segment `d1` · presenter full frame · host `girl`

> Line: 想做数字人口播，又不想花钱买接口？今天三步，在自己电脑上跑通。

Opening: the pain point plus the promise of three steps.

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

### 2. Segment `d2` · board + presenter window · host `girl`

> Line: 第一步，克隆声音。录一段十几秒的干声，交给千问的语音模型，再输入新台词，就能配出同一个声音。

Step segment (`pip`, over terminal / timeline footage): the longest segment, about 10 s.

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

### 3. Segment `d5` · presenter full frame · host `girl`

> Line: 整套流程不花一分接口费。想要完整的命令清单，评论区留言。

Closing: recap plus "comment for the command list".

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

### Other prompts from the same video

**Music 3 background music** · `d_tutorial/edit/public/music/bgm.prompt.txt`

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

## Style E · Two-host relay

**Video:** "Before you pay on Singles' Day: 3 traps", hosts `girl` + `tank`, 16:9 · [▶ Watch](https://github.com/walkskysu/digital-human-koubo-comfyui/releases/download/local-demos/local-e-relay.mp4) · project folder `e_relay/` (file paths below are relative to it; presenter prompts are saved in `gen/prompts/`)

### 1. Segment `e2` · selfie vlog · host `tank`

> Line: 第一个坑，分期免息。免的是利息，手续费可一分没少，先算清楚再下单。

Second host `tank` takes over: her own photo, voice and selfie-vlog framing.

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

### 2. Segment `e3` · presenter full frame · host `girl`

> Line: 第二个坑，先涨价再打折。加购之前，记下最近三十天的价格，一对比就知道。

Scene image as the reference (the segment sets `"ref": "scene/live.png"`): the person is described with `look_person`, and framing and set follow the reference.

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

### 3. Segment `e4` · selfie vlog · host `tank`

> Line: Third trap: don't buy extra stuff just to hit the discount threshold. If you don't need it, it's not a deal.

Switching to English mid-video: the line is tagged `<d>[English] ...</d>` and the voice is generated in English.

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

### Other prompts from the same video

**Qwen Image 2.1 scene: livestream room (scenes.json)** · `e_relay/scenes.json`

```text
Picture 1 中的女生站在一间明亮温馨的电商直播间里，正对镜头，从腰部以上的中景，头顶留出背景空间。同样的脸、同样的齐刘海黑长直发、同样的米白色罗纹背心。她身后是暖色灯光照亮的货架，摆着包装好的礼盒和日用品，旁边有一个环形补光灯和一个绿植，背景轻微虚化。横屏构图，人物在画面正中间，左右两侧都能看到背景。画面里不要任何文字、标志、价格牌或字幕。
```

**Music 3 background music** · `e_relay/edit/public/music/bgm.prompt.txt`

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

## Writing your own

- Let `comfy_batch.py` generate presenter segments: run `--stage tts` and listen first, then `--stage video`. It saves every prompt to `gen/prompts/`, so look there first when something goes wrong.
- When writing an H3 prompt by hand, follow the Ref2VA format in the `h3-prompt-writing` skill: `subject_definitions / summary / retention_analysis / detailed_description`, plus `overall_soundscape` and `non_diegetic_music`.
- The line must match the voice-over word for word for accurate lip sync. Write numbers out in Chinese characters (七十二, not 72) so the TTS reads them reliably.
- Say "lips rest gently closed" for pauses and "closes her lips into a soft smile" at the end; this stops the mouth moving after the last word.
- Every prompt ends with `No subtitles, no captions, no on-screen text.`: captions and graphics are added in Remotion.
