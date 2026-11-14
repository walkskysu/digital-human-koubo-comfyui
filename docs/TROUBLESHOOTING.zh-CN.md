# 踩过的坑（Skill 里都处理了）

[English](TROUBLESHOOTING.md) · [返回 README](../README.md) · [安装](INSTALL.zh-CN.md)

下面每一条都是实际做片时遇到的，箭头后面是 Skill 现在的处理办法。先跑一遍 `bash ~/.claude/skills/digital-human-koubo/scripts/doctor.sh`，环境问题它会直接列出来。

## 本地路线

- 不开 Lightning LoRA，H3 在 0.8MP 下超过 24 GB，卡在第 0 步 → 流程里主播用 4 步、B-roll 用 8 步 LoRA。
- Qwen3-TTS 偶尔会念糊一个词（比如 MiniMax 念成 mini maxax）→ 每句都用 SenseVoice **不带原文**回听；在那段加 `"seed": 新数` 重跑，只重配那一段。
- 单句超过 14 秒会直接报错 → 拆短；H3 单镜头太长质量会掉。
- 用场景图当参考时，`look` 里写的演播室会把背景拉回去（暖白直播间被画成深蓝墙）→ `look_person` 只写人物，段落有 `"ref"` 时自动用它。
- MiniMax Music 3 容易提前收尾（要 60 秒只给 28 秒）→ lyrics 里 `[Instrumental]` 标签越多越长（5 个约 37 秒）；剪辑模板本来就会循环。
- H3 画招牌会出乱码字 → 写 "shop signs are blurred and out of focus"，或者挑没有招牌的画面。
- `~/.bashrc` 里写在「非交互就 return」那行之后的变量，脚本读不到 → earshot 去连 Hugging Face 卡住；`EARSHOT_*` 要写在那行之前。
- whisper / SenseVoice 会把念出来的数字写成阿拉伯数字（七十二 → 72）→ `numcn.py` 比对前两边都转成读法。逐位念法（「三零九零」对 3090）和同音字仍可能被标出来 → 先听再决定重配。

## 两条路线通用 / 云端路线

- 几十段口播直接拼接，声音会一段段累积落后口型（实测 44 段到 4:43 晚 0.38 秒）→ `assemble.py` 拼接前把每段音频补齐到画面长度，并校验音画等长。
- whisper 带原文提示会把念错的字「纠正」回去 → `misread_check.py` 按停顿切句、不带原文转写；念错的用 `patch_words.py` 只换那一句（克隆音拉到原句长度），口型不受影响，不用整片换音色。
- 另配声音轨时，主播视频轨一定要静音；两条声音差几毫秒叠在一起会刺耳（梳状滤波）。
- expo 缓动到不了终点（99.9 四舍五入成 100）→ 计数动画结束时强制落在精确值。
- Grok 横屏口播偶尔**自己烧字幕**，提示词写了也挡不住 → 抽帧检查，重拍那段。
- whisper 会把中文数字写成阿拉伯数字（九百九十九 → 999），准确率会掉，但其实没念错 → 先听再决定重拍。
- Renoise 美国 CDN 并行下载会断成半截 → `rangedl.py` 6 段 Range 续传 + 解码校验。
- Grok 9:16 720p 是 **720×1280**，别拉成别的比例。
