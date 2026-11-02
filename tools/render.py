#!/usr/bin/env python3
"""Omple una plantilla de brand/templates/ amb text i fotos i l'exporta a PNG.

Ús:
  python3 tools/render.py tools/examples/story-dol.json            # → out/story-dol.png
  python3 tools/render.py --json '{"plantilla":"post-anunci","text":"Hola **món**"}' -o out/x.png
  python3 tools/render.py --list                                    # plantilles i camps
  python3 tools/render.py --install-fonts                           # instal·la Playfair + Lato (usuari)

El JSON porta "plantilla" i els camps de la plantilla (vegeu templates/INDEX.json).
Marcat de text:  **negreta**   [[daurat]]   \\n = salt de línia.
Fotos: "foto": "ruta.jpg" (+ opcional "foto_focus": [0.5, 0.35] = punt d'interès x,y de 0 a 1).
Requereix: Python 3 + Pillow, Inkscape (CLI) i les fonts instal·lades.
"""
import argparse
import base64
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageFont, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates"
FONTDIR = ROOT / "assets" / "fonts"
GOLD = "#C69232"
SVG, XLINK = "http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)

FONT_FILES = {
    ("playfair", 400): FONTDIR / "Playfair_Display/static/PlayfairDisplay-Regular.ttf",
    ("playfair", 700): FONTDIR / "Playfair_Display/static/PlayfairDisplay-Bold.ttf",
    ("playfair", 900): FONTDIR / "Playfair_Display/static/PlayfairDisplay-Black.ttf",
    ("lato", 400): FONTDIR / "Lato/Lato-Regular.ttf",
    ("lato", 700): FONTDIR / "Lato/Lato-Bold.ttf",
    ("lato", 900): FONTDIR / "Lato/Lato-Black.ttf",
}
FAMILY = {"playfair": "Playfair Display", "lato": "Lato"}
_cache = {}


def pil_font(fam, weight, size):
    key = (fam, weight, int(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(FONT_FILES[(fam, weight)]), int(size))
    return _cache[key]


def tag(el):
    return el.tag.split("}")[-1]


# ───────────────────────── text ─────────────────────────
def parse_runs(s):
    """'**a** [[b]]' → [(text, bold, gold)] conservant espais."""
    runs, bold, gold, buf = [], False, False, ""
    i = 0
    while i < len(s):
        if s.startswith("**", i):
            if buf: runs.append((buf, bold, gold)); buf = ""
            bold = not bold; i += 2
        elif s.startswith("[[", i):
            if buf: runs.append((buf, bold, gold)); buf = ""
            gold = True; i += 2
        elif s.startswith("]]", i):
            if buf: runs.append((buf, bold, gold)); buf = ""
            gold = False; i += 2
        else:
            buf += s[i]; i += 1
    if buf: runs.append((buf, bold, gold))
    return runs


def words_of(line, caps):
    """Llista de paraules [txt, bold, gold, glue]; glue=True si va enganxada a l'anterior (canvi de format sense espai)."""
    out = []
    prev_end_space = True
    for txt, b, g in parse_runs(line):
        if caps: txt = txt.upper()
        toks = re.findall(r"\s+|\S+", txt)
        for k, tk in enumerate(toks):
            if tk.isspace():
                prev_end_space = True
                continue
            out.append([tk, b, g, not prev_end_space and bool(out)])
            prev_end_space = False
    return out


def bw_for(base, bold):
    return {400: 700, 700: 900, 900: 900}[base] if bold else base


def measure(txt, fam, weight, size, tracking):
    return pil_font(fam, weight, size).getlength(txt) + tracking * len(txt)


def wrap(lines, fam, base, size, tracking, width, caps):
    out = []
    for raw in lines:
        words = words_of(raw, caps)
        cur, cw = [], 0.0
        space = lambda b: measure(" ", fam, bw_for(base, b), size, tracking)
        for w in words:
            ww = measure(w[0], fam, bw_for(base, w[1]), size, tracking)
            add = ww + (0 if (not cur or w[3]) else space(w[1]))
            if cur and cw + add > width:
                out.append(cur); cur, cw = [[w[0], w[1], w[2], False]], ww
            else:
                cur.append(w); cw += add
        out.append(cur)
    return out


def line_width(line, fam, base, size, tracking):
    t = 0.0
    for i, (w, b, g, glue) in enumerate(line):
        t += measure(w, fam, bw_for(base, b), size, tracking)
        if i and not glue: t += measure(" ", fam, bw_for(base, b), size, tracking)
    return t


def layout_text(el, value):
    a = el.attrib
    bx, by, bwid, bh = [float(v) for v in a["data-box"].split()]
    fam, base = a["data-font"], int(a["data-weight"])
    size_max, size_min = float(a["data-size"]), float(a["data-min"])
    lh, tr = float(a["data-lh"]), float(a["data-tracking"])
    caps, valign, align = a["data-caps"] == "1", a["data-valign"], a["data-align"]
    fill = a["data-fill"]
    raw = value.replace("\\n", "\n").split("\n")
    size, lines = size_max, None
    while size >= size_min:
        lines = wrap(raw, fam, base, size, tr, bwid, caps)
        widest = max(line_width(l, fam, base, size, tr) for l in lines)
        if len(lines) * size * lh <= bh and widest <= bwid + 0.5:
            break
        size -= 2
    else:
        size = size_min
        lines = wrap(raw, fam, base, size, tr, bwid, caps)
        print(f"  ⚠ el camp {el.get('id')} no cap bé ni a mida mínima ({size_min:.0f}px): acurça el text", file=sys.stderr)
    block = len(lines) * size * lh
    top = {"top": by, "middle": by + (bh - block) / 2, "bottom": by + bh - block}[valign]
    x = {"start": bx, "middle": bx + bwid / 2, "end": bx + bwid}[align]
    for c in list(el): el.remove(c)
    el.text = None
    el.set("font-family", FAMILY[fam]); el.set("font-weight", str(base)); el.set("font-size", f"{size:.1f}")
    el.set("fill", fill); el.set("text-anchor", align); el.set("letter-spacing", f"{tr}")
    el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for k in [k for k in a if k.startswith("data-")]: del el.attrib[k]
    for i, line in enumerate(lines):
        y = top + (i + .5) * size * lh + .33 * size
        ts = ET.SubElement(el, f"{{{SVG}}}tspan", {"x": f"{x:.1f}", "y": f"{y:.1f}"})
        for j, (w, b, g, glue) in enumerate(line):
            r = ET.SubElement(ts, f"{{{SVG}}}tspan")
            nxt_glue = j < len(line) - 1 and line[j + 1][3]
            r.text = w + (" " if j < len(line) - 1 and not nxt_glue else "")
            if b: r.set("font-weight", str(bw_for(base, True)))
            if g: r.set("fill", GOLD)


# ───────────────────────── fotos ─────────────────────────
def photo_uri(path, w, h, focus, gray, zoom=1.0):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    sc = max(w / im.width, h / im.height) * zoom
    nw, nh = int(im.width * sc + .5), int(im.height * sc + .5)
    im = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    left = min(max(int(fx * nw - w / 2), 0), nw - w)
    top = min(max(int(fy * nh - h / 2), 0), nh - h)
    im = im.crop((left, top, left + w, top + h))
    if gray:
        im = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1).convert("RGB")
        im = ImageEnhance.Brightness(im).enhance(.92)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ───────────────────────── horaris ─────────────────────────
