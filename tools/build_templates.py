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

MAG, GOLD, GREEN, WHITE, GREY = "#7D1941", "#C69232", "#576437", "#F5F5F5", "#373C41"
# Derivats del disseny «Paper i fil» (no són de paleta: tons per a text/fons sobre paper clar)
PAPER, INK, ACC, GOLD_T = "#F3EBDD", "#3A1427", "#A91F5C", "#B08628"

THEMES = {   # fons, tinta (cos), titular, accent (paraula clau / cursiva), etiqueta, color de filets
    "clar":    dict(bg="clar",    ink=INK,       title=MAG,       acc=ACC,       label=GOLD_T,   line=GOLD,      eye=ACC),
    "magenta": dict(bg="magenta", ink="#F5F5F5", title="#F5F5F5", acc="#E8C77D", label="#E8C77D", line="#D9B25F", eye="#E8C77D"),
    "dol":     dict(bg="dol",     ink="#2F2B2D", title="#2F2B2D", acc="#6E686A", label="#8A8587", line="#A8A29E", eye="#6E686A"),
}
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


def text(fid, box, size, *, th="clar", font="playfair", weight=400, fill=None, align="middle", lh=1.14,
         tracking=0, caps=False, valign="middle", minsize=None, sample="", cond=None, extra="", keep=False, accent=None):
    T = THEMES[th]
    fill = fill or T["ink"]
    accent = accent or T["acc"]
    b = " ".join(str(v) for v in box)
    minsize = minsize or max(24, int(size * 0.45))
    return (f'<text id="field-{fid}" data-box="{b}" data-size="{size}" data-min="{minsize}" '
            f'data-font="{font}" data-weight="{weight}" data-fill="{fill}" data-accent="{accent}" data-align="{align}" '
            f'data-lh="{lh}" data-tracking="{tracking}" data-caps="{int(caps)}" data-valign="{valign}"'
            + (f' data-if="{cond}"' if cond else "") + (' data-keep="1"' if sample and not cond and (fid == "etiqueta" or keep) else "") + f' {extra}>{sample}</text>')


def photo(fid, box, clip=None, cond=None, gray=0):
    x, y, w, h = box
    c = f' clip-path="url(#{clip})"' if clip else ""
    ci = f' data-if="{cond}"' if cond else ""
    return (f'<image id="field-{fid}" data-box="{x} {y} {w} {h}" data-gray="{gray}" x="{x}" y="{y}" width="{w}" '
            f'height="{h}" preserveAspectRatio="xMidYMid slice"{c}{ci} href=""/>')


def hairline(x1, x2, y, th="clar", op=1, cond=None, w=2):
    ci = f' data-if="{cond}"' if cond else ""
    return f'<path d="M{x1},{y}H{x2}" stroke="{THEMES[th]["line"]}" stroke-width="{w}" opacity="{op}"{ci}/>'


def star(cx, cy, r, fill):
    """Estrella de quatre puntes (la del filet i la passamaneria)."""
    k = r * .22
    return (f'<path d="M{cx},{cy-r}L{cx+k:.1f},{cy-k:.1f}L{cx+r},{cy}L{cx+k:.1f},{cy+k:.1f}L{cx},{cy+r}'
            f'L{cx-k:.1f},{cy+k:.1f}L{cx-r},{cy}L{cx-k:.1f},{cy-k:.1f}Z" fill="{fill}"/>')


def orn(cx, y, w=360, th="clar", r=11):
    """Filet — estrella — filet (separador i capçalera)."""
    c = THEMES[th]["line"]
    return (f'<path d="M{cx-w/2},{y}H{cx-r*2.2}M{cx+r*2.2},{y}H{cx+w/2}" stroke="{c}" stroke-width="2"/>'
            + star(cx, y, r, c))


