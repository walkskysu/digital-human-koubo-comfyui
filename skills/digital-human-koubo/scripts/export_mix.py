#!/usr/bin/env python3
"""Remotion 渲染出的 raw.mp4 → 交付文件：画面不重压，声音只做固定增益 + 限幅，并把声音对回画面。
用法：python3 export_mix.py out/raw.mp4 成片_无封面.mp4 [--voice public/voice.wav] [--lufs -16] [--main public/main.mp4]
- 不用 loudnorm：单遍 loudnorm 是动态的，音效一响就把整体压下去，人声听起来忽大忽小。这里先量整片响度，再整体加同一个增益，峰值用限幅器兜住。
- --voice：拿剪辑用的人声和成片的声音做互相关，量出声音晚了多少并裁掉。Remotion 的 AAC 编码会让声音整体晚约 42.7 毫秒（2048 个采样）。
  不给 --voice 就按 2048 个采样裁（--delay-samples 可改，0 = 不裁）。
- 导出后在开头、中段、结尾各测一次偏移（要 < 10 毫秒）并打印响度。"""
import subprocess, sys, re
A = sys.argv[1:]
if len(A) < 2: sys.exit(__doc__)
opt = lambda k, d: A[A.index(k) + 1] if k in A else d
src, dst, voice, lufs = A[0], A[1], opt('--voice', ''), float(opt('--lufs', -16)); SR = 48000


def load(p):
    import numpy as np
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)


def offsets(mix, ref, span=4800):
    """成片声音比参照人声晚多少个采样（开头 / 中段 / 结尾三处）。"""
    import numpy as np
    n = min(len(mix), len(ref)); res = []
    for t in (0.06, 0.5, 0.9):
        c = int(n * t); w = SR * 2; c = max(span, min(c, n - w - span)); x = mix[c:c + w]
        best = max(((float(np.dot(x, ref[c - l:c - l + w])), l) for l in range(-span, span + 1, 4)))
        res.append(best[1])
    return res


def loudness(p, af=''):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-af', (af + ',' if af else '') + 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1])


delay = int(opt('--delay-samples', 2048))
if voice:
    ref = load(voice); d = offsets(load(src), ref); delay = max(0, sorted(d)[1])
    print(f'渲染文件的声音比人声晚 {[round(x / 48, 1) for x in d]} 毫秒 → 裁掉 {delay} 个采样')
trim = f'atrim=start_sample={delay},asetpts=PTS-STARTPTS' if delay else 'anull'
gain = lufs - loudness(src, trim)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-c:v', 'copy', '-af', f'{trim},volume={gain:.2f}dB,alimiter=limit=0.89:attack=2:release=40:level=disabled',
                '-ar', str(SR), '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', dst], check=True)
msg = f'✓ {dst}：固定增益 {gain:+.1f} dB → {loudness(dst):.1f} LUFS'
if voice:
    d = offsets(load(dst), ref); ms = [round(x / 48, 1) for x in d]
    msg += f' · 音画偏移 {ms} 毫秒' + ('' if max(abs(x) for x in ms) < 10 else '  ⚠ 超过 10 毫秒')
print(msg)
