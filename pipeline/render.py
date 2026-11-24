#!/usr/bin/env python3
"""Ayah Daily renderer: builds a 1080x1920 Short from a JSON spec.

spec = {
  "audio": "assets/039053.mp3",
  "out": "out/sample.mp4",
  "surah_en": "Az-Zumar", "surah_ar": "الزمر", "ref": "39:53",
  "reciter_en": "Yasser Al-Dosari", "reciter_ar": "ياسر الدوسري",
  "segments": [{"start":0,"end":8.7,"ar":"...","en":"..."}],
  "scenes":   [{"path":"assets/a.jpg","start":0,"end":9,"move":"in"}]   # .mp4 = video
}
"""
import json, math, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
F_AR = os.path.join(HERE, "fonts/AmiriQuran.ttf")
F_AR_UI = os.path.join(HERE, "fonts/Amiri-Bold.ttf")
F_EN = os.path.join(HERE, "fonts/Amiri-Regular.ttf")
F_EN_B = os.path.join(HERE, "fonts/Amiri-Bold.ttf")
GOLD = (243, 214, 150)
CREAM = (255, 248, 235)
XFADE = 0.7      # scene crossfade seconds
TFADE = 0.35     # text fade seconds


def font(p, s):
    return ImageFont.truetype(p, s, layout_engine=ImageFont.Layout.RAQM)


def wrap(draw, text, fnt, maxw, rtl=False):
    words, lines, cur = text.split(), [], ""
    kw = dict(direction="rtl", language="ar") if rtl else {}
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt, **kw) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, text, path, size, maxw, maxlines, rtl):
    while size > 30:
        f = font(path, size)
        lines = wrap(draw, text, f, maxw, rtl)
        if len(lines) <= maxlines:
            return f, lines
        size -= 4
    return f, lines


def text_layer(seg):
    """Transparent RGBA layer with the Arabic + English for one segment."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    maxw = W - 150
    ar = seg["ar"].replace("۞", "").strip()
    for m in "ۚۖۗۛۙۘ":
        ar = ar.rstrip(" " + m).strip()
    far, ar_lines = fit_block(d, ar, F_AR, 92, maxw, 3, True)
    fen, en_lines = fit_block(d, seg["en"], F_EN_B, 54, maxw, 4, False)
    ar_lh, en_lh = int(far.size * 1.75), int(fen.size * 1.35)
    block_h = ar_lh * len(ar_lines) + 40 + en_lh * len(en_lines)
    y = int(H * 0.60) - block_h // 2           # centred a bit below middle, clear of Shorts UI
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    top = y - 50
    items = []
    for ln in ar_lines:
        tw = d.textlength(ln, font=far, direction="rtl", language="ar")
        items.append(((W - tw) / 2, y, ln, far, GOLD, True)); y += ar_lh
    y += 40
    for ln in en_lines:
        tw = d.textlength(ln, font=fen)
        items.append(((W - tw) / 2, y, ln, fen, CREAM, False)); y += en_lh
    bot = y + 20
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle([40, top, W - 40, bot], radius=48, fill=(8, 12, 28, 150))
    panel = panel.filter(ImageFilter.GaussianBlur(18))
    for x, yy, ln, f, col, rtl in items:
        kw = dict(direction="rtl", language="ar") if rtl else {}
        sd.text((x + 3, yy + 4), ln, font=f, fill=(0, 0, 0, 240), **kw)
    shadow = Image.alpha_composite(panel, shadow.filter(ImageFilter.GaussianBlur(5)))
    im = Image.alpha_composite(shadow, im)
    d = ImageDraw.Draw(im)
    for x, yy, ln, f, col, rtl in items:
        kw = dict(direction="rtl", language="ar") if rtl else {}
        d.text((x, yy), ln, font=f, fill=col + (255,), **kw)
    return im


def static_layer(spec):
    """Vignette/gradient + brand header + reciter footer (always on)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = np.zeros((H, W, 4), np.uint8)
    yy = np.linspace(0, 1, H)[:, None]
    # darker band behind text area (0.42-0.80) and soft top/bottom
    a = 0.45 * np.exp(-((yy - 0.60) / 0.17) ** 2) + 0.45 * np.clip((0.12 - yy) / 0.12, 0, 1) + 0.5 * np.clip((yy - 0.86) / 0.14, 0, 1)
    g[..., 3] = (np.clip(a, 0, 0.75) * 255).astype(np.uint8).repeat(W, 1)
    im = Image.alpha_composite(im, Image.fromarray(g, "RGBA"))
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(hp).rounded_rectangle([W/2-300, 100, W/2+300, 310], radius=40, fill=(8, 12, 28, 120))
    ImageDraw.Draw(hp).rounded_rectangle([W/2-300, 1415, W/2+300, 1535], radius=40, fill=(8, 12, 28, 110))
    im = Image.alpha_composite(im, hp.filter(ImageFilter.GaussianBlur(20)))
    d = ImageDraw.Draw(txt)
    # header
    f1 = font(F_EN_B, 40); f2 = font(F_AR_UI, 46); f3 = font(F_EN, 34)
    title = "AYAH DAILY"
    d.text(((W - d.textlength(title, font=f1)) / 2, 120), title, font=f1, fill=GOLD + (235,))
    d.line([(W / 2 - 60, 178), (W / 2 + 60, 178)], fill=GOLD + (160,), width=2)
    ref = f"Surah {spec['surah_en']}  •  {spec['ref']}"
    d.text(((W - d.textlength(ref, font=f3)) / 2, 196), ref, font=f3, fill=CREAM + (230,))
    sar = "سورة " + spec["surah_ar"]
    d.text(((W - d.textlength(sar, font=f2, direction="rtl", language="ar")) / 2, 244), sar, font=f2,
           fill=CREAM + (220,), direction="rtl", language="ar")
    # footer (kept above the bottom Shorts UI)
    f4 = font(F_EN, 36)
    rec = f"Recitation: {spec['reciter_en']}"
    d.text(((W - d.textlength(rec, font=f4)) / 2, 1430), rec, font=f4, fill=CREAM + (210,))
    h = "@AyahDaily365"
    d.text(((W - d.textlength(h, font=f4)) / 2, 1478), h, font=f4, fill=GOLD + (200,))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(txt.getchannel("A"))
    sh = sh.transform((W, H), Image.AFFINE, (1, 0, -2, 0, 1, -3)).filter(ImageFilter.GaussianBlur(4))
    return Image.alpha_composite(Image.alpha_composite(im, sh), txt)


