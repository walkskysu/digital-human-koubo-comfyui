#!/usr/bin/env python3
"""花字口播的音效排布：音效只放在人声停顿里，响度统一、比人声高一点，卡片跟着音效一起出现。
用法（要 numpy + ffmpeg；先放好 public/voice.wav、src/tl.json、src/edit.json）：
  python3 huazi_sfx.py <工程>/src [--over 5.5] [--margin 0.2] [--window 2.0] [--dry]
  python3 huazi_sfx.py <工程>/src --check        # 只检查现有 "sfx"：每个音效前后的人声静音、比人声高多少

为什么：模板自动配的音效（每张卡片、每个表情、每次推镜都响）会压在说话的字上，音量 0.2–0.6 不等，听起来和人声糊在一起、忽大忽小。
做法：
1) 从 voice.wav 找人声停顿（段间停顿 + 句间停顿）。
2) 要响的事件：开场、卡片、GlitchInterstitial / NumberSpike / KeywordStack、段间切换、片尾。每个事件找最近的、放得下这个音效的停顿
   （音效长度 + 前后各 --margin 秒），一个停顿只放一个音效；--window 秒内找不到停顿的事件不配音效（画面照常）。
3) 卡片和包装组件的 at 改成音效的时间（原写法存在 "at0"，重跑时从 at0 重新算），画面和声音同时出现。
4) 每个音效的音量 = 让它主体的 RMS 比人声说话段 RMS 高 --over dB，所以所有音效一样响。默认 5.5：这是 2026-11-15 用户听过认可的那版的实测值
   （短音效按主体算会偏高；同一版在成片里按 0.3 秒窗口量是比人声高 1–4.5 dB，听感是「比人声大一点」）。
   Remotion 的音量不能超过 1：音效开到最大还不够响时，改成把人声和配乐一起压低（写 "voiceVol"），相对关系不变，整片响度交给 export_mix.py 拉回。
5) 写进 edit.json 的 "sfx"；Huazi.tsx 看到 "sfx" 就不再自动配。表情、关键词推镜不再出声。作品展示的进出只在 0.5 秒内有停顿时才配音效（它的时间不能挪）。
渲染后用 export_mix.py 导出（固定增益，不用动态 loudnorm：它会在音效响起时把整体压下去）。"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

A = sys.argv[1:]
if not A or A[0].startswith('-'): sys.exit(__doc__)
opt = lambda k, d: type(d)(A[A.index(k) + 1]) if k in A else d
SRC = Path(A[0]); PUB = SRC.parent / 'public'
OVER, MARGIN, WINDOW = opt('--over', 5.5), opt('--margin', 0.2), opt('--window', 2.0)
SR = 48000
tl = json.load(open(SRC / 'tl.json')); ed = json.load(open(SRC / 'edit.json')); SEGS = tl['segs']


def T(r):
    if isinstance(r, (int, float)): return float(r)
    m = re.match(r'^(\d+):(.*)$', str(r)); s = SEGS[int(m.group(1)) - 1]; w = m.group(2)
    if not w: return s['start']
    if w == 'end': return s['end']
    word, _, nth = w.partition('#'); idx = -1
    for _ in range(int(nth or 1)): idx = s['text'].find(word, idx + 1)
    return s['chars'].get(str(idx), s['start'])


def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)


db = lambda x: 20 * np.log10(np.sqrt(np.mean(np.square(x, dtype=np.float64))) + 1e-9)
voice = load(PUB / ed.get('voice', 'voice.wav')); n = SR // 100
fr = np.sqrt((voice[:len(voice) // n * n].reshape(-1, n) ** 2).mean(1)); act = fr > 0.012
VOICE_DB = db(voice[:len(act) * n][act.repeat(n)]); TOTAL = len(voice) / SR
# 人声停顿：连续 ≥ 0.3 秒没有人声
pauses = []; i = 0
while i < len(act):
    if not act[i]:
        j = i
        while j < len(act) and not act[j]: j += 1
        if (j - i) / 100 >= 0.3: pauses.append([i / 100, j / 100])
        i = j
    else: i += 1
if not pauses or pauses[-1][1] < TOTAL - 0.02: pauses.append([TOTAL, TOTAL + 1.2])   # 片尾（模板会多留 1.2 秒）
else: pauses[-1][1] += 1.2
CUTS = [s['start'] for s in SEGS[1:]]


def body(name):
    """音效的主体：到衰减 30 dB 为止，最长 0.5 秒。返回（秒数, 主体 RMS dB）。"""
    f = PUB / 'sfx' / f'{name}.wav'
    if not f.exists(): return None
    x = load(f); pk = np.abs(x).max() + 1e-9; on = np.where(np.abs(x) > pk * 0.03)[0]
    d = min(0.5, (on[-1] + 1) / SR if len(on) else 0.2); return d, db(x[:int(d * SR)])


def silence_around(at, dur):
    a, b = int(at * 100), int((at + dur) * 100); pre = np.where(act[:a])[0]; post = np.where(act[b:])[0]
    return (a - pre[-1] - 1) / 100 if len(pre) else 9.0, post[0] / 100 if len(post) else 9.0, bool(act[a:b].any())


if '--check' in A:
    bad = 0
    for s in ed.get('sfx', []):
        at = T(s['at']); bd = body(s['name'])
        if not bd: print(f"⚠ {at:6.2f} {s['name']}: public/sfx 里没有这个文件"); bad += 1; continue
        pre, post, hit = silence_around(at, bd[0]); lv = bd[1] + 20 * np.log10(s.get('vol', 1)) - VOICE_DB - 20 * np.log10(ed.get('voiceVol', 1))
        flag = '⚠' if hit or min(pre, post) < 0.08 else ' '
        bad += flag == '⚠'
        print(f"{flag} {at:6.2f} {s['name']:8s} 比人声 {lv:+.1f} dB · 前静音 {pre:.2f}s · 后静音 {post:.2f}s" + ('  ← 压在人声上' if hit else ''))
    print(f"人声说话段 RMS {VOICE_DB:.1f} dB · {len(ed.get('sfx', []))} 个音效 · {'有 %d 处要处理' % bad if bad else '全部在停顿里'}")
    sys.exit(1 if bad else 0)

# ---------- 要响的事件 ----------
CARD_SND = {'stamp': 'slam-2', 'big': 'impact', 'slam': 'slam-1', 'tags': 'whoosh', 'bars': 'swish-2', 'list': 'swish-2', 'number': 'impact', 'image': 'swish-1', 'vs': 'pop'}
PACK_SND = {'GlitchInterstitial': 'whoosh', 'NumberSpike': 'impact', 'SlamText': 'slam-1', 'TiltLine': 'pop', 'KeywordStack': 'pop', 'ChapterCard': 'whoosh', 'FreezeFrame': 'slam-2'}
ev = []   # (时间, 音效, 回写函数, 说明)
at0 = lambda o: o.setdefault('at0', o['at'])
for k, c in enumerate(ed.get('cards', [])):
    ev.append([T(at0(c)), CARD_SND.get(c['type'], 'pop'), c, f"卡片 {c['type']}「{c.get('text') or c.get('title') or c.get('label') or ''}」"])
for it in ed.get('pack', []):
    u = it.get('use')
    if u not in PACK_SND: continue
    tgt = it['items'][0] if u == 'KeywordStack' and it.get('items') else it
    if 'at' in tgt: ev.append([T(at0(tgt)), PACK_SND[u], tgt, f'包装 {u}'])
for s in ed.get('showcase', []):
    ev.append([T(s['from']), 'whoosh', None, '作品展示 进']); ev.append([T(s['to']), 'whoosh', None, '作品展示 出'])
ev.sort(key=lambda e: e[0])
used = {}; out = []; log = []


def place(t, name, lo=None, hi=None, window=None):
    """找离 t 最近、放得下的停顿；返回音效开始时间。"""
    bd = body(name)
    if not bd: return None
    best = None
    for k, (a, b) in enumerate(pauses):
        if k in used or b - a < bd[0] + 2 * MARGIN: continue
        st = a + min(0.3, (b - a - bd[0]) / 2)          # 停顿够长就在人声停下 0.3 秒后响，短停顿放正中
        if abs(st - t) > (window or WINDOW) or (lo is not None and st < lo) or (hi is not None and st > hi): continue
        if best is None or abs(st - t) < abs(best[1] - t): best = (k, st)
    if best: used[best[0]] = name; return round(best[1], 2)
    return None


def add(st, name, why):
    bd = body(name); out.append({'at': st, 'name': name, 'vol': float(10 ** ((VOICE_DB + OVER - bd[1]) / 20)), 'for': why})


if pauses[0][0] == 0 and body('impact') and pauses[0][1] >= body('impact')[0] + MARGIN:   # 开场：人声开口前
    used[0] = 'impact'; add(0.0, 'impact', '开场')
for t, name, obj, why in ev:
    st = place(t, name, window=None if obj is not None else 0.5)
    if st is None: log.append(f'  {t:6.2f} {why}：{WINDOW if obj is not None else 0.5:g} 秒内没有放得下的停顿，不配音效（画面照常）'); continue
    if obj is not None:
        obj['at'] = st
        if 'until' in obj and T(obj['until']) < st + 1.0: obj['until'] = round(st + 2.5, 2)   # 挪后了，别一出现就消失
    add(st, name, why + (f'（{t:.2f} → {st:.2f}）' if abs(st - t) > 0.05 else ''))
for c in CUTS:                                          # 段间切换：还空着的段间停顿放一个 whoosh
    k = next((k for k, (a, b) in enumerate(pauses) if a - 0.05 <= c <= b + 0.05), None)
    if k is None or k in used: continue
    st = place(c, 'whoosh', lo=pauses[k][0], hi=pauses[k][1])
    if st is not None: add(st, 'whoosh', '段间切换')
last = len(pauses) - 1                                   # 片尾：最后一个字说完后
if last not in used and body('done'): add(round(pauses[last][0] + 0.3, 2), 'done', '片尾')
out.sort(key=lambda s: s['at'])
top = max([s['vol'] for s in out], default=1.0); vv = 1.0
if top > 1: vv = round(1 / top, 3); log.append(f'  音效开到最大还不够响：人声和配乐一起乘 {vv}（"voiceVol"），相对响度不变，整片响度由 export_mix.py 拉回')
for s in out: s['vol'] = round(min(1.0, s['vol'] * vv), 2)
print(f'人声说话段 RMS {VOICE_DB:.1f} dB · 停顿 {len(pauses)} 处 · 音效 {len(out)} 个（比人声高 {OVER:g} dB）')
for s in out:
    pre, post, hit = silence_around(s['at'], body(s['name'])[0])
    print(f"{'⚠' if hit else ' '} {s['at']:6.2f} {s['name']:8s} vol {s['vol']:.2f} · 前静音 {pre:.2f}s · 后静音 {post:.2f}s · {s['for']}")
print('\n'.join(log))
if '--dry' not in A:
    ed['sfx'] = out
    if vv < 1: ed['voiceVol'] = vv
    else: ed.pop('voiceVol', None)
    json.dump(ed, open(SRC / 'edit.json', 'w'), ensure_ascii=False, indent=1)
    print(f'→ 已写入 {SRC / "edit.json"} 的 "sfx"（卡片的 at 已跟着改，原写法在 at0）。接着跑 check_edit.py，再渲染。')
