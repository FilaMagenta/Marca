# Filà Magenta · Marca digital
- `manual/index.html` — manual visual (imprimible a PDF). En línia: https://filamagenta.github.io/Marca/ (es publica amb GitHub Pages).
- Disseny actual: «Paper i fil» (paper de lli clar, filets daurats, accent en cursiva). Fons: `python3 tools/make_fons_clars.py`.
- `AGENTS.md` — guia per a agents d'IA (context, taula de decisió, receptes, checklist).
- `templates/` — plantilles SVG (+ `INDEX.json` amb camps). Es regeneren amb `python3 tools/build_templates.py`.
- `tools/render.py` — omple una plantilla amb un JSON i exporta PNG (`--list` mostra camps). Exemples a `tools/examples/`.
- `assets/` — escut vectorial, fons i tipografies. `prompts/fons.md` — prompts per a fons nous. `out/` — peces generades.
