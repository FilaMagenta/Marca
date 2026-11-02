# Filà Magenta · Marca digital
- `manual/index.html` — manual visual (obre'l al navegador; imprimible a PDF).
- `AGENTS.md` — guia per a agents d'IA (context, taula de decisió, receptes, checklist).
- `templates/` — plantilles SVG (+ `INDEX.json` amb camps). Es regeneren amb `python3 tools/build_templates.py`.
- `tools/render.py` — omple una plantilla amb un JSON i exporta PNG (`--list` mostra camps). Exemples a `tools/examples/`.
- `assets/` — escut vectorial, fons i tipografies. `prompts/fons.md` — prompts per a fons nous. `out/` — peces generades.