def build_grups(g, grups):
    bx, by, bw, bh = [float(v) for v in g.get("data-box").split()]
    smax, smin = float(g.get("data-size")), float(g.get("data-min"))
    fill, gold = g.get("data-fill"), g.get("data-gold")
    LH, GAP = 1.2, .6
    n_lines = sum(1 + len(x.get("files", [])) if x.get("titol") else len(x.get("files", [])) for x in grups)
    n_gaps = max(len(grups) - 1, 0)

    def fits(s):
        if n_lines * LH * s + n_gaps * GAP * s > bh: return False
        for x in grups:
            for lab, hr in x.get("files", []):
                if measure(lab + ":", "playfair", 400, s, 0) + measure(str(hr), "playfair", 700, s, 0) + 70 > bw: return False
        return True
    s = smax
    while s > smin and not fits(s): s -= 2
    used = n_lines * LH * s + n_gaps * GAP * s
    y = by + (bh - used) / 2 if used < bh else by
    for k in list(g): g.remove(k)

    def t(txt, x, y, weight, color, anchor="start"):
        e = ET.SubElement(g, f"{{{SVG}}}text", {"x": f"{x:.1f}", "y": f"{y:.1f}", "font-family": "Playfair Display",
                                                "font-weight": str(weight), "font-size": f"{s:.1f}", "fill": color, "text-anchor": anchor})
        e.text = txt
    for gi, x in enumerate(grups):
        if gi: y += GAP * s
        if x.get("titol"):
            t(x["titol"] + ":", bx, y + LH * s * .5 + .33 * s, 700, fill); y += LH * s
        for lab, hr in x.get("files", []):
            base = y + LH * s * .5 + .33 * s
            t(lab + ":", bx, base, 400, fill)
            t(str(hr), bx + bw, base, 700, gold, "end")
            lw = measure(lab + ":", "playfair", 400, s, 0); hw = measure(str(hr), "playfair", 700, s, 0)
            if bw - lw - hw > 120:
                ET.SubElement(g, f"{{{SVG}}}path", {"d": f"M{bx+lw+24:.1f},{base-.12*s:.1f}H{bx+bw-hw-24:.1f}", "stroke": gold,
                                                    "stroke-width": "2", "stroke-dasharray": "2 9", "stroke-linecap": "round", "opacity": ".55"})
            y += LH * s
    for k in [k for k in g.attrib if k.startswith("data-")]: del g.attrib[k]