def eyebrow(fid, cx, y, w, sample, size=26, cond=None, th="clar", fill=None):
    """Etiqueta tècnica: Lato Bold en majúscules amb tracking ample."""
    box = (cx - w // 2, y, w, 40)
    return text(fid, box, size, th=th, font="lato", weight=700, fill=fill or THEMES[th]["eye"], tracking=7, caps=True,
                minsize=18, sample=sample, cond=cond)


def frame(w, h, th="clar", m=40, gap=18, stars=True):
    """Doble filet i cordó de passamaneria: el marc del cartell (fil daurat cosit sobre el paper)."""
    c = THEMES[th]["line"]
    o = f'<rect x="{m}" y="{m}" width="{w-2*m}" height="{h-2*m}" fill="none" stroke="{c}" stroke-width="4" opacity=".95"/>'
    # fil trenat: puntets clars sobre el cordó, com els tors d'una passamaneria
    o += (f'<rect x="{m}" y="{m}" width="{w-2*m}" height="{h-2*m}" fill="none" stroke="#FFF6DC" stroke-width="2" '
          f'stroke-dasharray="1.5 6" opacity=".55"/>')
    n = m + gap
    o += f'<rect x="{n}" y="{n}" width="{w-2*n}" height="{h-2*n}" fill="none" stroke="{c}" stroke-width="1.5" opacity=".7"/>'
    if stars:
        for (x, y) in [(n, n), (w - n, n), (n, h - n), (w - n, h - n)]:
            o += star(x, y, 9, c)
    return f'<g id="marc">{o}</g>'


def llac(cx, cy, k=1.0):
    """Llaç negre de dol (assets/llac-negre.svg). Alçada ≈ 117·k px, centrat a (cx, cy+10·k)."""
    import xml.etree.ElementTree as ET
    NS = "{http://www.w3.org/2000/svg}"
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    root = ET.parse(ROOT / "assets" / "llac-negre.svg").getroot()
    keep = []
    for el in root.iter():
        if el.tag in (NS + "linearGradient", NS + "radialGradient", NS + "path"):
            keep.append(el)
    # els degradats van dins de defs; els camins (hereten transform del grup layer1)
    defs = "".join(ET.tostring(e, encoding="unicode") for e in keep if e.tag != NS + "path")
    layer = next(e for e in root.iter(NS + "g"))
    tr = layer.get("transform", "")
    paths = "".join(ET.tostring(e, encoding="unicode") for e in layer.iter(NS + "path"))
    inner = f"<defs>{defs}</defs><g transform=\"{tr}\">{paths}</g>"
    inner = re.sub(r'\sxmlns(:\w+)?="[^"]*"', "", inner)
    inner = re.sub(r"<(/?)ns\d+:", r"<\1", inner)
    inner = re.sub(r'\sns\d*:[\w-]+="[^"]*"', "", inner)
    inner = re.sub(r'\s(?:sodipodi|inkscape|ns\d*):[\w-]+="[^"]*"', "", inner)
    inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="ll-{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", r"url(#ll-\1)", inner)
    VW, VH = 373.14, 409.41
    h = 117 * k; sc = h / VH
    return f'<g id="llac" transform="translate({cx - VW*sc/2:.1f},{cy + 10*k - h/2:.1f}) scale({sc:.4f})">{inner}</g>'


def footer(cx, y, th="clar", cond=None):
    c = THEMES[th]
    return text("peu_marca", (cx - 400, y, 800, 34), 22, th=th, font="lato", weight=700, fill=c["label"], tracking=6, caps=True,
                minsize=16, sample="Filà Magenta · Alcoi · Des de 1865", keep=True)


def bgimg(th, w, h):
    kind = "story" if (w, h) == (1080, 1920) else ("video" if w > h else "post")
    return f'<image id="fons" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" href="{FONS}{THEMES[th]["bg"]}-{kind}.jpg"/>'


DEFS = """<defs>
    <filter id="ombra" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#3A1427" flood-opacity=".22"/></filter>
  </defs>"""


def svg(w, h, body, title, extra_defs=""):
    d = DEFS.replace("</defs>", extra_defs + "</defs>")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n  <title>{title}</title>\n  {d}\n{body}\n</svg>\n')


def seal(x, y, d, tag, th="clar"):
    """Escut circular com un segell: anell de paper amb ombra (sense filet daurat, per no competir amb el vora de la foto)."""
    r = d / 2
    return (f'<circle cx="{x+r}" cy="{y+r}" r="{r+10}" fill="{PAPER}" filter="url(#ombra)"/>'
            + escut_circ(x, y, d, tag))


