# 网红花字口播模板（templates/huazi-916）

9:16，1080×1920，30fps。**内容全在 `src/edit.json`，时间全来自 `src/tl.json`**——改稿只动这两个文件。

## 起一个新工程
```bash
bash ~/.claude/skills/digital-human-koubo/scripts/new_edit.sh huazi-916 <工程目录>
```
然后放素材：`public/main.mp4`（拼好的数字人口播，竖屏）、`public/voice.wav`（处理过的人声）、`public/show/`（要展示的作品）、`src/tl.json`（`scripts/align.py` 的输出）。

## edit.json 字段
时间写法：`"3:"` 第 3 段开头 · `"3:end"` 第 3 段结束 · `"3:关键词"` 这个词开始 · `"3:关键词#2"` 第 2 次出现 · 数字 = 绝对秒。

| 字段 | 作用 | 例子 |
|---|---|---|
| `preset` | 花字强度 克制 / 标准 / 热闹 | `"标准"` |
| `title` | 顶部胶囊标题 | `{"left":"真实体验","right":"我为什么推荐 Renoise"}` |
| `chapters` | 章节胶囊（自动编 ①②③） | `[{"at":"4:","t":"隐私：MCP vs CLI"}]` |
| `keys` | 字幕里变色放大的关键词 | `["太臃肿","强烈建议"]` |
| `emojis` | 脸两侧弹的动态表情 | `[{"at":"2:太臃肿","e":"😵‍💫","side":"r"}]` |
| `punch` | 镜头推一下的时刻（不写就每段第一个关键词） | `["1:最大"]` |
| `cards` | 卡片，见下表 | |
| `showcase` | 主播缩小窗、全屏放作品 | `[{"from":"8:尤其","to":"8:end","items":[{"src":"show/a.mp4","label":"复刻"}]}]` |
| `cta` | 结尾号召大字 | `{"at":"11:强烈建议","text":"强烈建议","sub":"去试试 Renoise","subAt":"11:去试试"}` |
| `music` | 配乐 | `{"src":"music/bgm.mp3","vol":0.075}` |
| `sfx` | 音效表，**不手写**，由 `scripts/huazi_sfx.py` 生成（见下面「音效」） | `[{"at":21.77,"name":"slam-2","vol":0.63}]` |
| `voiceVol` | 人声和配乐一起乘的系数，`huazi_sfx.py` 需要时自动写 | `0.69` |
| `badge` / `credits` | 左上角 AI 标识 / 片尾署名 | 默认「内容由 AI 数字人演绎」 |
| `brand` | 主色 | `"orange"` / `"#FF7A1A"` |

### 卡片类型（cards[].type）
每张卡片都有 `at`，可选 `until`（默认到本段结束、下一张卡片或 4.5 秒，取最早）。

| type | 长什么样 | 什么时候用 | 关键字段 |
|---|---|---|---|
| `stamp` | 斜盖的描边印章 | 结论、「不用抽卡」 | text, color, x, y, rot |
| `slam` | 描边大字砸屏 | 吐槽、情绪最高点 | text, color |
| `big` | 黄色渐变大字块 | 标签式结论「起号神器」 | text |
| `number` | 数字滚动 | 价格、数量、积分 | value, unit, prefix, label |
| `vs` | 左右名牌 + VS | 对比两家 | left{at,t}, right{at,t} |
| `tags` | 2×2 彩色名牌逐个点亮 | 支持的平台 / 工具 | title, items[{at,t,color}] |
| `bars` | 横条对比 | 速度 / 价格对比（标「个人体验」） | title, items[{t,v,label,color}], note |
| `list` | ✅ / ❌ 清单 | 优缺点、两面 | title, items[{t,tone,at}] |
| `image` | 带白边的截图 | 官网、界面、聊天记录 | src, label, x, y, w, rot |

颜色可写 yellow / pink / cyan / red / green / orange / purple / white 或十六进制。