# ───────────────────────── render ─────────────────────────
def fix_hrefs(root, base):
    for el in root.iter():
        for k in ("href", f"{{{XLINK}}}href"):
            v = el.get(k)
            if v and not v.startswith(("data:", "/", "file:")) and v != "":
                el.set(k, str((base / v).resolve()))


def fill_template(data):
    name = data["plantilla"]
    f = TPL / f"{name}.svg"
    if not f.exists():
        sys.exit(f"Plantilla inexistent: {name}. Disponibles: {', '.join(sorted(p.stem for p in TPL.glob('*.svg')))}")
    tree = ET.parse(f)
    root = tree.getroot()
    fix_hrefs(root, TPL)
    present = {k for k, v in data.items() if v not in (None, "", [], False)}
    if data.get("continua", True) is not False: present.add("continua")
    parent = {c: p for p in root.iter() for c in p}
    kill = []
    for el in root.iter():
        cond = el.get("data-if")
        if cond is not None:
            if cond not in present: kill.append(el)
            else: del el.attrib["data-if"]
    for el in kill:
        parent[el].remove(el)
    for el in list(root.iter()):
        eid = el.get("id", "")
        if not eid.startswith("field-"): continue
        key = eid[6:]
        if key not in present and el.get("data-keep") == "1" and tag(el) == "text":
            data = {**data, key: el.text}; present.add(key)
        if key not in present:
            if el in parent and parent[el] is not None and el.get("data-box"):
                try: parent[el].remove(el)
                except ValueError: pass
            if key not in ("nota",): print(f"  · camp '{key}' buit → s'omet", file=sys.stderr)
            continue
        if tag(el) == "text":
            layout_text(el, str(data[key]))
        elif tag(el) == "image":
            x, y, w, h = [int(float(v)) for v in el.get("data-box").split()]
            p = Path(data[key]).expanduser()
            if not p.is_absolute():
                p = next((c for c in (Path.cwd() / p, Path(data.get("_base", ".")) / p, ROOT / p) if c.exists()), Path.cwd() / p)
            if not p.exists(): sys.exit(f"No trobe la foto: {p}")
            uri = photo_uri(p, w, h, data.get(key + "_focus", [.5, .4]), el.get("data-gray") == "1", float(data.get(key + "_zoom", 1)))
            el.set("href", uri); el.set(f"{{{XLINK}}}href", uri)
            for k in [k for k in el.attrib if k.startswith("data-")]: del el.attrib[k]
        elif tag(el) == "g":
            build_grups(el, data[key])
    # elements que depenen de camps de foto no omplits (res més a fer): foto absent → fons en color ja present
    return tree


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json", nargs="?")
    ap.add_argument("--json", dest="json_inline")
    ap.add_argument("-o", "--out")
    ap.add_argument("--svg", action="store_true", help="només escriu l'SVG omplit")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--install-fonts", action="store_true")
    ap.add_argument("--scale", type=float, default=1.0, help="factor de mida (2 = doble resolució)")
    a = ap.parse_args()
    if a.list:
        idx = json.loads((TPL / "INDEX.json").read_text())
        for n, d in idx.items():
            print(f"\n{n}  [{d['format']}]\n  {d['descripcio']}")
            for k, v in d["camps"].items(): print(f"    - {k}: {v}")
        return
    if a.install_fonts:
        dst = Path.home() / ".local/share/fonts/FilaMagenta"; dst.mkdir(parents=True, exist_ok=True)
        for p in FONT_FILES.values(): shutil.copy(p, dst)
        subprocess.run(["fc-cache", "-f"]); print("Fonts instal·lades a", dst); return
    if not (a.json or a.json_inline): ap.error("cal un JSON")
    data = json.loads(a.json_inline) if a.json_inline else json.loads(Path(a.json).read_text())
    if a.json: data["_base"] = str(Path(a.json).resolve().parent)
    tree = fill_template(data)
    out = Path(a.out) if a.out else ROOT / "out" / f"{data.get('sortida', data['plantilla'])}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    svgp = out.with_suffix(".svg") if a.svg else Path(tempfile.mkdtemp()) / "r.svg"
    tree.write(svgp, encoding="utf-8", xml_declaration=True)
    if a.svg: print(svgp); return
    r = subprocess.run(["fc-list", "Playfair Display"], capture_output=True, text=True)
    if not r.stdout.strip(): print("⚠ Playfair Display no instal·lada: executa --install-fonts", file=sys.stderr)
    root = tree.getroot(); W = float(root.get("width"));
    cmd = ["inkscape", str(svgp), "-o", str(out), "-w", str(int(W * a.scale))]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode: sys.exit(res.stderr)
    print(out)


if __name__ == "__main__":
    main()
