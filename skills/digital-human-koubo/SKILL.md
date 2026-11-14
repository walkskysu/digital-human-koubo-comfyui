---
name: digital-human-koubo
description: 用固定的数字人形象（白背心数字人 / 用户本人数字人 / 猫狗角色）做口播视频。生成有两条路线：本地 ComfyUI（Qwen3-TTS 克隆配音 → MiniMax H3 照着配音对口型，Qwen Image 场景图、Music 3 配乐，不花积分；检测到 127.0.0.1:8188 就默认走本地）或云端 Renoise Grok Video 1.5（先报价、用户确认才生成）。先按内容推荐剪辑风格让用户选（小林式解说 / 网红花字口播 / 发布解读 / 保姆级教程 / 多主播多语言），自动套上从 MrBeast、MKBHD、影视飓风、Johnny Harris、Vox、半佛、差评等头部博主拆出来的 48 个包装组件（开场钩子、数字钉子、文字在人身后的景深字、证据截图、地图路线、弹幕、投票、复盘板…），再写稿 → 切段 → 生成 → 逐段回听 → 对齐 → Remotion 剪辑出片 → 默认做封面（16:9 / 9:16 / 3:4）并接成成片首帧。触发：在本地做个口播、本地做口播、做个口播、用我的显卡做口播、本地数字人口播、不花积分做口播、用开源模型做数字人、用我的数字人讲这段、数字人口播、让白背心数字人说、用数字人 Skill、数字人带货 / 解读 / 教程 / 种草视频、做成小林说那样、加花字、加包装 / 加地图 / 加弹幕 / 开场加预告 / 文字放在人身后、做成 MrBeast 那种节奏、有哪些包装手法。不用于：换一个全新形象（先按 references/new-avatar.md 做形象）、冒充真人。
---

# 数字人口播

形象、声音、提示词、切段规则固定在 `persona.json`；剪辑风格在 `references/style-menu.md`。每次照这里做，出来的就是同一个人、同一种风格。

## 红线
- 云端路线生成花用户的 Renoise credits：create_tasks 之前先报「段数 · 秒数 · 预估 credits · 余额」，等用户在对话里明确同意。先拍第 1 段给用户确认音色，再批量。重拍也要先报价。本地路线不花钱但占 GPU，开跑前同样报「段数 · 秒数 · 预估 GPU 时间」等用户同意。
- 成片标「内容由 AI 数字人演绎」；场景、动物片段、B-roll 角上标「AI 生成」。用户明确要去掉画面标注时照做，但要提醒：公开发布时在平台发布页勾选「AI 生成」声明。
- 用户本人的形象（persona.json → other_hosts.me）只用在用户自己的片子里。
- 「小林式」只学结构和剪辑手法：不用真实创作者的脸、声音、布景和原句。
- 点名评价第三方产品的说法，要有出处或标「网友分析 / 个人体验」。展示素材只用用户自己的作品；带歌词字幕的片子不用。

## 流程

### 准备：先检查，有就跳过，缺才引导安装（每次新对话第一次用时做）
**原则：已经装好的一句话带过，不让用户重装；缺什么才给装法，装法给多种，先放用户当前用的那种。** 详细装法在 references/install.md。
0. **选生成路线（先做这一步）**：
   - 用户已经点名路线（「在本地做 / 本地做 / 用我的显卡 / ComfyUI / 开源模型 / 不花积分」→ 本地，说到「本地」两个字就算；「用 Renoise / Grok / 云端」→ 云端）→ 照用户说的走，不再问。本地路线照样做下面的 8188 检查，连不上就停下告诉用户先启动 ComfyUI。
   - 没点名 → 先检查本地 ComfyUI：`curl -s -m 5 http://127.0.0.1:8188/system_stats`（地址以 persona.json → `comfy.url` 为准）。
     - 能连上 → **默认走本地路线**，只说一句「检测到本地 ComfyUI（版本 X，显卡 Y），默认用本地生成，不花积分；想用 Renoise 云端说一声」，不用问，接着干活。后面按「本地 ComfyUI 路线」一节做，不用检查 Renoise。
     - 连不上 → 问用户用哪种方式做视频（Claude Code 用 AskUserQuestion，其他工具列编号）：①本地 ComfyUI（不花积分，要先启动 ComfyUI，需要 24 GB 左右显存，装法见 references/install.md / README）②Renoise 云端（花积分，按下面第 1 步检查连接）。用户选了本地就等他启动 ComfyUI 后再测一次 8188。
   - 选定的路线写进 `brief.json` 的 `"route": "local"` / `"cloud"`，后面每一步按它来。
