#!/usr/bin/env python3
"""Genera els fons del disseny «Paper i fil» (assets/fons/clar-*.jpg i magenta-*.jpg).

Colors plans i clars, però amb tacte físic: teixit de lli (fils de trama i ordit),
gra de paper i un degradat suau, com un cartell imprés sobre tela.
Executar:  python3 tools/make_fons_clars.py
"""
from pathlib import Path
import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "fons"
rng = np.random.default_rng(1865)


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def blob(w, h, cx, cy, r):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((x - cx * w) / (r * max(w, h))) ** 2 + ((y - cy * h) / (r * max(w, h))) ** 2)
    return np.clip(1 - d, 0, 1) ** 1.6


def linen(w, h, period=5):
    """Teixit de lli: fils horitzontals i verticals amb irregularitats (gruixos desiguals)."""
    # fils: cada fil té una intensitat pròpia lleugerament diferent
    rows = rng.normal(0, 1, h // period + 2).astype(np.float32)
    cols = rng.normal(0, 1, w // period + 2).astype(np.float32)
    ry = np.repeat(rows, period)[:h][:, None]
    cx = np.repeat(cols, period)[:w][None, :]
    # perfil sinusoïdal dins de cada fil (relleu del fil)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    prof = (np.sin(y / period * 2 * np.pi) * .5 + np.sin(x / period * 2 * np.pi) * .5)
    # trames alternades (ordit/trama) per donar aspecte de teixit
    chk = (((y // period).astype(int) + (x // period).astype(int)) % 2).astype(np.float32)
    t = prof * .45 + (ry * .5 + cx * .5) * .35 + (chk - .5) * .25
    # irregularitat a gran escala (fils més gruixuts de tant en tant)
    big = rng.normal(0, 1, (h // 60 + 2, w // 60 + 2)).astype(np.float32)
    big = np.array(Image.fromarray(big).resize((w, h), Image.BICUBIC))
    return t + big * .18


def grain(w, h):
    g = rng.normal(0, 1, (h, w)).astype(np.float32)
    # gra lleugerament filtrat (fibres de paper)
    g2 = np.array(Image.fromarray(g).resize((w // 2, h // 2), Image.BILINEAR).resize((w, h), Image.BICUBIC))
    return g * .6 + g2 * .8


def make(name, w, h, base, glows, tex_amp, grain_amp):
    img = np.ones((h, w, 3), np.float32) * hexrgb(base)
    for (cx, cy, r, col, a) in glows:
        m = blob(w, h, cx, cy, r)[..., None] * a
        img = img * (1 - m) + hexrgb(col) * m
    t = linen(w, h)[..., None]
    g = grain(w, h)[..., None]
    img = img + t * tex_amp + g * grain_amp
    img = np.clip(img, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(OUT / name, quality=92, subsampling=0)
    print(name, w, h)


# Paper clar (crema càlid; cantonada dalt-dreta dauradeta, baix-esquerra rosadeta, com la inspiració)
CLAR = ("#F3EBDD", [(1.0, 0.0, 0.9, "#E6D6B6", .85), (0.0, 1.0, 0.8, "#EBD3CC", .95), (0.5, 0.5, 0.7, "#F7F1E6", .55)])
# Paper de dol (més fred i neutre, sense calidesa daurada)
DOL = ("#EFEBE6", [(1.0, 0.0, 0.9, "#DDD8D0", .7), (0.0, 1.0, 0.8, "#E3DCDC", .7), (0.5, 0.5, 0.7, "#F4F1ED", .55)])
# Magenta pla (tela tintada; més clar que el vellut d'abans)
MAG = ("#8A1F4B", [(0.75, 0.2, 0.95, "#A32A5E", .9), (0.1, 1.0, 0.8, "#6B1236", .85)])

for pre, (base, glows), amp, gr in (("clar", CLAR, 3.2, 2.4), ("dol", DOL, 3.0, 2.2), ("magenta", MAG, 3.6, 2.4)):
    make(f"{pre}-story.jpg", 1080, 1920, base, glows, amp, gr)
    make(f"{pre}-post.jpg", 1080, 1350, base, glows, amp, gr)
    make(f"{pre}-video.jpg", 1920, 1080, base, glows, amp, gr)