def card(x, y, w, h, op=.96):
    """Targeta de paper amb ombra suau (rectangles apilats; evita filtres amb opacitat)."""
    sh = "".join(f'<rect x="{x-d}" y="{y-d+8}" width="{w+2*d}" height="{h+2*d}" fill="#3A1427" opacity="{.07 - d*.006:.3f}"/>' for d in (0, 3, 6, 9))
    return sh + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PAPER}" opacity="{op}"/>'


INDEX = {}


def save(name, content, desc, uses, fields, fmt):
    (OUT / f"{name}.svg").write_text(content)
    INDEX[name] = {"descripcio": desc, "usar_per_a": uses, "format": fmt, "camps": fields}


S_W, S_H = 1080, 1920
P = 1080

# ───────────────────────── STORIES ─────────────────────────
# 1. Horaris  (dades en blocs: es dibuixen amb render.py, camp 'grups')
T = THEMES["clar"]
body = f"""{bgimg('clar', S_W, S_H)}
  {frame(S_W, S_H)}
  {orn(540, 292, 380)}
  {text('data', (90, 322, 900, 40), 28, font='lato', weight=700, fill=T['eye'], tracking=7, caps=True, minsize=18, sample='', cond='data')}
  {text('titol', (90, 410, 900, 190), 168, fill=MAG, lh=1.0, sample='Mig {{Any}}')}
  {text('subtitol', (90, 610, 900, 70), 46, fill=INK, sample='', cond='subtitol', extra='font-style="italic"')}
  <g id="field-grups" data-box="120 750 840 780" data-size="74" data-min="34" data-fill="{INK}" data-accent="{ACC}" data-tab="{MAG}" data-tabink="{WHITE}" data-rule="{GOLD}"></g>
  {text('nota', (110, 1480, 860, 50), 28, font='lato', weight=700, fill=GOLD_T, tracking=5, caps=True, minsize=20, sample='', cond='nota')}
  {orn(540, 1545, 120, r=9)}"""
save("story-horaris", svg(S_W, S_H, body, "Story · Horaris"),
     "Horaris d'actes (diana, entradeta, Mig Any…) sobre paper clar. Blocs amb pestanya + files hora / acte.",
     ["horaris d'una entradeta", "horaris del Mig Any", "programa d'un cap de setmana"],
     {"titol": "Títol (\\n per a salt). Paraula en cursiva magenta amb {{ }}: 'Mig {{Any}}'",
      "data": "(opc.) Línia de data en majúscules: 'Dissabte · 24 d'octubre de 2026'",
      "subtitol": "(opc.) Línia en cursiva sota el títol: 'Horaris de la jornada'",
      "grups": "[{'titol':'La diana','files':[['Arrancà','9:35','detall opcional'],['Carbonato','10:31']]}, ...] (màx. ~3 grups / 8 files)",
      "nota": "(opc.) Línia curta al peu en Lato"}, "story 1080×1920")

# 2. Anunci de text (clar i magenta)
def story_anunci(th):
    T = THEMES[th]
    body = f"""{bgimg(th, S_W, S_H)}
  {frame(S_W, S_H, th)}
  {escut(540, 290, 230, 'a')}
  {eyebrow('etiqueta', 540, 565, 800, 'Filà Magenta · Alcoi', th=th)}
  {orn(540, 640, 380, th)}
  {text('titol', (90, 680, 900, 330), 118, th=th, weight=700, fill=T['title'], lh=1.08, sample='Titular\ndel missatge')}
  {text('text', (110, 1020, 860, 440), 52, th=th, weight=400, lh=1.3, sample='Cos amb **noms propis** en negreta.', cond='text')}
  {text('dada', (90, 1470, 900, 70), 36, th=th, font='lato', weight=700, fill=T['label'], tracking=3, sample='', cond='dada')}"""
    return svg(S_W, S_H, body, "Story · Anunci de text")


