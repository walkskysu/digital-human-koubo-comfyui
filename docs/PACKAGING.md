# Editing styles and the 48 packaging components

[中文](PACKAGING.zh-CN.md) · [Back to README](../README.en.md)

## Five editing styles

<p align="center"><img src="images/five-styles.jpg" width="820" alt="The five editing styles"></p>

| Style | Ratio | Length | Best for | Template |
|---|---|---|---|---|
| **A** Finance / tech explainer (Xiaolin-style structure) | 16:9 | 3–20 min | events, data, "why…" | `templates/lin-169` (plan.json-driven: text behind presenter, boards + presenter PiP, B-roll, formulas built term by term, worked examples, charts) |
| **B** Influencer talking head with animated captions | 9:16 | 30–120 s | product picks, sales, opinions | `templates/huazi-916` (data-driven) |
| **C** Launch breakdown | 16:9 | 30–90 s | new products / models | `templates/reference/launch-169` |
| **D** Step-by-step tutorial | 16:9 | 3–8 min | "how to…", tool setup | `templates/reference/tutorial-169` |
| **E** Multi-host · multi-language · multi-scene | 16:9 | 3–7 min | capability demos, going global | `templates/reference/multihost-169` |

Style B has three caption intensities — **restrained / standard / lively**:

<p align="center"><img src="images/huazi-presets.jpg" width="820" alt="Caption intensity presets"></p>

Style A learns only the *structure and editing grammar* of popular explainer channels. It never uses a real creator's face, voice, set or lines.

## 48 packaging components

We measured 25 videos frame by frame (shot detection, opening beats, on-screen text, sound) — full reports in [`references/research/`](../skills/digital-human-koubo/references/research/).

<p align="center"><img src="images/creator-pacing.jpg" width="720" alt="Cuts per minute measured on 25 creator videos"></p>

**Rules distilled from the research** ([`packaging-playbook.md`](../skills/digital-human-koubo/references/packaging-playbook.md)):
- Cut count can be low, but stimulation can't stop: in the first 30 s, something new every 3–5 s.
- First 3 s: the claim or the action — no greeting, no logo.
- A BGM bed under everything; sound effects only on events (1–3 per minute in Chinese talking-head channels); 0.6–1.0 s of silence right before a reveal.
- For a single-camera digital human, the cheapest pacing is **punch-in cuts** on sentence boundaries (1.0× / 1.18× / 1.32×).

<div align="center">
<a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4"><img src="gifs/packaging-gallery.gif" width="560"></a><br>
<b>Packaging component gallery</b> · 48 components · 2:40 · <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/packaging-gallery.mp4">▶ Watch</a>
</div>

<p align="center"><img src="images/packaging-gallery.jpg" width="820" alt="Packaging component gallery"></p>

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
Reference: [`references/packaging.md`](../skills/digital-human-koubo/references/packaging.md). Validate before rendering: `python3 scripts/check_edit.py <project>/src`.

## Text behind the presenter

<p align="center"><img src="images/text-behind-layers.jpg" width="760" alt="Original → person matte → original + big text + cut-out presenter"></p>

```bash
python3 scripts/cutout_video.py public/main.mp4 public/main_cut_s4.webm --from 17.2 --to 22.4   # matte only the seconds you need
```
On Linux / Windows the matte comes from BiRefNet in ComfyUI; on macOS from Apple Vision. It works on **medium shots with headroom**. In a selfie close-up the person fills ~89 % of the frame and hides the text — the script warns above 60 %. Mark such segments `"shot": "depth"` and they are generated as medium shots.

<p align="center"><img src="images/closeup-vs-medium.jpg" width="560" alt="Close-up (89%) hides the text, medium shot (57%) shows it"></p>
