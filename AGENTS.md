# Filà Magenta · Guia per a agents d'IA (xarxes socials)

Llig açò abans de generar res. Objectiu: convertir una petició curta («ha mort X, ací tens la foto», «horari de l'entradeta de dimarts») en una peça Meta correcta, sense preguntar el que ja ací està escrit.
Manual visual per a persones: `manual/index.html`. Tokens: `tokens/brand.json`.

## 1. Context en 30 segons
- **Festes de Moros i Cristians d'Alcoi**: es celebren al voltant de Sant Jordi (abril) i commemoren la defensa d'Alcoi davant al-Azraq (1276). Trilogia Festera (22, 23 i 24 d'abril): entrades, actes de Sant Jordi i dia de la pólvora. A octubre es fa el **Mig Any** (vegeu §1b).
- **Filà** = comparsa. **Filà Magenta** (bàndol moro; fundada maig de 1865 com a *Beduïns*, nom actual oficial el 1878; magenta pel color dels bombatxos). Emblema: mitja lluna groga amb estrella verda sobre fons magenta. Lema popular: «La Magenta la que més espenta». Seu: c/ Sant Doménech. Banda actual: **Primitiva Apolo d'Alcoi** (Instagram: instagram.com/primitivaalcoi). Abans, segons fonts de 2021, la Unió Musical de Beniarrés.
- Vocabulari: *primer tro* (president), *alferes*, *capità*, *sargent*, *dianer*, *glorier/glorieret*, *esquadra*, *boato*, *entrada/entradeta*, *diana*, *arrancà*, *font redona*, *Mig Any*, *assemblea*, *festers*, *cavallers*.
- Dades històriques vénen de fonts comunitàries: **no inventes dades**; si falta un nom, data o hora, pregunta-ho o deixa el camp buit.

## 1b. El Mig Any: com es viu (context après)
Informació donada per la filà; úsala com a punt de partida i **confirma-la** si hi ha dubte. Casos de referència: `casos/20261019-horaris mig any.json`, `casos/2026102*`.
- **Quan**: un dissabte d'octubre (2026: dissabte 24). Cada filà publica el seu horari intern, i l'organització un programa general per a totes («Programa d'actes»).
- **Diana**: a mig any **no se sol fer diana** (només la del matí del dia de l'entrada). El 2026 va ser una excepció: **diana extraordinària pel 750 aniversari del patronatge de Sant Jordi**. Missa del Fester a Sant Jordi, Plaça d'Espanya (res de l'Avemaria, hissada de l'ensenya pel Sant Jordiet a l'ajuntament, *Himne de la Festa*) i diana per ordre d'antiguitat. Els festers van poder vestir el **tratge oficial** (disseny oficial de cada filà).
- **Aniversari**: el 750 aniversari del patronatge és de **2026**; es va celebrar a les festes d'abril de 2026 i al Mig Any 2026, **però no es farà a les festes de 2027**. No hi facis referència en peces de 2027.
- **Esquadra del mig**: la filà ostenta el càrrec **d'esquadra del mig** durant el cicle 2026-2027, fins a les festes. El Mig Any 2026 va ser el seu primer acte al carrer com a tal. Escriu «enguany ostentem el càrrec d'esquadra del mig» o «som l'esquadra del mig», no «hem tingut esquadra del mig». Té una **heràldica pròpia**, gravada a la **cullera commemorativa** del Mig Any (cullera de fusta amb «Magenta» i l'heràldica, lliurada amb l'olla).
- **Dinar**: es dina **olleta** (olla). Les esquadres amb càrrec, com l'esquadra del mig, **dinen a la glorieta**; la resta de la filà dina a la seua filà (el 2026, **als Creuats**, perquè la seu de la Magenta encara estava en obres, i cal traure ticket a l'App).
- **Concurs d'olleta** (Parc de la Glorieta): lliurament d'ingredients a partir de les 8.30; plat concursant entre les 13.30 i les 13.40; premi a les 14.00. Cuina una colla xicoteta, no tota la filà. El 2026 el va guanyar la **Filà Maseros**; la Magenta no va guanyar però va fer una olla deliciosa. No ho oblides en les peces.
- **Nit**: **entradetes**, desfilada informal pel centre històric; és el **final de la jornada**, no el dinar. El programa permet formar amb disseny oficial **o de paisà**, però **no esquadres amb vestimenta mixta**. El 2026 la Magenta va formar **només de paisà**: hi havia festers amb el tratge, però no els suficients per a una esquadra i, per la imatge de la filà, es va decidir no formar-ne.
- **Llocs**: Creuats, Cafeteria Blau (darrere dels Verds), Bar Mamella, Parc de la Glorieta, Font Redona (eixida de l'entradeta de la Magenta, 20.55), Tot Mentira, **Cercle Industrial** (als horaris apareix com «Círcol»: és un error), Ajuntament.
- **Ordre de la jornada Magenta 2026**: 8.00 Creuats (café, herbero, dolcets) → 9.00 dianers de l'Arrancà (Cafeteria Blau) → 10.00 dianers del Carbonato (Bar Mamella) → arrancà, Bambú, País Valencià, Partidor, final → carrer Sant Jordi i Carbonato → 14.00 concurs d'olletes → 14.30 dinar → 20.55 entradeta des de la Font Redona.
- **Fonts**: `ca.750sanjorge.org` (programa del 750 aniversari).

## 1c. Peces del Mig Any: fluxos i criteris (aprés al Mig Any 2026)
- **Carrusel d'acte**: `carrusel-portada` (foto 1) + `carrusel-interior` per foto + `post-anunci-titol` de tancament. Numera tot «02 / 0N» **comptant la portada**; si afegeixes tancament, renumera les interiors. Noms: `casos/AAAAMMDD-carrusel-<acte>-NN.json` i `out/…png`; la data és la de l'acte, no la de la peça.
- **Peus de foto**: només el que sàpigues (acte, lloc). No inventes noms. Pregunta quina foto és quin acte si no ho saps.
- **Descripcions**: una versió **Facebook** (llarga, càlida, amb enllaços) i una **Instagram** (curta, fresca, amb un parell d'emojis i hashtags: #FilàMagenta #MigAny #Alcoi). Agraeix als cuiners i a la filà que ens va acollir; no diguis «gràcies a tots» pels cuiners (és una colla xicoteta). A IG es menciona la filà amb el seu usuari (Creuats: `@fila.cruzados`).
- **Crònica** (ODT, estil de les publicacions, `out/AAAAMMDD-cronica-<acte>.odt`): **atemporal**, pensada per a llegir-se d'ací 100 anys. Sense xarxes socials ni usuaris, sense «enguany/aquest any/ja només queda…». Data completa, context (què és la filà, el Mig Any) i horaris com a «horari previst» si no estàs segur que es complís. Pots esplaiar-te més que a les xarxes i incloure l'horari de la filà i el general. Genera l'ODT directament (zip amb `content.xml`, `styles.xml`, `Pictures/`); al meu entorn el LibreOffice no carregava fitxers i no vaig poder verificar-lo visualment: comprova'l abans de donar-lo per bo.
- **Estil d'escriptura**: normativa de l'AVL (§5). Evita floritures no sustentades («un dels punts més emotius…»).

## 2. Identitat visual (resum) — disseny «Paper i fil»
- Clar, pla i net, però amb tacte físic: **paper de lli** amb gra, **doble filet daurat amb cordó de passamaneria** i estrelles de quatre puntes, majúscules espaiades, numeració, molt d'aire. Una **paraula en cursiva d'accent** al titular: `{{Any}}`.
- Fons (`assets/fons/`, es regeneren amb `python3 tools/make_fons_clars.py`): `clar` (per defecte), `magenta` pla (avisos solemnes i comunicat) i `dol` (gris sobri, amb llaç negre `assets/llac-negre.svg`). Ja no hi ha vellut ni cortines.
- Colors de marca: Magenta Històric `#7D1941`, Daurat Enriquit `#C69232`, Verd Bosc `#576437`, Blanco Roto `#F5F5F5`, Gris Obscur `#373C41`. Derivats: Paper `#F3EBDD`, Tinta `#3A1427` (cos), Magenta Viu `#A91F5C` (accent i hores), Daurat de Text `#B08628` (etiquetes), Magenta Pla `#8A1F4B` (fons).
- Tipus: **Playfair Display** (titulars, noms, frases, detalls en cursiva) i **Lato** (etiquetes, hores, peus). Sobre paper: titular magenta, cos en tinta. Sobre magenta pla: titular i cos blanc roto, accent daurat clar. El daurat `#C69232` és per a filets, mai per a text.
- Escut: `assets/escut.svg` (rectangular) o `assets/escut-circular.svg`. No deformar, no recolorar. El circular va com a segell sobre la vora d'una foto, sense anell daurat.
- Peu de marca dels posts de text: «Filà Magenta · Alcoi · Des de 1865».

## 2b. Tria de plantilla (taula de decisió)
| Petició | Plantilla | Camps |
|---|---|---|
| Horaris d'acte (entradeta, diana, Mig Any) | `story-horaris` | `data`, `titol`, `subtitol`, `grups[]` |
| Avís / renovació / novetat només amb text, story | `story-anunci` (o `story-anunci-magenta` si és solemne) | `titol`, `text`, `dada` |
| Una foto d'un acte, story | `story-foto` | `foto`, `titol`, `subtitol` |
| Felicitar / nomenar algú, story | `story-persona` | `foto`, `nom`, `text`, `dates` |
| **Mort d'algú**, story | `story-dol` | `foto`, `nom`, `dates`, `text` |
| Felicitar algú, post | `post-persona` | `foto`, `nom`, `text` |
| **Mort d'algú**, post | `post-dol` | `foto`, `nom`, `text` |
| Anunci de text, post (renovació, felicitació) | `post-anunci` | `text`, `dada` |
| Anunci amb titular i cos (assemblea, sopar) | `post-anunci-titol` | `titol`, `text`, `dada` |
| Comunicat oficial | `post-comunicat` | `subtitol` (+ text complet al peu de foto) |
| Anunci amb **una** foto | `post-foto` | `foto`, `titol`, `subtitol` |
| Carrusel de fotos d'un acte | `carrusel-portada` + n × `carrusel-interior` (+ opc. `post-anunci-titol` de tancament) | vegeu §4 |
| Vídeo: nom del que parla | `video-lower-third` | `nom`, `carrec` |
| Vídeo: títol d'obertura | `video-titol` | `titol`, `subtitol` |
`python3 tools/render.py --list` mostra tots els camps.

## 3. Com generar (3 passos)
1. Crea un JSON (copia `tools/examples/<plantilla>.json`):
   ```json
   {"plantilla": "story-dol", "foto": "/ruta/foto.jpg", "foto_focus": [0.5, 0.35],
    "nom": "Nom Cognom", "dates": "1948 — 2026",
    "text": "La Filà Magenta lamenta la seua pèrdua i acompanya la família i els amics."}
   ```
2. `python3 tools/render.py peça.json -o out/nom.png` (opcional `--scale 2`).
3. Obri el PNG i passa la **checklist de §6**. Si el text no cap, acurça'l (l'script avisa amb ⚠), no baixes de la mida mínima.
Marcat de text: `**negreta**` (noms propis), `[[accent]]` (paraula clau amb color d'accent), `{{cursiva}}` (cursiva amb color d'accent), `\n` salt de línia. L'script ajusta la mida automàticament.
`foto_focus` = punt d'interès (x,y entre 0 i 1) per al retall; apunta-lo a la cara.
Requisits: Python 3 + Pillow, Inkscape CLI, fonts (`python3 tools/render.py --install-fonts`).

## 4. Receptes
**Ha mort X (+ foto)** → `story-dol` (story) i/o `post-dol`. Foto en B/N automàtica. Text sobri: *«La Filà Magenta lamenta la mort de [Nom] i acompanya la família i els amics en aquest moment.»* Sense emojis, sense exclamacions, sense hashtags festius. Si no hi ha foto: `story-anunci` amb `titol` «Descanse en pau» i `text` amb el nom (no inventes foto).
**Horari de [acte]** → `story-horaris`. `data`: «Dissabte · 24 d'octubre de 2026», `titol`: «Mig {{Any}}», `subtitol`: «Horaris de la jornada». Un `grup` per cada acte (`titol`, es dibuixa com a pestanya) amb `files` `[acte, hora, detall opcional]`. Hores en format `9:35` / `20:55`. Màx. 3 grups / 8 files; si n'hi ha més, parteix en dues stories. Nom del fitxer: `AAAAMMDD-horaris <acte>.png`.
**Felicitació / nou càrrec** → `post-persona` o `post-anunci` (frase tipus: «Des de la **Filà Magenta** donem l'enhorabona a **[Nom]** pel seu càrrec de **[càrrec]**»).
**Renovació amb la banda / contracte** → `post-anunci-titol` (`titol` «Renovem amb la banda», `text` amb la informació) o `story-anunci`.
**Comunicat oficial** → `post-comunicat` com a primera imatge; el text íntegre al peu de la publicació.
**Carrusel d'un acte**: 1) `carrusel-portada` (`titol1` blanc en majúscules, `titol2` daurat en majúscules, `subtitol`, `foto` la millor); 2) una `carrusel-interior` per foto (`pagina` «02 / 08»); 3) opc. `post-anunci-titol` de tancament. Màx. 10 imatges (límit de Meta). Ordre: cronològic, portada primer.
**Concurs d'olla** → `story-olla` (olla daurada; titular segons classificació: campions / subcampions / tercers) amb `dada` «Enhorabona als cuiners». Cuina només una parella o tres persones, no tota la filà: no escrigues «gràcies a tots». Prepara-les abans del resultat (`casos/*-olla-*.json`) i usa només la que toque. La foto de l'equip, amb `story-foto`.
**Una sola foto d'un acte** → `post-foto` (post) o `story-foto` (story).
**Vídeo d'activitat**: edita el vídeo en vertical 1080×1920, sobreposa `video-titol` (PNG amb alfa) els primers 2-3 s i `video-lower-third` (1920×1080) si apareix algú identificat; tanca amb `story-anunci`.

## 5. Redacció
- Català (valencià), **normativa de l'AVL**: subjuntiu en -isca/-esca (llegisca, servisquen), formes valencianes (eixir, xicotet, conéixer, aquell, vam), «Cercle Industrial» (no «Círcol»). Accents i apòstrofs correctes. Tractament de «nosaltres» («Des de la Filà Magenta donem…»).
- Titulars curts (≤ 8 paraules). **Negreta només per a noms propis i dades clau.**
- Dates: «divendres 18 de setembre», hores «17:30 h» (en story, «17:30»).
- Cap valor de dades inventat. Cap faltes. «Magenta» sempre amb majúscula; el nom oficial és «Filà Magenta».
- Dol: sobri; ni punts d'admiració ni emojis. Celebració: càlid, però no col·loquial.

## 6. Checklist abans d'entregar
- [ ] La plantilla correspon al cas i al format (story 1080×1920, post/carrusel 1080×1350 = 4:5). Instagram només accepta pujar de 4:5 a 1,91:1 (3:4 és fora de rang i s'autoretalla); la graella del perfil mostra 3:4 i retalla ~34 px a cada costat d'un 4:5, per això el text i els rostres han d'estar a ≥ 60 px dels laterals. Portades de reel: el títol dins la franja central 3:4 (y 240–1680).
- [ ] El text no queda tallat ni ha baixat de ~32 px; res a les zones de la UI de Meta (story: 250 px dalt i 340 px baix).
- [ ] Nom, càrrec, dates i hores coincideixen amb el que ha dit l'usuari.
- [ ] Ortografia revisada. Majúscules i accents.
- [ ] Foto: cares ben retallades (usa `foto_focus`); en dol, B/N.
- [ ] Només colors i tipus de la marca; l'escut sense alterar.
- [ ] Fitxer: PNG sRGB, nom `AAAAMMDD-descripció.png`.

## 7. Prohibit
Canviar la paleta o tipus · gradients freds/neó · emojis dins la imatge · estirar l'escut · foto sense permís explícit · text llarg sobre foto · majúscules en blocs llargs · fons blancs sense marca · generar escuts amb IA (usa `assets/escut*.svg`).

## 8. Fons nous i casos no coberts
Si cap plantilla encaixa, copia la més pròxima de `templates/` i modifica'n els camps (`id="field-…"`, `data-box="x y w h"`). Per a fons nous amb IA d'imatge, usa `prompts/fons.md`. Regenera totes les plantilles amb `python3 tools/build_templates.py`.