F_ANUNCI = {"etiqueta": "(opc.) Etiqueta en majúscules, per defecte 'Filà Magenta · Alcoi'",
            "titol": "Frase principal (2-4 línies). **negreta** per a noms. [[x]] = color d'accent; {{x}} = cursiva d'accent.",
            "text": "(opc.) Cos explicatiu", "dada": "(opc.) Data/hora/lloc destacat en Lato"}
save("story-anunci", story_anunci("clar"),
     "Anunci només de text sobre paper clar amb escut: novetats, avisos, convocatòries, renovacions.",
     ["hem renovat contracte amb la banda", "convocatòria", "avís", "recordatori"], F_ANUNCI, "story 1080×1920")
save("story-anunci-magenta", story_anunci("magenta"),
     "Igual que story-anunci però sobre magenta pla: per a notícies destacades i solemnes.",
     ["renovació amb la banda", "comunicat destacat"], F_ANUNCI, "story 1080×1920")

# 3. Foto d'un acte
body = f"""{bgimg('clar', S_W, S_H)}
  {frame(S_W, S_H)}
  <rect x="86" y="300" width="908" height="1000" fill="none" stroke="{GOLD}" stroke-width="2"/>
  {photo('foto', (100, 314, 880, 972))}
  {seal(440, 1236, 130, 'f')}
  {eyebrow('etiqueta', 540, 1405, 800, 'Filà Magenta', cond='etiqueta')}
  {text('titol', (90, 1440, 900, 150), 84, weight=700, fill=MAG, lh=1.08, valign='top', sample='Titular sobre la foto')}
  {text('subtitol', (110, 1595, 860, 60), 36, font='lato', weight=400, valign='top', lh=1.3, sample='', cond='subtitol')}"""
save("story-foto", svg(S_W, S_H, body, "Story · Foto"),
     "Una fotografia (vertical o retallada) emmarcada sobre paper, amb segell de l'escut i titular a sota.",
     ["foto d'un acte", "moment de l'entradeta", "agraïment amb foto"],
     {"foto": "Ruta a la fotografia", "titol": "Titular (1-2 línies)",
      "subtitol": "(opc.) Frase en Lato", "etiqueta": "(opc.) Etiqueta en majúscules"}, "story 1080×1920")


# 4/5. Persona (felicitació / nomenament)  i  dol
def persona_story(dol):
    th = "dol" if dol else "clar"
    T = THEMES[th]
    fil = T["line"]
    dy = -30
    arch = f"M200,{1030+dy}V{720+dy}A340,340 0 0 1 880,{720+dy}V{1030+dy}Z"
    outer = f"M178,{1052+dy}V{720+dy}A362,362 0 0 1 902,{720+dy}V{1052+dy}Z"
    ex = f'<clipPath id="arc"><path d="{arch}"/></clipPath>'
    label = "In memoriam" if dol else "Enhorabona"
    body = f"""{bgimg(th, S_W, S_H)}
  {frame(S_W, S_H, th)}
  {llac(540, 140, 1.6) if dol else ''}
  {eyebrow('etiqueta', 540, 275, 800, label, size=28, th=th)}
  {photo('foto', (200, 350, 680, 650), clip='arc', gray=(1 if dol else 0))}
  <path d="{arch}" fill="none" stroke="{fil}" stroke-width="5"/>
  <path d="{outer}" fill="none" stroke="{fil}" stroke-width="2" opacity=".65"/>
  {text('nom', (80, 1080, 920, 230), 98, th=th, weight=700, fill=T['title'], lh=1.06, sample='Nom Cognom')}
  {text('dates', (90, 1320, 900, 60), 38, th=th, font='lato', weight=700, fill=T['label'], tracking=5, sample='', cond='dates')}
  {orn(540, 1405, 300, th)}
  {text('text', (110, 1430, 860, 150), 44, th=th, weight=400, lh=1.28, sample='', cond='text')}"""
    return svg(S_W, S_H, body, "Story · " + ("Dol" if dol else "Persona"), ex)