1. **Renoise MCP**（只在云端路线时检查）：直接调 `get_account`。
   - 成功 → 只说一句「Renoise 已连接，余额 X 积分」，接着干活。
   - 工具不存在 / 未连接 → 停下引导安装。用户还没有 Renoise 账号时，注册链接一律给 https://renoise.ai/mcp?utm_medium=xcom&utm_source=official（原样给出，保留 utm 追踪参数，不要改写成 renoise.ai 首页）。然后把用户当前客户端的装法放第一个并标「推荐」，下面列出其他方式（Claude 桌面端/网页连接器、Claude Code 插件、Codex `codex mcp add`、OpenClaw、Cursor 等通用远程 MCP 配置、renoise.ai/plugin 官网），让用户自己挑。装完让用户重开对话或重连，再调一次确认。
   - 报工具被关闭 → 不是没装，让用户去连接器设置里打开；报授权过期 → 重新登录授权，不用重装。
2. **本机环境**（要剪辑时才需要）：`bash scripts/doctor.sh`。有的打 ✓ 不提；缺的它会按 macOS / Windows / Linux 列出多种装法。系统软件让用户自己装，Python 包可以在用户同意后帮装。
3. **数字人形象**：persona.json 的 reference_material 能用就直接用；当前账号用不了（换了账号、素材过期、别人的包）→ 按 references/new-avatar.md 用用户自己的照片重做。

### 0. 看内容 → 推荐风格 → 让用户选
按 `references/style-menu.md`：
1. 一行诊断（内容类型、有没有可展示的素材、适合的平台和时长）。
2. 推荐 2 个风格并说理由，把 `assets/styles/` 里对应的预览图发给用户。
3. 一次问完：风格 · 比例和时长 · 花字强度（克制 / 标准 / 热闹）· 主播（白背心 / 用户本人 / 两人接力 / 动物）。每题第一个选项是推荐项。Claude Code 用 AskUserQuestion，其他工具列编号。
4. 用户回「你定」就按推荐，并说一句按了什么。结果写进 `brief.json`，后面每一步按它来。

| 风格 | 比例 | 时长 | 剪辑实现 |
|---|---|---|---|
| A 小林式解说 | 16:9 | 3–20 分钟 | `templates/lin-169`（plan.json → scenes.json 驱动：景深字 / 题板+主播小窗 / B-roll / 公式逐项长出 / 算例 / 图表，见 references/lin-style.md） |
| B 网红花字口播 | 9:16 | 30–120 秒 | `templates/huazi-916`（edit.json 驱动，三档花字） |
| C 发布解读 | 16:9 | 30–90 秒 | 参考实现 `templates/reference/launch-169` |
| D 保姆级教程 | 16:9 | 3–8 分钟 | 参考实现 `templates/reference/tutorial-169` |
| E 多主播多语言 | 16:9 | 3–7 分钟 | 参考实现 `templates/reference/multihost-169` |

### 1. 写稿 → script.json
按选定风格的稿子写法（style-menu.md 里每种都有）。每段一句或两句，10 秒左右（约 40–55 字，Grok 中文约 5.4 字/秒），标 `shot`：`full`（全屏出镜）/ `pip`（画中画讲解）/ `vlog`（随意自拍口吻）/ `depth`（要做「文字在人身后」的段：中景、头顶两侧留背景）。英文缩写、网址写成好念的样子；字幕要显示原写法时在那段加 `"sub": {"SKILL 点 M D": "SKILL.md"}`（align.py 按念法对齐、字幕换回写法）。外语段直接写目标语言的台词。

### 2. 切段 + 报价
`python3 scripts/build_tasks.py script.json tasks.json --purpose "teaching a beginner tutorial step by step"`
→ 打印段数、秒数、预估 credits。full 段 720p（17/秒），pip 段 480p（10/秒）。**主播要裁成半身 / 放大显示、或者 pip 段的主播卡并不小时，所有出镜段一律 720p（`--all-720p`）**：480p 原片只有 400×736，裁半身再铺满大卡会放大 2 倍以上，明显发糊（vibe-knowledge 介绍片因此重拍 4 段，多花 680 积分）。拿 `estimate_cost` 核一次，报给用户等确认。用户本人或动物主播用 persona.json → other_hosts 里的提示词模板。

### 3. 生成
tasks.json 每 10 个一批 create_tasks → wait_tasks。要进场景（直播间、门店、街景）时先用 GPT Image 2.5 合成开场画面（人物参考图 + 场景描述，2k 约 23 积分），再把这张图当 Grok 的参考图。

