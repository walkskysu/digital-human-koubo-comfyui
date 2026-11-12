#!/usr/bin/env python3
"""脸中心（跨平台，替代 macOS 专用的 face_center.swift）。
用法：python3 face_center.py <图片或视频> [--t 秒（视频取帧时间，默认 3）] [--all]
打印 "x y"：脸中心在 1920×1080 画布上的像素坐标（原点左上，和 face_center.swift 一致；竖屏素材同样按比例换算）。
--all：每张脸一行 "x y 宽 高 置信度"（同一画布坐标），先大后小。没找到脸时什么都不打印、退出码 1。
依赖：mediapipe + 模型 ~/models/blaze_face_short_range.tflite（或环境变量 FACE_MODEL）。
"""
import os, sys
from pathlib import Path

MODEL = os.environ.get("FACE_MODEL") or os.path.expanduser("~/models/blaze_face_short_range.tflite")
W, H = 1920, 1080


def load_rgb(path, t):
    import numpy as np
    if Path(path).suffix.lower() in {".mp4", ".mov", ".webm", ".mkv", ".m4v"}:
        import av
        with av.open(path) as c:
            s = c.streams.video[0]
            c.seek(int(max(0, t - 0.5) / s.time_base), stream=s, backward=True)
            last = None
            for f in c.decode(s):
                last = f
                if f.time is not None and f.time >= t:
                    break
            return last.to_ndarray(format="rgb24")
    from PIL import Image
    return np.asarray(Image.open(path).convert("RGB"))


def faces(rgb):
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
    if not Path(MODEL).exists():
        sys.exit(f"缺人脸模型 {MODEL}：curl -L -o ~/models/blaze_face_short_range.tflite "
                 "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite")
    h, w = rgb.shape[:2]
    opts = vision.FaceDetectorOptions(base_options=BaseOptions(model_asset_path=MODEL), min_detection_confidence=0.5)
    with vision.FaceDetector.create_from_options(opts) as det:
        res = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb.copy()))
    out = []
    for d in res.detections:
        b = d.bounding_box
        out.append(((b.origin_x + b.width / 2) / w, (b.origin_y + b.height / 2) / h, b.width / w, b.height / h, d.categories[0].score))
    return sorted(out, key=lambda f: -f[2] * f[3])


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    t = float(a[a.index("--t") + 1]) if "--t" in a else 3.0
    fs = faces(load_rgb(a[0], t))
    if not fs:
        sys.exit(1)
    if "--all" in a:
        for cx, cy, fw, fh, sc in fs:
            print(f"{cx * W:.0f} {cy * H:.0f} {fw * W:.0f} {fh * H:.0f} {sc:.2f}")
    else:
        print(f"{fs[0][0] * W:.0f} {fs[0][1] * H:.0f}")


if __name__ == "__main__":
    main()
