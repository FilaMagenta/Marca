#!/usr/bin/env python3
"""Genera els fons 4:5 (1080×1350) a partir dels fons quadrats existents, allargant la zona central buida.
Executar:  python3 tools/make_bg_34.py"""
from pathlib import Path
from PIL import Image

F = Path(__file__).resolve().parent.parent / "assets" / "fons"


def stretch(im, y0, y1, new_h):
    """Conserva dalt (0..y0) i baix (y1..H) i estira la banda central y0..y1 fins a que el total faça new_h."""
    w, h = im.size
    mid_h = new_h - y0 - (h - y1)
    out = Image.new(im.mode, (w, new_h))
    out.paste(im.crop((0, 0, w, y0)), (0, 0))
    out.paste(im.crop((0, y0, w, y1)).resize((w, mid_h), Image.LANCZOS), (0, y0))
    out.paste(im.crop((0, y1, w, h)), (0, y0 + mid_h))
    return out


# marc ornamental: 2048² → 2048×2560 (3:4)
im = Image.open(F / "marc-quadrat.jpg").convert("RGB")
stretch(im, 880, 1168, 2560).save(F / "marc-45.jpg", quality=92)

# cortina diagonal amb alfa: 1024² → 1024×1280; s'allarga el vellut inferior
c = Image.open(F / "cortina-diagonal.png").convert("RGBA")
stretch(c, 900, 1024, 1280).save(F / "cortina-45.png")
print("ok")