save("story-persona", persona_story(False),
     "Felicitació, nomenament o reconeixement a una persona amb la seua foto en finestra d'arc.",
     ["felicitar algú", "nou càrrec", "aniversari", "anunci d'alferes/capità"],
     {"foto": "Foto de la persona (preferiblement retrat; es retalla)", "nom": "Nom i cognoms (2 línies màx.)",
      "text": "(opc.) Motiu: 'per la seua alferecia 2027'", "dates": "(opc.) Dada: 'Alferes 2027'",
      "etiqueta": "(opc.) Per defecte 'Enhorabona'"}, "story 1080×1920")
save("story-dol", persona_story(True),
     "Condol per defunció. Paper gris sense calidesa, foto en blanc i negre, to sobri (sense emojis ni exclamacions).",
     ["ha mort un company/a", "condol", "aniversari de la mort"],
     {"foto": "Foto de la persona", "nom": "Nom i cognoms", "dates": "(opc.) '1948 — 2026'",
      "text": "(opc.) Frase sobria: 'La Filà Magenta lamenta la seua pèrdua i acompanya la família'",
      "etiqueta": "(opc.) Per defecte 'In memoriam'"}, "story 1080×1920")

# 6. Concurs d'olla (olla en traç daurat sobre paper; titular segons classificació)
body = f"""{bgimg('clar', S_W, S_H)}
  {frame(S_W, S_H)}
  {escut(540, 290, 230, 'o')}
  {eyebrow('etiqueta', 540, 565, 800, 'Filà Magenta · Alcoi')}
  {orn(540, 640, 380)}
  {text('titol', (90, 680, 900, 330), 118, weight=700, fill=MAG, lh=1.08, sample='Titular\ndel missatge')}
  <g id="olla" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" transform="translate(540,1215)">
    <path d="M-170,-40 H170 V60 C170,150 110,190 0,190 C-110,190 -170,150 -170,60 Z"/>
    <path d="M-170,-10 C-215,-10 -225,40 -170,40 M170,-10 C215,-10 225,40 170,40"/>
    <path d="M-190,-40 H190 M-120,-70 C-120,-85 120,-85 120,-70 V-40 M-120,-70 V-40"/>
    <path d="M0,-85 V-100 M-18,-100 H18"/>
    <path d="M-60,-120 C-85,-160 -35,-180 -60,-225 M0,-130 C-25,-175 25,-195 0,-245 M60,-120 C35,-160 85,-180 60,-225" opacity=".8"/>
    <path d="M-110,60 C-60,90 60,90 110,60" opacity=".6"/>
  </g>
  {text('dada', (90, 1470, 900, 70), 36, font='lato', weight=700, fill=GOLD_T, tracking=3, sample='', cond='dada')}"""
save("story-olla", svg(S_W, S_H, body, "Story · Olla"),
     "Concurs d'olla: olla daurada i titular segons classificació (campions / subcampions / tercers).",
     ["resultat del concurs d'olla", "avís del concurs"],
     {"etiqueta": "(opc.) per defecte 'Filà Magenta · Alcoi'", "titol": "Titular. [[x]] per a la paraula clau",
      "dada": "(opc.) 'Enhorabona als cuiners'"}, "story 1080×1920")

# ───────────────────────── POSTS (1080×1350, 4:5 = mínim d'Instagram; la graella retalla 34 px a cada costat) ─────────────────────────
PW, PH = 1080, 1350
FMT = "post 1080×1350 (4:5)"

body = f"""{bgimg('clar', PW, PH)}
  {frame(PW, PH)}
  {escut(540, 110, 150, 'p1')}
  {orn(540, 310, 340)}
  {text('text', (160, 345, 760, 640), 66, weight=400, lh=1.22, sample='Des de la **Filà Magenta** donem l\'enhorabona a **Nom Cognom**')}
  {text('dada', (140, 1030, 800, 60), 32, font='lato', weight=700, fill=GOLD_T, tracking=4, caps=True, sample='', cond='dada')}
  {footer(540, 1200)}"""
save("post-anunci", svg(PW, PH, body, "Post · Anunci de text"),
     "Anunci només de text sobre paper clar: felicitacions, avisos, renovacions.",
     ["felicitar algú amb text", "avís", "renovació de la banda"],
     {"text": "Frase completa; **negreta** per a noms propis, [[x]] accent, {{x}} cursiva d'accent",
      "dada": "(opc.) Data o lloc en Lato (majúscules)"}, FMT)

