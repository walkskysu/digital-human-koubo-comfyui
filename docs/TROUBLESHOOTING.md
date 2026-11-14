# Known pitfalls (all handled by the skill)

[中文](TROUBLESHOOTING.zh-CN.md) · [Back to README](../README.en.md) · [Install](INSTALL.md)

Each item below came up while making real videos; the text after the arrow is what the skill does about it now. Run `bash ~/.claude/skills/digital-human-koubo/scripts/doctor.sh` first: it lists any setup problem directly.

## Local route

- Without the Lightning LoRA, H3 at 0.8 MP needs more than 24 GB and hangs at step 0 → the workflows use the 4-step (presenter) and 8-step (B-roll) LoRAs.
- Qwen3-TTS occasionally garbles a word (e.g. "MiniMax" → "mini maxax") → every line is checked with SenseVoice *without* the script; add `"seed": <n>` to that segment and re-run, only it is redone.
- Lines longer than 14 s fail on purpose → split them; H3 quality drops on long single shots.
- With a scene image as reference, the studio described in `look` pulls the background back (a warm livestream room came out as a dark-blue wall) → `look_person` describes only the person and is used automatically when a segment has `"ref"`.
- MiniMax Music 3 tends to end early (28 s for a 60 s request) → more `[Instrumental]` tags in the lyrics make it longer (5 tags ≈ 37 s); the editors loop it anyway.
- H3 draws gibberish characters on shop signs → write "shop signs are blurred and out of focus", or pick shots without signs.
- Variables in `~/.bashrc` below the "not interactive → return" line are invisible to scripts → earshot tries to reach Hugging Face and hangs; put the `EARSHOT_*` exports above it.
- whisper / SenseVoice write spoken numbers as digits ("七十二" → "72") → `numcn.py` converts both sides to the spoken form before comparing. Digit-by-digit readings ("三零九零" for 3090) and homophones can still be flagged → listen before re-voicing.

## Both routes / cloud route

- Concatenating dozens of clips makes the voice drift behind the lips (measured: 0.38 s late by 4:43 over 44 clips) → `assemble.py` pads every clip's audio to its video length and checks audio/video durations match.
- whisper with the script as prompt "corrects" mispronounced words → `misread_check.py` transcribes pause-split clauses without the script; `patch_words.py` replaces just that clause with a voice-clone take stretched to the original length, so lip sync stays intact (don't re-voice the whole film).
- Always mute the presenter video track when a separate voice track is used; doubled audio a few ms apart sounds harsh (comb filtering).
- Expo easing never quite reaches the target (99.9 → rounds to 100) → counters snap to the exact value at the end.
- Grok occasionally **burns subtitles** into landscape clips even when told not to → frame check + re-shoot that segment.
- whisper writes Chinese numbers as digits (九百九十九 → 999), so accuracy drops but the line is correct → listen before re-shooting.
- Renoise's US CDN can truncate parallel downloads → `rangedl.py` downloads in 6 ranges with resume + decode check.
- Grok 9:16 720p is **720×1280** — never stretch it to another ratio.