### 4. 下载（Renoise 美国 CDN 很慢，必须这样下）
download_results 拿链接 → 整理成 `urls.txt`（每行 `<taskId>.<ext> <url>`）→ `python3 scripts/rangedl.py`：每个文件 6 段 Range 并发、断点续传、下完 ffmpeg 解码校验。

### 5. 回听 + 抽帧 + 拼接
`python3 scripts/assemble.py script.json ids.json --out 成片_完整版.mp4`（ids.json = {段 id: taskId}）：whisper 逐段转写比对文稿、只保留到说完后 0.25 秒、拼接、loudnorm -16。剪辑用 `cut/joined.mov`：拼接前已把每段音频补齐到和画面等长，避免几十段拼下来声音累积落后口型；拼完会打印画面和声音的时长，两者必须一致。改过某段后用 `--rejoin` 只重新拼。
- whisper `--prompt 原文` 会让个别段漏掉前半句，用中性提示「以下是普通话的句子。」。外语段按语言转写；日韩阿拉伯语不要加 `-ml 1`（会把多字节字符截断成乱码）。
- **每段抽 4 帧看一眼**：Grok 横屏口播偶尔自己烧字幕（提示词写了也挡不住），有就重拍那段。
- Grok 有时漏念开头的语气词：没影响意思就按实际口播改字幕，别为这个重拍。
- **念错字（不是漏语气词）要当场修，不能交给用户去听**：
  - **查**：`python3 scripts/misread_check.py script.json`，按停顿切句、不带原文逐句转写，列出可疑字。**不能拿带原文提示的转写判断读音**：它会把念错的字纠正回去（「通胀」念成 tōng zhèng，带原文照样判全对）。同音字会误报，可疑处听一下确认。
  - **修（0 积分、保口型）**：`python3 scripts/patch_words.py script.json patch.json --ref <2–3 段干净原声> --synth-only` → 填克隆句时间 → 再跑 → `assemble.py --rejoin`。只把错的那一句换成 MiMo 克隆音，长度拉到和原句一样，切在停顿上。换整句比只换两个字自然。
  - **别整片换音色**：口型跟的是原声，整片换掉会到处对不上；也别先提 OmniHuman 重做口型（全片约 5,000 积分）。
  - 口型实在差太多，再报价重拍那一段。
- 开头第一个字最容易被吞或念歪（例：「一个知识点」→「几个知识地点」），写稿时第一段开头别放关键名词，或者先垫一个短词。

### 6. 对齐 + 剪辑
`python3 scripts/align.py script.json --out <工程>/src/tl.json` 出逐字时间轴，然后按 brief.json 的风格剪：
- **B 花字口播**：`bash scripts/new_edit.sh huazi-916 <工程>` → 写 `src/edit.json`（关键词、表情、卡片、作品展示、号召，字段见 references/huazi.md）→ `python3 scripts/check_edit.py <工程>/src` → 抽帧 → 渲染。
- **A 小林式**：`bash scripts/new_edit.sh lin-169 <工程>`，按 `references/lin-style.md` 做：
  1. `lin_subs.py` 出字幕（数字用 disp.txt 显示成阿拉伯数字）。
  2. 写 `plan.json`，示例见 `templates/lin-169/plan.example.json`，时间写「@s07:两千」。
  3. 跑 `lin_scenes.py --face` 生成 scenes.json，并自动量主播脸的位置给小窗用。
  4. B-roll 用 Wan 3.0 生成（先报价，每段约 60 积分），景深字段跑 `cutout_video.py` 抠像。
  5. 渲染。每个场景抽开头和中点两帧检查，重点看小窗有没有挡住内容、有没有空板。
  - 只做纯图表、不出镜的财经长片，仍可用 finance-explainer 的引擎。