body = f"""{bgimg('clar', PW, PH)}
  {frame(PW, PH)}
  {escut(540, 100, 130, 'p2')}
  {text('titol', (150, 260, 780, 260), 92, weight=700, fill=MAG, lh=1.06, sample='Titular')}
  {orn(540, 545, 340)}
  {text('text', (160, 575, 760, 430), 50, weight=400, lh=1.28, sample='Cos del missatge amb **noms**.')}
  {text('dada', (140, 1030, 800, 56), 30, font='lato', weight=700, fill=GOLD_T, tracking=4, caps=True, sample='', cond='dada')}
  {footer(540, 1200)}"""
save("post-anunci-titol", svg(PW, PH, body, "Post · Anunci amb titular"),
     "Anunci amb titular i cos sobre paper. Per a missatges amb més informació (assemblea, sopar, cartells).",
     ["convocatòria d'assemblea", "novetat", "tancament de carrusel (agraïment)"],
     {"titol": "Titular (1-2 línies). {{x}} = paraula en cursiva d'accent", "text": "Cos", "dada": "(opc.) Data/lloc"}, FMT)

body = f"""{bgimg('magenta', PW, PH)}
  {frame(PW, PH, 'magenta')}
  {escut(540, 250, 270, 'p3')}
  {text('titol', (120, 580, 840, 340), 118, th='magenta', weight=700, caps=True, lh=1.06, tracking=3, sample='COMUNICAT\nOFICIAL', keep=True)}
  {orn(540, 975, 340, 'magenta')}
  {text('subtitol', (140, 1005, 800, 50), 28, th='magenta', font='lato', weight=700, fill='#E8C77D', tracking=6, caps=True, sample='', cond='subtitol')}
  {footer(540, 1200, 'magenta')}"""
save("post-comunicat", svg(PW, PH, body, "Post · Comunicat oficial"),
     "Portada simètrica i solemne sobre magenta pla per a comunicats oficials. El text complet va al peu de foto o a un 2n slide.",
     ["comunicat oficial", "nota de premsa", "decisió de junta"],
     {"titol": "Per defecte 'COMUNICAT\\nOFICIAL'", "subtitol": "(opc.) Data o assumpte en Lato"}, FMT)

body = f"""{bgimg('clar', PW, PH)}
  {frame(PW, PH)}
  <rect x="86" y="86" width="908" height="820" fill="none" stroke="{GOLD}" stroke-width="2"/>
  {photo('foto', (100, 100, 880, 792))}
  {seal(880, 800, 110, 'pf')}
  {text('titol', (90, 950, 900, 200), 86, weight=700, fill=MAG, valign='top', lh=1.08, sample='Titular sobre la foto')}
  {text('subtitol', (110, 1160, 860, 80), 36, font='lato', weight=400, valign='top', sample='', cond='subtitol')}"""
save("post-foto", svg(PW, PH, body, "Post · Foto amb titular"),
     "Una sola fotografia emmarcada sobre paper amb titular. Per a anunci amb foto o resum d'un acte.",
     ["anunci amb una foto", "foto destacada d'un acte"],
     {"foto": "Fotografia", "titol": "Titular (1-2 línies)", "subtitol": "(opc.) Línia en Lato"}, FMT)


def persona_post(dol):
    th = "dol" if dol else "clar"
    T = THEMES[th]; fil = T["line"]
    ex = '<clipPath id="ov"><ellipse cx="540" cy="480" rx="205" ry="270"/></clipPath>'
    body = f"""{bgimg(th, PW, PH)}
  {frame(PW, PH, th)}
  {llac(540, 112, .85) if dol else ''}
  {photo('foto', (335, 210, 410, 540), clip='ov', gray=(1 if dol else 0))}
  <ellipse cx="540" cy="480" rx="205" ry="270" fill="none" stroke="{fil}" stroke-width="4"/>
  <ellipse cx="540" cy="480" rx="225" ry="290" fill="none" stroke="{fil}" stroke-width="1.5" opacity=".6"/>
  {eyebrow('etiqueta', 540, 810, 600, 'In memoriam' if dol else 'Enhorabona', size=26, th=th)}
  {text('nom', (120, 860, 840, 110), 80, th=th, weight=700, fill=T['title'], lh=1.05, sample='Nom Cognom')}
  {text('text', (170, 990, 740, 110), 36, th=th, weight=400, lh=1.24, sample='', cond='text')}
  {footer(540, 1200, th)}"""
    return svg(PW, PH, body, "Post · " + ("Dol" if dol else "Persona"), ex)