def hook_layer(text):
    """Big attention-grabbing line shown in the upper third for the first seconds."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f, lines = fit_block(d, text, F_EN_B, 92, W - 140, 3, False)
    lh = int(f.size * 1.2); y = int(H * 0.30) - lh * len(lines) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    pos = []
    for ln in lines:
        x = (W - d.textlength(ln, font=f)) / 2; pos.append((x, y, ln)); y += lh
    for x, yy, ln in pos:
        sd.text((x + 3, yy + 5), ln, font=f, fill=(0, 0, 0, 255))
    im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)
    d = ImageDraw.Draw(im)
    for x, yy, ln in pos:
        d.text((x, yy), ln, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(20, 20, 30, 255))
    return im


def cover(img, w, h):
    iw, ih = img.size
    s = max(w / iw, h / ih)
    img = img.resize((math.ceil(iw * s), math.ceil(ih * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


class Scene:
    def __init__(self, sc):
        self.sc, self.start, self.end = sc, sc["start"], sc["end"]
        self.video = sc["path"].lower().endswith((".mp4", ".mov", ".webm"))
        if self.video:
            dur = self.end - self.start + XFADE
            clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                         sc["path"]], capture_output=True, text=True).stdout)
            k = max(1.0, dur / (clip - 0.1))          # slow the clip down rather than loop it
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sc["path"], "-t", f"{dur:.2f}",
                                  "-vf", f"setpts={k:.4f}*PTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                                  "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
            self.frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
        else:
            base = Image.open(sc["path"]).convert("RGB")
            self.big = cover(base, int(W * 1.18), int(H * 1.18))

    def frame(self, t):
        lt = max(0.0, t - self.start)
        if self.video:
            i = min(int(lt * FPS), len(self.frames) - 1)
            return Image.fromarray(self.frames[i])
        p = lt / max(0.1, self.end - self.start + XFADE)
        z = 1.0 + 0.12 * p if self.sc.get("move", "in") == "in" else 1.12 - 0.12 * p
        bw, bh = self.big.size
        cw, ch = bw / z, bh / z
        cx = bw / 2 + (self.sc.get("pan", 0) * 40 * (p - 0.5))
        cx = min(max(cx, cw / 2), bw - cw / 2)
        box = (max(0, cx - cw / 2), max(0, bh / 2 - ch / 2), min(bw, cx + cw / 2), min(bh, bh / 2 + ch / 2))
        return self.big.resize((W, H), Image.BILINEAR, box=box)


def main(spec_path):
    spec = json.load(open(spec_path))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                spec["audio"]], capture_output=True, text=True).stdout) + spec.get("tail", 1.2)
    scenes = [Scene(s) for s in spec["scenes"]]
    scenes[-1].end = max(scenes[-1].end, dur)
    static = static_layer(spec)
    layers = [(s["start"], s["end"], text_layer(s)) for s in spec["segments"]]
    hook = hook_layer(spec["hook"]) if spec.get("hook") else None
    HOOK_END = spec.get("hook_end", 3.2)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-i", spec["audio"],
                           "-af", f"adelay=300|300,apad,afade=t=out:st={dur-0.8:.2f}:d=0.8",
                           "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                           spec["out"]], stdin=subprocess.PIPE)
    n = int(dur * FPS)
    for i in range(n):
        t = i / FPS
        at = t - 0.3                                   # audio is delayed 0.3s
        cur = [s for s in scenes if s.start - XFADE / 2 <= t < s.end + XFADE / 2] or [scenes[-1]]
        if len(cur) == 2:
            a = np.clip((t - (cur[1].start - XFADE / 2)) / XFADE, 0, 1)
            fr = Image.blend(cur[0].frame(t), cur[1].frame(t), float(a))
        else:
            fr = cur[0].frame(t)
        fade_in = min(1.0, t / 0.6)
        fr = fr.convert("RGBA")
        fr = Image.alpha_composite(fr, static)
        if hook is not None and t < HOOK_END:
            a = min(1.0, t / 0.25, (HOOK_END - t) / 0.4)
            h2 = hook.copy(); h2.putalpha(hook.getchannel("A").point(lambda v: int(v * a)))
            fr = Image.alpha_composite(fr, h2)
        for st, en, lay in layers:
            if st - TFADE <= at < en:
                a = min(1, (at - (st - TFADE)) / TFADE, (en - at) / TFADE)
                if a >= 0.999:
                    fr = Image.alpha_composite(fr, lay)
                elif a > 0:
                    l2 = lay.copy(); l2.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
                    fr = Image.alpha_composite(fr, l2)
        out = np.asarray(fr.convert("RGB"))
        if fade_in < 1 or t > dur - 0.8:
            k = min(fade_in, max(0, (dur - t) / 0.8))
            out = (out * k).astype(np.uint8)
        ff.stdin.write(out.tobytes())
    ff.stdin.close(); ff.wait()
    print("wrote", spec["out"], f"{dur:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
