# Cloud route (Renoise MCP, optional)

[中文](CLOUD.zh-CN.md) · [Back to README](../README.en.md)

This repository is about the local ComfyUI route. The cloud route of the original project, [andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo) (Grok Video, GPT Image, Wan), is kept as it was. You can choose per video, or mix it with the local route.

<p align="center"><img src="images/cover.jpg" width="820" alt="One photo + one sentence → a 27-second livestream sales ad"></p>

> This 27-second livestream ad has no real presenter. Face, voice, studio, captions and the price animation are all AI.
> The only input was one sentence: *"Use this digital human to make a 30-second livestream ad for the WorkBuddy course — 10 lessons, ¥99, was ¥999."*
> Total cost: **482 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) credits**.

## Cloud-route demos (from the original project)

| | | |
|:---:|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4"><img src="gifs/workbuddy-live-ad.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4"><img src="gifs/renoise-koubo-huazi.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4"><img src="gifs/text-behind.gif" width="300"></a> |
| **Livestream sales ad** · 9:16 · 27 s<br>Style B + depth-text price ¥999→¥99<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4) | **Product recommendation** · 9:16 · 89 s<br>Animated captions, emoji, picture-in-picture<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4) | **Text behind the presenter** · 5 s<br>Vision person matting, 3-layer composite<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4) |

| | |
|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4"><img src="gifs/tutorial-ep2.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4"><img src="gifs/tutorial-digital-human-upgrade.gif" width="400"></a> |
| **Step-by-step tutorial** · 16:9 · 4:36<br>The digital human teaches how she was made (Style D)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4) | **Digital human, upgraded** · 16:9 · 5:55<br>Two presenters, 6 languages, 4 scenes, cat & dog (Style E)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4) |
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4"><img src="gifs/memt-launch.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4"><img src="gifs/xiaolin-style-explainer.gif" width="400"></a> |
| **Launch breakdown** · 16:9 · 39 s<br>Presenter on the side, code B-roll on the right (Style C)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4) | **Finance / tech explainer** · 16:9 · 2:21<br>Charts, documents, chapter cards (Style A)<br>[▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4) |

> These presenters are AI digital humans; the male presenter is the original author's own digital twin, made from his own photo.

## Connect Renoise MCP

Create an account at **[renoise.ai](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)** first. Login is in the browser — you never paste an API key.

| Agent | How |
|---|---|
| Claude Code | `/plugin marketplace add ArcoCodes/renoise-plugins-official` then `/plugin install renoise@renoise-plugins-official` |
| Codex | `codex mcp add renoise --url https://renoise.ai/api/public/mcp` then `codex mcp login renoise` |
| OpenClaw | `openclaw plugins install renoise --marketplace ArcoCodes/renoise-plugins-official` |
| Claude desktop / claude.ai | Settings → Connectors → **Add custom connector** → name `Renoise`, URL `https://renoise.ai/api/public/mcp` |
| WorkBuddy, Cursor, Windsurf, Cline, 豆包, 千问, 纳米Work, … | add a remote MCP server with URL `https://renoise.ai/api/public/mcp` (typical config: `{"mcpServers":{"renoise":{"url":"https://renoise.ai/api/public/mcp"}}}`) |

Latest official instructions: **[renoise.ai/plugin](https://renoise.ai/plugin)**. Check it worked by asking your agent: *"查一下我的 Renoise 余额 / check my Renoise balance."*

## (Optional) Xiaomi MiMo TTS — designed or cloned voices

On the cloud route the default voice is Grok's native voice (best lip-sync). For a designed voice, your own cloned voice, or narration-only videos, the skill uses **Xiaomi MiMo TTS**:

1. Register at **[platform.xiaomimimo.com](https://platform.xiaomimimo.com/)** and create an API key. At the time of writing Xiaomi offered the TTS models free for a limited time — check the site for current pricing.
2. Put the key in an environment variable, or in `~/.config/ai-teardown/mimo.env`:
   ```bash
   mkdir -p ~/.config/ai-teardown && cat > ~/.config/ai-teardown/mimo.env <<'EOF'
   MIMO_API_KEY=your-key-here
   MIMO_BASE_URL=https://api.xiaomimimo.com/v1
   EOF
   chmod 600 ~/.config/ai-teardown/mimo.env
   ```
3. Only clone **your own** voice or a voice you have explicit permission to use.

> Note: Grok generates lip movement from its own voice. Swapping in a different voice afterwards leaves ~100 ms lip offset (fine in picture-in-picture, visible in full-screen close-ups). The local route avoids this by generating the lips from the cloned voice.

## Make your own digital human (cloud route)

1. Pick a photo: frontal face, even light, hair off the face, mouth closed. **Only your own photo or one you have permission to use.**
2. Ask the agent to generate a 4-view sheet (front, both sides, back) — GPT Image 2.5, 2k, ~23 credits (or Qwen Image 2.1 locally) — so the face stays the same from every angle.
3. Compare models with the same image and line (Grok Video 1.5 vs Wan 3.0, 8 s each) and pick one.
4. Upload the reference to Renoise and put its `material:<id>` into `skills/digital-human-koubo/persona.json` (`renoise.reference_material`, or `other_hosts.me` for a second presenter).

Details: [`references/new-avatar.md`](../skills/digital-human-koubo/references/new-avatar.md). The `material:` IDs in this repo belong to the original author's account and won't work on yours — that's expected. For the local route, just add a host to `persona.json → comfy.hosts` (see [Presenters](WORKFLOWS.md#presenters-for-the-local-route)).

<p align="center"><img src="images/scene-composite.jpg" width="720" alt="Reference photo → composited livestream studio"></p>

## Cloud cost reference (real runs)

| Video | Generation | Credits |
|---|---|---|
| Livestream ad, 9:16, 27 s | 1 scene image + 5 Grok segments (720p) | **482** |
| Tutorial Ep2, 16:9, 4:36 | 32 segments (full 720p / PiP 480p) + demos | ~3,250 |
| Tutorial Ep3, 16:9, 5:54 | 30 new segments + 7 scene images, 17 segments reused | ~3,409 |

Prices at the time of writing: Grok Video 1.5 — 720p 17 credits/s, 480p 10 credits/s; GPT Image 2.5 2k — 23 credits. Always confirm with the agent's live quote.