save("post-persona", persona_post(False),
     "Felicitació o reconeixement a una persona, amb foto en finestra ovalada.",
     ["felicitar algú", "nou càrrec", "aniversari"],
     {"foto": "Retrat", "nom": "Nom i cognoms", "text": "(opc.) Motiu breu", "etiqueta": "(opc.) 'Enhorabona'"}, FMT)
save("post-dol", persona_post(True),
     "Condol per defunció (post). Paper gris, foto en B/N, to sobri.",
     ["ha mort un company/a", "condol"],
     {"foto": "Retrat", "nom": "Nom i cognoms", "text": "(opc.) Frase sobria breu", "etiqueta": "(opc.) 'In memoriam'"}, FMT)

# Carrusel: portada (foto emmarcada, titular a sota)
body = f"""{bgimg('clar', PW, PH)}
  {frame(PW, PH)}
  <rect x="86" y="86" width="908" height="700" fill="none" stroke="{GOLD}" stroke-width="2"/>
  {photo('foto', (100, 100, 880, 672))}
  {seal(150, 150, 104, 'cp')}
  {text('titol1', (80, 810, 920, 120), 100, weight=700, fill=MAG, caps=True, align='start', valign='bottom', lh=1, sample='TITOL')}
  {text('titol2', (80, 925, 920, 110), 100, weight=700, caps=True, fill=ACC, align='start', valign='bottom', lh=1, sample='DESTACAT', cond='titol2', extra='font-style="italic"')}
  {text('subtitol', (84, 1060, 700, 120), 40, weight=400, align='start', valign='top', lh=1.22, sample='Subtítol breu')}
  <g id="continua" data-if="continua"><text id="label-continua" x="960" y="1235" text-anchor="end" font-family="Playfair Display" font-style="italic" font-size="38" fill="{ACC}">Continua</text>
  <path d="M976,1226H1004M992,1212L1006,1226L992,1240" fill="none" stroke="{ACC}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>"""
save("carrusel-portada", svg(PW, PH, body, "Carrusel · Portada"),
     "Portada de carrusel: foto emmarcada sobre paper amb segell, titular en majúscules (magenta + cursiva d'accent) i 'Continua →'.",
     ["portada de fotos d'un acte", "resum d'una activitat"],
     {"foto": "Foto de portada", "titol1": "Primera línia (magenta, majúscules)",
      "titol2": "(opc.) Segona línia (cursiva, color d'accent)", "subtitol": "Frase curta. **negreta** per a noms",
      "continua": "true/false: mostra 'Continua →' (per defecte true)"}, FMT)

body = f"""<rect width="{PW}" height="{PH}" fill="{PAPER}"/>
  {photo('foto', (0, 0, PW, PH))}
  <g data-if="peu">{card(50, 1150, 700, 150, 1)}<rect x="62" y="1162" width="676" height="126" fill="none" stroke="{GOLD}" stroke-width="1.5"/></g>
  {escut_circ(50, 50, 96, 'ci')}
  {text('peu', (80, 1162, 640, 126), 34, fill=INK, align='start', valign='middle', lh=1.22, sample='', cond='peu')}
  <g data-if="pagina"><rect x="870" y="1236" width="160" height="56" rx="28" fill="{PAPER}" stroke="{GOLD}" stroke-width="2"/></g>
  {text('pagina', (870, 1236, 160, 56), 26, font='lato', weight=700, fill=GOLD_T, tracking=3, minsize=20, sample='02 / 08', cond='pagina')}"""
