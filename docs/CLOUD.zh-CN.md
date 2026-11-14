# 云端路线（Renoise MCP，可选）

[返回 README](../README.zh-CN.md)

本仓库的重点是本地 ComfyUI 路线。原项目 [andyhuo520/digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo) 的云端路线（Grok Video、GPT Image、Wan）原样保留，每条片子可以自己选，也可以和本地路线混着用。

<p align="center"><img src="images/cover.jpg" width="820" alt="一张照片 + 一句话，27 秒直播带货广告"></p>

> 这条 27 秒的直播间广告里，主播不存在。脸、声音、直播间、花字、价格动画，全是 AI 做的。
> 输入只有一句话：「用这个数字人做一条 30 秒直播间广告，卖 WorkBuddy 上手课，10 节课 99 元，原价 999。」
> 总共花了 **482 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) 积分**。

## 云端路线示例（来自原项目）

| | | |
|:---:|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4"><img src="gifs/workbuddy-live-ad.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4"><img src="gifs/renoise-koubo-huazi.gif" width="230"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4"><img src="gifs/text-behind.gif" width="300"></a> |
| **直播间带货广告** · 9:16 · 27 秒<br>风格 B + 景深价格 ¥999→¥99<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4) | **产品推荐口播** · 9:16 · 89 秒<br>花字、动态表情、画中画<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4) | **文字在人身后（景深字）** · 5 秒<br>Vision 人像抠图，三层合成<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4) |

| | |
|:---:|:---:|
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4"><img src="gifs/tutorial-ep2.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4"><img src="gifs/tutorial-digital-human-upgrade.gif" width="400"></a> |
| **保姆级教程** · 16:9 · 4 分 36 秒<br>数字人亲自讲「我是怎么被做出来的」（风格 D）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4) | **数字人升级版** · 16:9 · 5 分 55 秒<br>两位主播、六种语言、四个场景、猫狗角色（风格 E）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4) |
| <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4"><img src="gifs/memt-launch.gif" width="400"></a> | <a href="https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4"><img src="gifs/xiaolin-style-explainer.gif" width="400"></a> |
| **发布解读** · 16:9 · 39 秒<br>主播在侧边，右侧代码动效（风格 C）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4) | **财经 / 科技解说** · 16:9 · 2 分 21 秒<br>图表、文件标黄、章节卡（风格 A）<br>[▶ 播放](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4) |

> 这些主播都是 AI 数字人；男主播是原作者用本人照片做的数字分身。

## 接入 Renoise MCP

先去 **[renoise.ai](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)** 注册账号。登录都在浏览器里完成，不用复制任何 API key。

| Agent | 怎么接 |
|---|---|
| Claude Code | `/plugin marketplace add ArcoCodes/renoise-plugins-official`，再 `/plugin install renoise@renoise-plugins-official` |
| Codex | `codex mcp add renoise --url https://renoise.ai/api/public/mcp`，再 `codex mcp login renoise` |
| OpenClaw | `openclaw plugins install renoise --marketplace ArcoCodes/renoise-plugins-official` |
| Claude 桌面端 / claude.ai | 设置 → 连接器 → **Add custom connector** → 名称 `Renoise`，地址 `https://renoise.ai/api/public/mcp` |
| WorkBuddy、Cursor、Windsurf、Cline、豆包、千问、纳米Work…… | 添加远程 MCP 服务器，地址 `https://renoise.ai/api/public/mcp`（常见配置：`{"mcpServers":{"renoise":{"url":"https://renoise.ai/api/public/mcp"}}}`） |

官方最新装法：**[renoise.ai/plugin](https://renoise.ai/plugin)**。装好后问 Agent 一句「查一下我的 Renoise 余额」，能查到就连上了。

## （可选）小米 MiMo 语音：音色设计 / 声音克隆

云端路线默认用 Grok 自带的声音（口型最准）。想要设计一个新音色、用你自己的克隆声音，或者做纯旁白视频，Skill 会调用 **小米 MiMo TTS**：

1. 去 **[platform.xiaomimimo.com](https://platform.xiaomimimo.com/)** 注册并创建 API Key。写这份文档时小米的 TTS 模型是限时免费的，具体以官网当前价格为准。
2. 把 Key 放进环境变量，或写到 `~/.config/ai-teardown/mimo.env`：
   ```bash
   mkdir -p ~/.config/ai-teardown && cat > ~/.config/ai-teardown/mimo.env <<'EOF'
   MIMO_API_KEY=你的key
   MIMO_BASE_URL=https://api.xiaomimimo.com/v1
   EOF
   chmod 600 ~/.config/ai-teardown/mimo.env
   ```
3. 只克隆**你本人**的声音，或明确授权给你的声音。

> 注意：Grok 的口型跟的是它自己生成的声音。事后换成别的声音，口型会差约 100 毫秒（画中画看不出，全屏特写看得出）。本地路线是照着克隆声音生成嘴型的，没有这个问题。

## 做你自己的数字人（云端路线）

1. 选一张照片：正脸、光线均匀、头发不挡脸、嘴闭着。**只用你本人或明确授权的照片。**
2. 让 Agent 生成四视图（正面、两个侧面、背面）：GPT Image 2.5，2k，约 23 积分（本地可用 Qwen Image 2.1），保证换角度不变脸。
3. 同一张图、同一句台词做多模型对比（Grok Video 1.5 vs Wan 3.0，各 8 秒），选一个。
4. 把参考图上传到 Renoise，把 `material:<id>` 写进 `skills/digital-human-koubo/persona.json`（`renoise.reference_material`；第二位主播写在 `other_hosts.me`）。

详细步骤见 [`references/new-avatar.md`](../skills/digital-human-koubo/references/new-avatar.md)。仓库里的 `material:` ID 属于原作者的账号，你的账号用不了，这是正常的。本地路线只要在 `persona.json → comfy.hosts` 里加一个主播（见[本地路线的主播](WORKFLOWS.zh-CN.md#本地路线的主播)）。

<p align="center"><img src="images/scene-composite.jpg" width="720" alt="参考照 → 合成直播间"></p>

## 云端成本参考（真实跑过的数）

| 视频 | 生成内容 | 积分 |
|---|---|---|
| 直播间广告 9:16 27 秒 | 1 张场景图 + 5 段 Grok 口播（720p） | **482** |
| 教程第二期 16:9 4 分 36 秒 | 32 段口播（全屏 720p / 画中画 480p）+ 演示素材 | 约 3250 |
| 数字人升级版 16:9 5 分 55 秒 | 30 段新片段 + 7 张场景图，复用 17 段 | 约 3409 |

写文档时的价格：Grok Video 1.5 720p 17 积分/秒、480p 10 积分/秒；GPT Image 2.5 2k 23 积分/张。以 Agent 实时报价为准。
