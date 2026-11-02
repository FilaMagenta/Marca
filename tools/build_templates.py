#!/usr/bin/env python3
"""Genera les plantilles SVG de brand/templates/ i templates/INDEX.json.

Convenció dels camps (la llegeix render.py):
  <text id="field-X" data-box="x y w h" ...>   camp de text amb ajust automàtic
  <image id="field-foto" data-box="x y w h">    camp de foto (retall 'cover')
  data-if="camp"                                 l'element s'elimina si el camp no s'ha omplit
Executar:  python3 tools/build_templates.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "templates"
OUT.mkdir(exist_ok=True)

MAG, GOLD, GREEN, WHITE, GREY, VEL = "#7D1941", "#C69232", "#576437", "#F5F5F5", "#373C41", "#2A0614"
FONS = "../assets/fons/"


# ───────────────────────── peces reutilitzables ─────────────────────────
def _asset_inner(name, tag):
    """Contingut intern d'un SVG d'assets/ (net d'Inkscape), amb ids prefixats per evitar col·lisions."""
    s = (ROOT / "assets" / name).read_text()
    inner = s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    inner = re.sub(r"<defs[^>]*/>", "", inner)
    return re.sub(r'\bid="([^"]+)"', lambda m: f'id="{tag}-{m.group(1)}"', inner)


ESCUT_W, ESCUT_H = 195.2348, 266.72002   # viewBox d'assets/escut.svg


def escut(cx, top, h, tag="e"):
    """Escut vectorial centrat horitzontalment a cx, amb la vora superior a 'top' i alçada h."""
    sc = h / ESCUT_H
    x = cx - ESCUT_W / 2 * sc
    return (f'<g id="escut" transform="translate({x:.1f},{top}) scale({sc:.4f})">'
            f'{_asset_inner("escut.svg", tag)}</g>')


def escut_circ(x, y, d, tag="c"):
    return f'<g id="escut-circular" transform="translate({x},{y}) scale({d/512:.4f})">{_asset_inner("escut-circular.svg", tag)}</g>'


def text(fid, box, size, *, font="playfair", weight=400, fill=WHITE, align="middle", lh=1.14,
         tracking=0, caps=False, valign="middle", minsize=None, sample="", cond=None, extra="", keep=False):
    b = " ".join(str(v) for v in box)
    minsize = minsize or max(24, int(size * 0.45))
    return (f'<text id="field-{fid}" data-box="{b}" data-size="{size}" data-min="{minsize}" '
            f'data-font="{font}" data-weight="{weight}" data-fill="{fill}" data-align="{align}" '
            f'data-lh="{lh}" data-tracking="{tracking}" data-caps="{int(caps)}" data-valign="{valign}"'
            + (f' data-if="{cond}"' if cond else "") + (' data-keep="1"' if sample and not cond and (fid == "etiqueta" or keep) else "") + f' {extra}>{sample}</text>')


def photo(fid, box, clip=None, cond=None, gray=0):
    x, y, w, h = box
    c = f' clip-path="url(#{clip})"' if clip else ""
    ci = f' data-if="{cond}"' if cond else ""
    return (f'<image id="field-{fid}" data-box="{x} {y} {w} {h}" data-gray="{gray}" x="{x}" y="{y}" width="{w}" '
            f'height="{h}" preserveAspectRatio="xMidYMid slice"{c}{ci} href=""/>')


def hairline(x1, x2, y, op=1, cond=None):
    ci = f' data-if="{cond}"' if cond else ""
    return f'<path d="M{x1},{y}H{x2}" stroke="url(#gold)" stroke-width="2" opacity="{op}"{ci}/>'


def eyebrow(fid, cx, y, w, sample, size=26, cond=None, fill=GOLD):
    """Etiqueta tècnica: Lato Bold en majúscules amb tracking ample, flanquejada per filets."""
    box = (cx - w // 2, y, w, 40)
    return text(fid, box, size, font="lato", weight=700, fill=fill, tracking=7, caps=True,
                minsize=18, sample=sample, cond=cond)


def brackets(w, h, m=48, l=70, op=0.9):
    d = ""
    for (x, y, sx, sy) in [(m, m, 1, 1), (w - m, m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1)]:
        d += f"M{x},{y+sy*l}V{y}H{x+sx*l}"
    return f'<path d="{d}" fill="none" stroke="url(#gold)" stroke-width="3" opacity="{op}"/>'


DEFS = f"""<defs>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#E2B857"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="#A9761E"/>
    </linearGradient>
    <linearGradient id="fadeBottom" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#14030A" stop-opacity="0"/><stop offset=".55" stop-color="#14030A" stop-opacity=".78"/><stop offset="1" stop-color="#14030A" stop-opacity=".96"/>
    </linearGradient>
    <linearGradient id="fadeTop" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#14030A" stop-opacity="0"/><stop offset="1" stop-color="#14030A" stop-opacity=".7"/>
    </linearGradient>
    <radialGradient id="vinyeta" cx=".5" cy=".5" r=".75">
      <stop offset=".55" stop-color="{MAG}" stop-opacity="0"/><stop offset="1" stop-color="#1a0410" stop-opacity=".7"/>
    </radialGradient>
  </defs>"""


def svg(w, h, body, title, extra_defs=""):
    d = DEFS.replace("</defs>", extra_defs + "</defs>")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n  <title>{title}</title>\n  {d}\n{body}\n</svg>\n')


def bg(file, w, h):
    return f'<image id="fons" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="{FONS}{file}"/>'


INDEX = {}


def save(name, content, desc, uses, fields, fmt):
    (OUT / f"{name}.svg").write_text(content)
    INDEX[name] = {"descripcio": desc, "usar_per_a": uses, "format": fmt, "camps": fields}


S_W, S_H = 1080, 1920
P = 1080

# ───────────────────────── STORIES ─────────────────────────
# 1. Horaris  (dades en blocs: es dibuixen amb render.py, camp 'grups')
body = f"""{bg('story-cortines-marc.jpg', S_W, S_H)}
  {text('titol', (90, 330, 900, 330), 133, weight=700, lh=1.08, sample='Horaris\nMig Any')}
  <g id="field-grups" data-box="110 700 860 820" data-size="88" data-min="38" data-fill="{WHITE}" data-gold="{GOLD}"></g>
  {text('nota', (110, 1540, 860, 70), 34, font='lato', weight=700, fill=GOLD, tracking=3, caps=True, minsize=24, sample='', cond='nota')}"""
save("story-horaris", svg(S_W, S_H, body, "Story · Horaris"),
     "Horaris d'actes, diana, entradeta, arrancà, etc. Blocs de títol + files etiqueta/hora.",
     ["horaris d'una entradeta", "horaris del Mig Any", "programa d'un cap de setmana"],
     {"titol": "Títol de la story (\\n per a salt de línia). Ex.: 'Horaris\\nMig Any'",
      "grups": "[{'titol':'Diana Centenari','files':[['Arrancà','9:35'],['Carbonato','10:31']]}, ...] (màx. ~3 grups / 8 files)",
      "nota": "(opc.) Línia curta al peu en Lato: 'Recorregut per Sant Nicolau'"}, "story 1080×1920")

# 2. Anunci de text
body = f"""{bg('story-vellut.png', S_W, S_H)}
  {escut(540, 290, 230, 'a')}
  {eyebrow('etiqueta', 540, 565, 800, 'Filà Magenta · Alcoi')}
  {hairline(340, 740, 620, .8)}
  {text('titol', (90, 655, 900, 330), 118, weight=700, lh=1.08, sample='Titular\ndel missatge')}
  {text('text', (110, 990, 860, 460), 54, weight=400, lh=1.28, sample='Cos amb **noms propis** en negreta.', cond='text')}
  {text('dada', (90, 1470, 900, 70), 38, font='lato', weight=700, fill=GOLD, tracking=2, sample='', cond='dada')}"""
save("story-anunci", svg(S_W, S_H, body, "Story · Anunci de text"),
     "Anunci només de text sobre vellut amb escut: novetats, avisos, convocatòries, renovació de contractes.",
     ["hem renovat contracte amb la banda", "convocatòria", "avís", "recordatori"],
     {"etiqueta": "(opc.) Etiqueta tècnica en majúscules, per defecte 'Filà Magenta · Alcoi'",
      "titol": "Frase principal (2-4 línies). **negreta** per a noms. [[daurat]] per a paraules clau.",
      "text": "(opc.) Cos explicatiu", "dada": "(opc.) Data/hora/lloc destacat en Lato"}, "story 1080×1920")

# 3. Foto a sang amb titular
body = f"""<rect width="{S_W}" height="{S_H}" fill="{VEL}"/>
  {photo('foto', (0, 0, S_W, S_H))}
  <rect width="{S_W}" height="{S_H}" fill="url(#vinyeta)"/>
  <rect y="{S_H-1250}" width="{S_W}" height="1250" fill="url(#fadeBottom)"/>
  <rect width="{S_W}" height="420" fill="url(#fadeTop)"/>
  {escut_circ(64, 262, 150, 'f')}
  {brackets(S_W, S_H, 40, 60, .0)}
  {hairline(70, 330, 1250)}
  {eyebrow('etiqueta', 300, 1180, 600, 'Filà Magenta', cond='etiqueta')}
  {text('titol', (70, 1275, 940, 330), 104, weight=700, lh=1.1, align='start', valign='top', sample='Titular sobre la foto')}
  {text('subtitol', (70, 1610, 940, 120), 42, font='lato', weight=400, align='start', valign='top', lh=1.3, sample='', cond='subtitol')}"""
save("story-foto", svg(S_W, S_H, body, "Story · Foto a sang"),
     "Una fotografia vertical (o retallada) a pantalla completa amb titular a sota. Ràpida, per a el dia a dia.",
     ["foto d'un acte", "moment de l'entradeta", "agraïment amb foto"],
     {"foto": "Ruta a la fotografia", "titol": "Titular (1-3 línies)",
      "subtitol": "(opc.) Frase en Lato", "etiqueta": "(opc.) Etiqueta en majúscules"}, "story 1080×1920")


# 4/5. Persona (felicitació / nomenament)  i  dol
# arc: finestra de la foto, definida una sola vegada amb coordenades coherents
def persona_story(dol):
    fil = "#BDBDBD" if dol else GOLD
    arch = "M200,1030V720A340,340 0 0 1 880,720V1030Z"
    outer = "M178,1052V720A362,362 0 0 1 902,720V1052Z"
    ex = f'<clipPath id="arc"><path d="{arch}"/></clipPath>'
    label = "In memoriam" if dol else "Enhorabona"
    body = f"""{bg('story-vellut.png', S_W, S_H)}
  {'<rect width="1080" height="1920" fill="#06010A" opacity=".5"/>' if dol else ''}
  {eyebrow('etiqueta', 540, 300, 800, label, size=28, fill=('#D0D0D0' if dol else GOLD))}
  {photo('foto', (200, 380, 680, 650), clip='arc', gray=(1 if dol else 0))}
  <path d="{arch}" fill="none" stroke="{fil}" stroke-width="5"/>
  <path d="{outer}" fill="none" stroke="{fil}" stroke-width="2" opacity=".65"/>
  {text('nom', (80, 1110, 920, 230), 100, weight=700, lh=1.06, sample='Nom Cognom')}
  {text('dates', (90, 1350, 900, 60), 40, font='lato', weight=700, fill=('#D0D0D0' if dol else GOLD), tracking=4, sample='', cond='dates')}
  {hairline(340, 740, 1425, .7)}
  {text('text', (110, 1450, 860, 170), 46, weight=400, lh=1.28, sample='', cond='text')}"""
    return svg(S_W, S_H, body, "Story · " + ("Dol" if dol else "Persona"), ex)


save("story-persona", persona_story(False),
     "Felicitació, nomenament o reconeixement a una persona amb la seua foto en finestra d'arc.",
     ["felicitar algú", "nou càrrec", "aniversari", "anunci d'alferes/capità"],
     {"foto": "Foto de la persona (preferiblement retrat; es retalla)", "nom": "Nom i cognoms (2 línies màx.)",
      "text": "(opc.) Motiu: 'per la seua alferecia 2027'", "dates": "(opc.) Dada: 'Alferes 2027'",
      "etiqueta": "(opc.) Per defecte 'Enhorabona'"}, "story 1080×1920")
save("story-dol", persona_story(True),
     "Condol per defunció. Foto en blanc i negre, fons més fosc, to sobri (sense emojis ni exclamacions).",
     ["ha mort un company/a", "condol", "aniversari de la mort"],
     {"foto": "Foto de la persona", "nom": "Nom i cognoms", "dates": "(opc.) '1948 — 2026'",
      "text": "(opc.) Frase sobria: 'La Filà Magenta lamenta la seua pèrdua i acompanya la família'",
      "etiqueta": "(opc.) Per defecte 'In memoriam'"}, "story 1080×1920")

# ───────────────────────── POSTS (1080×1350, 4:5 = mínim d'Instagram; la graella retalla 34 px a cada costat) ─────────────────────────
PW, PH = 1080, 1350
FR = "marc-45.jpg"
FMT = "post 1080×1350 (4:5)"

body = f"""{bg(FR, PW, PH)}
  {escut(540, 34, 150, 'p1')}
  {text('text', (170, 285, 740, 740), 66, weight=400, lh=1.2, sample='Des de la **Filà Magenta** donem l\'enhorabona a **Nom Cognom**')}
  {text('dada', (140, 1075, 800, 60), 34, font='lato', weight=700, fill=GOLD, tracking=3, caps=True, sample='', cond='dada')}"""
save("post-anunci", svg(PW, PH, body, "Post · Anunci de text"),
     "Anunci només de text dins el marc ornamental: felicitacions, avisos, renovacions.",
     ["felicitar algú amb text", "avís", "renovació de la banda"],
     {"text": "Frase completa; **negreta** per a noms propis i [[daurat]] per a paraules clau",
      "dada": "(opc.) Data o lloc en Lato (majúscules)"}, FMT)

body = f"""{bg(FR, PW, PH)}
  {escut(540, 34, 150, 'p2')}
  {text('titol', (170, 285, 740, 280), 96, weight=700, fill=GOLD, lh=1.06, sample='Titular')}
  {hairline(340, 740, 590, .8)}
  {text('text', (170, 620, 740, 430), 52, weight=400, lh=1.25, sample='Cos del missatge amb **noms**.')}
  {text('dada', (140, 1075, 800, 56), 32, font='lato', weight=700, fill=GOLD, tracking=3, caps=True, sample='', cond='dada')}"""
save("post-anunci-titol", svg(PW, PH, body, "Post · Anunci amb titular"),
     "Anunci amb titular daurat i cos. Per a missatges amb més informació (assemblea, sopar, cartells).",
     ["convocatòria d'assemblea", "novetat", "tancament de carrusel (agraïment)"],
     {"titol": "Titular daurat (1-2 línies)", "text": "Cos", "dada": "(opc.) Data/lloc"}, FMT)

body = f"""{bg(FR, PW, PH)}
  {escut(540, 300, 290, 'p3')}
  {text('titol', (120, 650, 840, 340), 128, weight=700, caps=True, lh=1.04, tracking=3, sample='COMUNICAT\nOFICIAL', keep=True)}
  {text('subtitol', (140, 1005, 800, 50), 28, font='lato', weight=700, fill=GOLD, tracking=6, caps=True, sample='', cond='subtitol')}"""
save("post-comunicat", svg(PW, PH, body, "Post · Comunicat oficial"),
     "Portada simètrica i solemne per a comunicats oficials. El text complet va al peu de foto o a un 2n slide.",
     ["comunicat oficial", "nota de premsa", "decisió de junta"],
     {"titol": "Per defecte 'COMUNICAT\\nOFICIAL'", "subtitol": "(opc.) Data o assumpte en Lato"}, FMT)

body = f"""<rect width="{PW}" height="{PH}" fill="{VEL}"/>
  {photo('foto', (0, 0, PW, PH))}
  <rect width="{PW}" height="{PH}" fill="url(#vinyeta)"/>
  <rect y="{PH-760}" width="{PW}" height="760" fill="url(#fadeBottom)"/>
  {escut_circ(54, 54, 130, 'pf')}
  <rect x="28" y="28" width="{PW-56}" height="{PH-56}" fill="none" stroke="url(#gold)" stroke-width="2" opacity=".85"/>
  {hairline(70, 250, 960)}
  {text('titol', (70, 980, 940, 210), 96, weight=700, align='start', valign='top', lh=1.08, sample='Titular sobre la foto')}
  {text('subtitol', (70, 1205, 940, 90), 40, font='lato', weight=400, align='start', valign='top', sample='', cond='subtitol')}"""
save("post-foto", svg(PW, PH, body, "Post · Foto amb titular"),
     "Una sola fotografia a sang amb titular. Per a anunci amb foto o resum d'un acte en una imatge.",
     ["anunci amb una foto", "foto destacada d'un acte"],
     {"foto": "Fotografia", "titol": "Titular (1-2 línies)", "subtitol": "(opc.) Línia en Lato"}, FMT)


def persona_post(dol):
    fil = "#BDBDBD" if dol else GOLD
    ex = '<clipPath id="ov"><ellipse cx="540" cy="520" rx="205" ry="270"/></clipPath>'
    body = f"""{bg(FR, PW, PH)}
  {'<rect width="1080" height="1350" fill="#06010A" opacity=".5"/>' if dol else ''}
  {photo('foto', (335, 250, 410, 540), clip='ov', gray=(1 if dol else 0))}
  <ellipse cx="540" cy="520" rx="205" ry="270" fill="none" stroke="{fil}" stroke-width="4"/>
  <ellipse cx="540" cy="520" rx="223" ry="288" fill="none" stroke="{fil}" stroke-width="1.5" opacity=".6"/>
  {eyebrow('etiqueta', 540, 828, 600, 'In memoriam' if dol else 'Enhorabona', size=26, fill=('#D0D0D0' if dol else GOLD))}
  {text('nom', (140, 872, 800, 100), 80, weight=700, lh=1.05, sample='Nom Cognom')}
  {text('text', (170, 985, 740, 100), 36, weight=400, lh=1.22, sample='', cond='text')}"""
    return svg(PW, PH, body, "Post · " + ("Dol" if dol else "Persona"), ex)


save("post-persona", persona_post(False),
     "Felicitació o reconeixement a una persona, amb foto en finestra ovalada.",
     ["felicitar algú", "nou càrrec", "aniversari"],
     {"foto": "Retrat", "nom": "Nom i cognoms", "text": "(opc.) Motiu breu", "etiqueta": "(opc.) 'Enhorabona'"}, FMT)
save("post-dol", persona_post(True),
     "Condol per defunció (post). Foto en B/N, to sobri.",
     ["ha mort un company/a", "condol"],
     {"foto": "Retrat", "nom": "Nom i cognoms", "text": "(opc.) Frase sobria breu", "etiqueta": "(opc.) 'In memoriam'"}, FMT)

# Carrusel: portada (la cortina inferior s'allarga amb cortina-45.png)
body = f"""<rect width="{PW}" height="{PH}" fill="{VEL}"/>
  {photo('foto', (300, 0, 780, 660))}
  <image id="cortina" x="0" y="0" width="{PW}" height="{PH}" preserveAspectRatio="none" href="{FONS}cortina-45.png"/>
  {escut_circ(68, 57, 253, 'cp')}
  {text('titol1', (30, 935, 1020, 130), 126, weight=700, caps=True, align='start', valign='bottom', lh=1, sample='TITOL')}
  {text('titol2', (30, 1060, 1020, 130), 126, weight=700, caps=True, fill=GOLD, align='start', valign='bottom', lh=1, sample='DESTACAT', cond='titol2')}
  {text('subtitol', (40, 1200, 760, 110), 44, weight=400, align='start', valign='top', lh=1.2, sample='Subtítol breu')}
  <g id="continua" data-if="continua"><text id="label-continua" x="990" y="1275" text-anchor="end" font-family="Playfair Display" font-size="36" fill="{GOLD}">Continua</text>
  <path d="M1006,1267H1046M1030,1251L1046,1267L1030,1283" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>"""
save("carrusel-portada", svg(PW, PH, body, "Carrusel · Portada"),
     "Portada de carrusel: foto a la finestra de la cortina, titular blanc + daurat, subtítol i 'Continua →'.",
     ["portada de fotos d'un acte", "resum d'una activitat"],
     {"foto": "Foto de portada (zona visible: part superior dreta)", "titol1": "Primera línia (blanc, majúscules)",
      "titol2": "(opc.) Segona línia (daurat)", "subtitol": "Frase curta. **negreta** per a noms",
      "continua": "true/false: mostra 'Continua →' (per defecte true)"}, FMT)

body = f"""<rect width="{PW}" height="{PH}" fill="{VEL}"/>
  {photo('foto', (0, 0, PW, PH))}
  <rect y="{PH-340}" width="{PW}" height="340" fill="url(#fadeBottom)" data-if="peu"/>
  {escut_circ(40, 40, 96, 'ci')}
  {text('peu', (60, 1110, 760, 130), 38, weight=400, align='start', valign='bottom', lh=1.22, sample='', cond='peu')}
  <g data-if="pagina"><rect x="880" y="1250" width="160" height="56" rx="28" fill="#14030A" fill-opacity=".6" stroke="url(#gold)" stroke-width="2"/></g>
  {text('pagina', (880, 1250, 160, 56), 28, font='lato', weight=700, fill=GOLD, tracking=3, minsize=20, sample='02 / 08', cond='pagina')}"""
save("carrusel-interior", svg(PW, PH, body, "Carrusel · Foto interior"),
     "Foto a sang per als slides interiors del carrusel, amb escut petit i comptador opcional.",
     ["resta de fotos del carrusel"],
     {"foto": "Fotografia", "peu": "(opc.) Peu breu", "pagina": "(opc.) '02 / 08'"}, FMT)

# Carrusel: interior apaïsat (foto 4:3 sencera a tota l'amplada sobre vellut; el llenç continua en 4:5)
body = f"""<rect width="{PW}" height="{PH}" fill="{VEL}"/>
  {photo('foto', (0, 270, PW, 810))}
  <rect y="268" width="{PW}" height="3" fill="url(#gold)"/><rect y="1079" width="{PW}" height="3" fill="url(#gold)"/>
  {escut_circ(40, 40, 96, 'ia')}
  {text('peu', (60, 1115, 760, 150), 38, weight=400, align='start', valign='top', lh=1.22, sample='', cond='peu')}
  <g data-if="pagina"><rect x="880" y="1250" width="160" height="56" rx="28" fill="#14030A" fill-opacity=".6" stroke="url(#gold)" stroke-width="2"/></g>
  {text('pagina', (880, 1250, 160, 56), 28, font='lato', weight=700, fill=GOLD, tracking=3, minsize=20, sample='02 / 08', cond='pagina')}"""
save("carrusel-interior-apaisat", svg(PW, PH, body, "Carrusel · Foto interior apaïsada"),
     "Foto apaïsada (4:3) sencera a tota l'amplada, centrada sobre vellut. El llenç segueix sent 4:5 perquè Instagram fixa la proporció del carrusel amb la primera imatge.",
     ["foto horitzontal d'un carrusel (grups, files)"],
     {"foto": "Fotografia apaïsada", "peu": "(opc.) Peu breu", "pagina": "(opc.) '02 / 08'"}, FMT)

# ───────────────────────── VÍDEO (capes amb transparència) ─────────────────────────
body = f"""<rect x="0" y="{820}" width="1920" height="260" fill="url(#fadeBottom)" opacity=".85"/>
  <rect x="96" y="896" width="6" height="108" fill="url(#gold)"/>
  {text('nom', (126, 880, 1100, 80), 64, weight=700, align='start', valign='middle', lh=1, sample='Nom Cognom')}
  {text('carrec', (126, 962, 1100, 44), 28, font='lato', weight=700, fill=GOLD, align='start', tracking=6, caps=True, minsize=20, sample='Càrrec', cond='carrec')}
  {escut_circ(1700, 884, 120, 'v1')}"""
save("video-lower-third", svg(1920, 1080, body, "Vídeo · Lower third"),
     "Capa transparent 1920×1080 (PNG amb alfa) amb nom i càrrec sobre un vídeo.",
     ["identificar qui parla al vídeo"], {"nom": "Nom", "carrec": "(opc.) Càrrec o rol"}, "vídeo 1920×1080 alfa")

body = f"""<rect y="{S_H-900}" width="{S_W}" height="900" fill="url(#fadeBottom)"/>
  {escut_circ(64, 262, 130, 'v2')}
  {hairline(70, 330, 1300)}
  {eyebrow('etiqueta', 300, 1230, 600, 'Filà Magenta', cond='etiqueta')}
  {text('titol', (70, 1325, 940, 280), 100, weight=700, align='start', valign='top', lh=1.08, sample='Títol del vídeo')}
  {text('subtitol', (70, 1610, 940, 80), 40, font='lato', align='start', valign='top', sample='', cond='subtitol')}"""
save("video-titol", svg(S_W, S_H, body, "Vídeo · Targeta de títol"),
     "Capa transparent vertical 1080×1920 amb títol i escut per a obrir un vídeo/reel (respecta zones segures).",
     ["títol d'inici de reel", "tancament amb data"],
     {"titol": "Títol", "subtitol": "(opc.)", "etiqueta": "(opc.)"}, "vídeo 1080×1920 alfa")

(OUT / "INDEX.json").write_text(json.dumps(INDEX, ensure_ascii=False, indent=1))
print("ok", len(INDEX), "plantilles")