save("carrusel-interior", svg(PW, PH, body, "Carrusel · Foto interior"),
     "Foto a sang per als slides interiors del carrusel, amb escut petit, peu en targeta de paper i comptador opcional.",
     ["resta de fotos del carrusel"],
     {"foto": "Fotografia", "peu": "(opc.) Peu breu", "pagina": "(opc.) '02 / 08'"}, FMT)

body = f"""{bgimg('clar', PW, PH)}
  {frame(PW, PH)}
  <rect x="76" y="226" width="928" height="708" fill="none" stroke="{GOLD}" stroke-width="2"/>
  {photo('foto', (90, 240, 900, 680))}
  {escut_circ(96, 100, 90, 'ia')}
  {text('peu', (80, 980, 920, 170), 42, fill=INK, align='start', valign='top', lh=1.24, sample='', cond='peu')}
  <g data-if="pagina"><rect x="826" y="107" width="158" height="56" rx="28" fill="none" stroke="{GOLD}" stroke-width="2"/></g>
  {text('pagina', (826, 107, 158, 56), 26, font='lato', weight=700, fill=GOLD_T, tracking=3, minsize=20, sample='02 / 08', cond='pagina')}"""
save("carrusel-interior-apaisat", svg(PW, PH, body, "Carrusel · Foto interior apaisada"),
     "Foto apaïsada (4:3) emmarcada sobre paper. El llenç segueix sent 4:5 perquè Instagram fixa la proporció del carrusel amb la primera imatge.",
     ["foto horitzontal d'un carrusel (grups, files)"],
     {"foto": "Fotografia apaïsada", "peu": "(opc.) Peu breu", "pagina": "(opc.) '02 / 08'"}, FMT)

# ───────────────────────── VÍDEO (capes amb transparència) ─────────────────────────
body = f"""{card(96, 850, 1100, 160, .96)}
  <rect x="96" y="850" width="10" height="160" fill="{MAG}"/>
  <rect x="116" y="862" width="1068" height="136" fill="none" stroke="{GOLD}" stroke-width="1.5" opacity=".8"/>
  {text('nom', (150, 868, 1000, 76), 60, weight=700, fill=MAG, align='start', valign='middle', lh=1, sample='Nom Cognom')}
  {text('carrec', (150, 948, 1000, 40), 26, font='lato', weight=700, fill=ACC, align='start', tracking=6, caps=True, minsize=20, sample='Càrrec', cond='carrec')}
  {escut_circ(1190, 830, 110, 'v1')}"""
save("video-lower-third", svg(1920, 1080, body, "Vídeo · Lower third"),
     "Capa transparent 1920×1080 (PNG amb alfa): targeta de paper amb nom i càrrec sobre un vídeo.",
     ["identificar qui parla al vídeo"], {"nom": "Nom", "carrec": "(opc.) Càrrec o rol"}, "vídeo 1920×1080 alfa")

body = f"""{card(60, 1250, 960, 380)}
  <rect x="76" y="1266" width="928" height="348" fill="none" stroke="{GOLD}" stroke-width="1.5"/>
  {escut_circ(100, 1290, 100, 'v2')}
  {eyebrow('etiqueta', 640, 1310, 700, 'Filà Magenta', cond='etiqueta', size=24)}
  {text('titol', (90, 1380, 900, 150), 84, weight=700, fill=MAG, align='middle', valign='middle', lh=1.06, sample='Títol del vídeo')}
  {text('subtitol', (90, 1535, 900, 60), 34, font='lato', fill=INK, align='middle', valign='top', sample='', cond='subtitol')}"""
save("video-titol", svg(S_W, S_H, body, "Vídeo · Targeta de títol"),
     "Capa transparent vertical 1080×1920: targeta de paper amb títol i escut per a obrir un vídeo/reel (respecta zones segures).",
     ["títol d'inici de reel", "tancament amb data"],
     {"titol": "Títol", "subtitol": "(opc.)", "etiqueta": "(opc.)"}, "vídeo 1080×1920 alfa")

(OUT / "INDEX.json").write_text(json.dumps(INDEX, ensure_ascii=False, indent=1))
print("ok", len(INDEX), "plantilles")