- **C / D / E**：`bash scripts/new_edit.sh reference/<目录> <工程>`，换 tl.json，按段重写 Scene（templates/reference/README.md）。
- **包装（每种风格都做）**：按 `references/packaging-presets.json` 里这个风格的默认包装排——开场 30 秒按 open 顺序、正文保证 stimulus_every_s 秒内有一个新视觉事件、讲到 per_beat 里那类内容就用对应组件、recurring 全片挂着。组件写进 `pack` 数组（字段见 references/packaging.md），手法依据见 references/packaging-playbook.md。用户点名要的手法（「加地图」「开场加预告」「加弹幕」「换成 MrBeast 那种」）在默认基础上加减。用户问「有哪些包装」先发 `assets/packaging/图鉴.jpg`。景深字（文字在人身后）要先跑 `scripts/cutout_video.py` 抠像，见 references/packaging.md。
- 声音：数字人视频轨一定 `muted`，人声单独铺一条；多段 Grok 原声用 `python3 scripts/voicefx/unify.py <输出目录> <片段…>` 统一频谱 + 同一个小房间混响（复用旧段时加 `--ref 旧片段目录`，场景/动物片段加 `--scene`）。BGM 压在人声下约 20 dB。
  - **音效**：`python3 scripts/lin_sfx.py <工程>/src/scenes.json --out audio` 按场景自动排音效（earshot 音效库：切画面 whoosh、景深字和结果「碰」、卡片 pop、结论 bell）。音效要高出人声和音乐 8–10 dB，用 `earshot timeline --cues` 复查。
  - **BGM**：用 `earshot rank` 从曲库挑。
  - **混音和导出**：`python3 scripts/lin_mix.py` 做人声链 + BGM 循环避让人声 + 音效，出 −16 LUFS 的 mix.wav；加 `--speed 1.1` 出 1.1 倍成片（BGM 保持原速）。
  - **音画同步**：交付前在开头、中段、结尾各测一处声音偏移，要小于 10 ms。
- 抽帧检查一定看过渡的中间帧和零间隔衔接处（上一条的尾巴会盖住下一条）。

### 7. 封面 + 首帧（默认做，不用问）
平台默认拿视频第一帧当封面，所以每条片子都做封面，并把它接在成片最前面。交付的主文件就是带封面首帧的版本。
1. 写 `cover.json`（字段见 references/cover.md）：
   - 小字栏目名
   - 钩子标题 ≤8 字
   - 红色强调句 ≤6 字
   - 一句副标题
   - ≤3 个标签
   - 链接或号召
   - 主播帧
   - ≤2 张证据卡（官方截图、作品）
2. `python3 scripts/make_cover.py cover.json --candidates` 抽 12 帧拼成候选图。挑一帧笑着、眼睛睁开、没在说话或嘴型好看的，时间写进 `host.t`。
3. `python3 scripts/make_cover.py cover.json` 生成 `cover/cover_16x9.jpg`（横屏），按 ratios 还会出 `cover_9x16.jpg`（竖屏）和 `cover_3x4.jpg`（小红书）。看一眼 `thumb_*.jpg`，540px 宽时标题要读得清，文字不能压到卡片。
4. `python3 scripts/cover_first.py 成片.mp4 cover/cover_<比例>.jpg 交付.mp4`：封面停 0.5 秒后硬切进正片，声音整体后推 0.5 秒。抽 0 秒、0.45 秒、0.55 秒三帧确认。不带封面的版本另存为 `_无封面.mp4`。

## 本地 ComfyUI 路线（不花 Renoise 积分，替换第 2–5 步）
准备阶段第 0 步选了本地路线时走这条（用户点名本地，或没点名但 8188 能连上）。先配音再出画面：Qwen3-TTS 克隆配音 → MiniMax H3 参考生视频（配音当 `<Audio 1>` fully_copy，口型跟着配音走）→ 把原配音合回画面。配置在 persona.json → `comfy`，流程 JSON 在 `comfy/`。
1. **检查**：ComfyUI 能连上（`curl -s 127.0.0.1:8188/system_stats`），有 Qwen3-TTS 节点包和 H3 ref2va 模型 + 4 步 Lightning LoRA。主播要有 `voice_ref`（12–20 秒干声 + 逐字文本）。
2. **估时**：`python scripts/comfy_batch.py script.json --stage plan`（用 `~/.venvs/comfy-mcp/bin/python`，要 PyAV）。不花钱但占 GPU：10 秒一段约 8 分钟（RTX 3090，672×1216，4 步），报给用户。
   - **主播和画幅**：不写 `"host"` 默认用 `annie`。9:16 竖屏的片子给 `comfy_batch.py` 每个阶段都加 `--ratio 9:16`（或只在某段写 `"ratio": "9:16"`）：`annie` 会换用竖屏形象图 `assets/host_annie_vertical.png`（672×1216，演播室中景）；`ella` 本来就是竖屏自拍特写，只能出 9:16。