## 三档花字强度（对比图：assets/styles/B_huazi_presets.jpg，选强度时发给用户）
| | 克制 | 标准 | 热闹 |
|---|---|---|---|
| 字幕字号（普通 / 关键词） | 66 / 76 | 76 / 92 | 82 / 106 |
| 关键词颜色 | 黄 | 黄 | 黄 / 粉 / 青 轮换 |
| 逐字弹跳 | 很轻 | 明显 | 更弹 |
| 表情 | 隔一个出一个，偏小 | 全部 | 全部，更大 |
| 跳切推近 / 重点推镜 | 不交替 / 很轻 | 1.09 / 14% | 1.11 / 20% |
| 段间闪白 | 无 | 有 | 更亮 |
| 音效 | 0.6 倍 | 正常 | 1.2 倍 + 推镜处加 pop |
适合：克制 = 知识、品牌、严肃话题；标准 = 大多数口播；热闹 = 带货、搞笑、年轻向。不管哪档都**不做整段抖动**，只在关键帧推镜。

## 写 edit.json 的习惯（参考爆款口播）
- 关键词：每段 1–3 个，挑「情绪词 + 数字 + 产品名」，不要整句都标黄。
- 表情：每分钟 6–10 个，跟情绪走（惊讶 😱、推荐 😍、吐槽 😤、秘密 🤫、成功 💯），左右交替。
- 卡片：一段最多一张；一屏只说一件事，内容完整放下，别拆碎。
- 引用别人的说法（评测、扒料）在卡片 title 里写「网友分析 / 个人体验」。
- 作品展示 ≥ 3 秒一个，最多 3 个。

## 音效：只放在人声停顿里（每条片子都跑）
```bash
python3 ~/.claude/skills/digital-human-koubo/scripts/huazi_sfx.py <工程>/src          # 排音效，写进 edit.json 的 "sfx"
python3 ~/.claude/skills/digital-human-koubo/scripts/huazi_sfx.py <工程>/src --check  # 改过 edit.json 后复查
```
- **为什么**：模板自动配的音效（每张卡片、每个表情、每次推镜都响，一分钟 50 多个，音量 0.2–0.6 不等）全压在说话的字上，和人声糊在一起、忽大忽小（2026-11-15 用户反馈）。
- **规则**：音效只放在人声停顿里（段间停顿 + 够长的句间停顿），音效前后各留至少 0.2 秒没有人声；一个停顿只放一个；一分钟 10–12 个就够。表情和关键词推镜不出声。
- **画面跟着声音走**：卡片、插屏、关键词三连的 `at` 会被改成音效的时间（原写法留在 `at0`，重跑从 `at0` 重算），所以卡片是在一句话说完的停顿里「砸」出来，不卡在某个字上。附近 2 秒内没有停顿的卡片照常出现、不配音效。想让某张卡片有声音：把它的 `at0` 改到离段尾或句号更近的词，再跑一次。
- **响度**：所有音效拉到同一响度，比人声说话段高 5.5 dB（按音效主体的 RMS；成片里按 0.3 秒窗口量是比人声高 1–4.5 dB，听感「比人声大一点」）。`--over` 可调。
- **人声**：`assemble.py` 已把每段人声拉到同一响度（说话部分 RMS −20 dBFS，只加固定增益）。`public/voice.wav` 直接从 `cut/joined.mov` 抽，**不要再过 loudnorm**。
- 段间停顿不够 0.9 秒时（Grok 原声常见），音效会少；本地路线每段配音首尾自带静音，段间一般有 1 秒以上。

## 检查 + 渲染
```bash
python3 ~/.claude/skills/digital-human-koubo/scripts/check_edit.py <工程>/src     # 所有时间引用能对上才往下
npx remotion still src/index.ts Huazi out/a.jpg --frame=<帧>                    # 抽卡片、表情、展示过渡的中间帧
npx remotion render src/index.ts Huazi out/raw.mp4 --concurrency=6
python3 ~/.claude/skills/digital-human-koubo/scripts/export_mix.py out/raw.mp4 成片_无封面.mp4 --voice public/voice.wav
```
`export_mix.py`：画面不重压；声音量出整片响度后加固定增益到 −16 LUFS + 限幅，并裁掉 Remotion 带来的约 42.7 毫秒声音延迟，最后打印三处音画偏移（要 < 10 毫秒）。**不要用 `loudnorm`**：它是动态的，音效一响就把整体压下去，人声会忽大忽小。
示例数据：模板自带的 tl.json / edit.json 是「Renoise 推荐口播」那期（11 段 · 88 秒），可以直接照着改。
