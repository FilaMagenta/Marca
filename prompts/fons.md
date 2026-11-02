# Prompts per a fons nous (IA d'imatge)

Per a generar fons coherents amb els existents (`assets/fons/`). Sempre: **sense text, sense logotips, sense persones**. Revisa que no apareguen lletres falses ni símbols religiosos o d'altres entitats.

## Base comuna (afegeix-la a tots)
> Luxurious antique theatre curtain photography, deep wine-magenta velvet (#7D1941 to near-black #2A0614), embroidered gold trim (#C69232) with floral baroque and Moorish arabesque filigree, accents of forest-olive green silk (#576437), soft cinematic side light, shallow depth of field, rich fabric texture, elegant, ceremonial, classic. No text, no letters, no logos, no people, no watermark.

## Formats
- **Story 1080×1920 (9:16)**: «…vertical 9:16 composition, ornate draped valance at the top and a smaller gold-embroidered fabric swag at the bottom, large calm dark velvet area in the center with no detail.»
- **Post 1080×1350 (4:5)**: «…vertical 4:5 composition, organic frame of overlapping gold-edged magenta and olive silk ribbons around all four corners, smooth empty velvet center.»
- **Cortina per a portada de carrusel (PNG amb alfa)**: «…diagonal drape of velvet and gold satin with embroidered green ribbon crossing from top-left to right, the top-right corner left pure black (to become transparent), dark velvet bottom area for text.» (Treu el negre amb Inkscape/GIMP → alfa.)
- **Vídeo**: mateix que story, però «static, no motion blur, large empty center for subtitles».

## Variants
- **Dol**: base + «more muted and darker, desaturated wine and charcoal, gold trim subdued and matte, candle-like soft glow, solemn, no bright highlights».
- **Mig Any / festa**: base + «warmer golden highlights, festive but refined».
- **Fons clar (ús diürn)**: «warm off-white (#F5F5F5) linen with fine gold and magenta embroidered border, minimal».
- **Textura de vellut sola**: «macro photo of wine-magenta velvet, subtle pile, no folds, seamless, even lighting».

## Després de generar
1. Redimensiona a 1080×1920 / 1080×1350 (mín. 1080 d'amplada; millor 2×).
2. Guarda a `assets/fons/` i referencia'l des de `tools/build_templates.py` (`bg('nom.jpg', w, h)`).
3. Comprova que el centre és prou fosc per a text blanc (contrast ≥ 7:1) i que els ornaments no entren a les zones segures.