3. **配音**：`--stage tts`。每段配完自动用 SenseVoice 不带原文回听，准确率 < 90% 打 ⚠；念错就在 script.json 那段加 `"seed": 新数` 再跑（只重配这一段）。单段超过 14 秒报错：拆短台词。先让用户听第 1 段确认音色。
4. **出画面**：`--stage video`（长任务放后台跑）。完成的段记在 `gen/state.json`，中断后重跑自动跳过；台词改了只重做那段。
5. **检查**：每段抽帧看口型（停顿处闭嘴、结尾闭嘴）和人脸。
6. **拼接**：`python3 scripts/assemble.py script.json ids.json --src 'gen/{id}.mp4'`，后面第 6、7 步照常（2026-11-12 在 WSL Ubuntu 上跑通：assemble → align → huazi-916 渲染 → 封面 → 首帧）。WSL 里先 `source ~/.venvs/koubo/bin/activate`（numpy / pillow / playwright / av 都装在这里）。配音本来就照稿念，`misread_check` / `patch_words` 一般用不上；`voicefx/unify.py` 只需轻处理。
- 提示词是 H3 Ref2VA 格式（persona.json → comfy.prompt_template），每段存在 `gen/prompts/<id>.txt`。
- **进场景**（直播间、门店、街景）：先 `python scripts/comfy_scene.py scenes.json --out scene`（Qwen Image 2.1，`comfy/qwen_t2i.api.json`，形象照当参考图合成开场画面；纯文生图可加 `--enhance` 开提示词增强，每张约 25–50 秒，首张含加载最多约 5 分钟），再在 script.json 那几段加 `"ref": "scene/<id>.png"`，H3 就用这张图当参考。用场景图时提示词改用主播的 `look_person`（只写人物、不写布景），否则 `look` 里的默认演播室会把背景拉回去（2026-11-12 实测：暖白直播间被画成深蓝墙）；新主播记得补这个字段。四视图、贴纸四宫格也用它出。
- **B-roll**：`python scripts/comfy_broll.py broll.json --out <工程>/public/broll [--stage plan]`（H3 文生 / 图生视频，5 秒一段约 5–6 分钟，`--mp 0.4` 更快；带招牌的街景会出乱码字，写成招牌虚化）。字段见脚本文件头。
- **景深字抠像**：`cutout_video.py` 在非 macOS 上自动走 ComfyUI BiRefNet；**量脸**：`lin_scenes.py --face` 自动用 `face_center.py`（mediapipe）。
- **BGM**：`python scripts/comfy_music.py --out <工程>/public/music/bgm.mp3 [--caption "…"] [--seed 8]`（MiniMax Music 3，纯音乐，60 秒约 1 分钟出）。模型会提前收尾：lyrics 里 `[Instrumental]` 标签越多越长（5 个约 37 秒），比成片短也没关系，lin_mix.py 会循环。出完用 `earshot describe bgm.mp3` 听一下：voice 类别分数要低（没有人声），看 genre/mood 对不对。
- **earshot**：模型放本地文件夹时，`EARSHOT_CLAP` / `EARSHOT_AST` / `EARSHOT_HOME` / `EARSHOT_OFFLINE=1` 要写在 `~/.bashrc` 的「非交互就 return」那行**之前**，否则脚本里读不到，earshot 会去连 Hugging Face 卡住。`lin_sfx.py` 只用 `kit init/render`，不需要这两个模型。

## 参考
- references/install.md：Renoise MCP 和本机环境的多种装法（只在缺的时候用）
- references/style-menu.md：五种风格、内容诊断、怎么问用户、brief.json
- references/packaging.md：47 个包装组件的用法和参数（pack 写法、9:16 自动适配）
- references/packaging-playbook.md：头部博主实测结论（节奏、开场公式、字幕、声音、号召、红线），完整报告在 references/research/
- references/packaging-presets.json：五种风格各自的默认包装
- references/huazi.md：花字模板 edit.json 字段、九种卡片、三档强度、写法习惯
- references/lin-style.md：A 小林式的画面语法、13 种场景、流水线、B-roll 提示词、音效档位、踩过的坑
- scripts：
  - lin_scenes.py：plan.json 转 scenes.json，自动量脸
  - lin_subs.py：字幕
  - lin_sfx.py：earshot 音效
  - lin_mix.py：混音、变速导出
  - misread_check.py：查念错
  - patch_words.py：只换念错的句子，保住口型
- persona.json：白背心数字人 + 其他主播（用户本人、橘猫店长、柴犬主播）、提示词模板、动作库、多语言实测
- references/voice.md：换声音（MiMo 克隆 / 音色设计）
- references/new-avatar.md：从一张照片做新形象
- references/edit-styles.md：各剪辑工程的入口文件和声音统一做法
- references/cover.md：封面 cover.json 字段、三种比例的版式、首帧接法
- assets/styles/：五种风格的预览图（给用户选的时候发）
- assets/packaging/：包装组件图鉴（47 格总览 + 每个组件一张）
