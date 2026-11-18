#!/usr/bin/env python3
"""Genera hepta-home-wp.html desde el hepta-home-v*.html de la raíz.

No editar el fragmento a mano: el CSS se reescribe para vivir dentro de
#hepta-landing y las imágenes pasan a /wp-content/uploads/hepta-landing/.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_BASE = "/wp-content/uploads/hepta-landing"
SCOPE = "#hepta-landing#hepta-landing"
OUT_NAME = "hepta-home-wp.html"

# Ids del documento estático. En una página de WordPress pueden chocar
# con el tema, Elementor o WooCommerce.
IDS = [
    "slideTitle",
    "swipeHint",
    "catPrev",
    "catNext",
    "catsWrap",
    "categorias",
    "productos",
    "obra-gruesa",
    "terciados",
    "como",
    "lineas",
    "bPrev",
    "bNext",
    "bDots",
    "contacto",
    "c",
    "navMenu",
]

PREPEND_CSS = (
    "/* all:revert va primero: un all posterior borraría fondo, color y tipografía. */\n"
    f"{SCOPE}{{all:revert;display:block}}\n"
)

EXTRA_CSS = r"""
/* El scroll de la portada es el del documento. overflow en #hepta-landing
   rompería el header sticky y el WhatsApp fixed. */
html:has(#hepta-landing){scroll-behavior:smooth;overflow-x:clip;background:#F5F4F1}
body:has(#hepta-landing){background:#F5F4F1;margin:0}
#hepta-landing#hepta-landing{isolation:isolate;min-height:100vh;color-scheme:light}
/* Astra/Elementor pintan p, h1 o a con un id (#content .entry-content p).
   Heredar desde el padre no les gana: hay que repetir color y fuente en el elemento.
   Las reglas con clase de la landing (.display, .hero h1, .lead) siguen ganando. */
#hepta-landing#hepta-landing p,
#hepta-landing#hepta-landing li,
#hepta-landing#hepta-landing h1,
#hepta-landing#hepta-landing h2,
#hepta-landing#hepta-landing h3,
#hepta-landing#hepta-landing h4,
#hepta-landing#hepta-landing h5,
#hepta-landing#hepta-landing h6,
#hepta-landing#hepta-landing a,
#hepta-landing#hepta-landing span,
#hepta-landing#hepta-landing small,
#hepta-landing#hepta-landing b,
#hepta-landing#hepta-landing strong,
#hepta-landing#hepta-landing em,
#hepta-landing#hepta-landing label{
  color:inherit;
  font-family:inherit;
  letter-spacing:inherit;
  text-transform:inherit
}
#hepta-landing#hepta-landing button{font:inherit;color:inherit;background:transparent;border:0;margin:0;padding:0;appearance:none;-webkit-appearance:none}
#hepta-landing#hepta-landing h1,
#hepta-landing#hepta-landing h2,
#hepta-landing#hepta-landing h3,
#hepta-landing#hepta-landing h4,
#hepta-landing#hepta-landing p{margin:0}
#hepta-landing#hepta-landing ul,
#hepta-landing#hepta-landing ol{list-style:none;margin:0;padding:0}
#hepta-landing#hepta-landing :focus-visible{outline:2px solid #17191D;outline-offset:3px}
#hepta-landing#hepta-landing section[id]{scroll-margin-top:84px}
body.admin-bar #hepta-landing#hepta-landing header{top:32px}
body.admin-bar #hepta-landing#hepta-landing section[id]{scroll-margin-top:116px}
@media (max-width:782px){
  body.admin-bar #hepta-landing#hepta-landing header{top:46px}
  body.admin-bar #hepta-landing#hepta-landing section[id]{scroll-margin-top:130px}
}
#hepta-landing#hepta-landing .form-card iframe{display:block;width:100%;max-width:100%;border:0;background:transparent}

/* Contenedor de Astra / Elementor / Gutenberg: solo ancestros de esta landing. */
body:has(#hepta-landing) .entry-header,
body:has(#hepta-landing) h1.entry-title,
body:has(#hepta-landing) .site-header,
body:has(#hepta-landing) header#masthead,
body:has(#hepta-landing) .ast-above-header,
body:has(#hepta-landing) .ast-below-header,
body:has(#hepta-landing) .site-footer,
body:has(#hepta-landing) footer#colophon,
body:has(#hepta-landing) .elementor-location-header,
body:has(#hepta-landing) .elementor-location-footer{display:none !important}
.ast-container:has(#hepta-landing),
.site-content:has(#hepta-landing),
.entry-content:has(#hepta-landing),
#content:has(#hepta-landing){max-width:none !important;width:100% !important;padding:0 !important;margin-inline:0 !important}
.elementor-section:has(#hepta-landing),
.elementor-container:has(#hepta-landing),
.elementor-column:has(#hepta-landing),
.elementor-widget-wrap:has(#hepta-landing),
.elementor-widget-container:has(#hepta-landing),
.elementor-widget-html:has(#hepta-landing),
.e-con:has(#hepta-landing),
.e-con:has(#hepta-landing) > .e-con-inner,
.wp-block-html:has(#hepta-landing){
  --padding-top:0px;--padding-right:0px;--padding-bottom:0px;--padding-left:0px;
  --container-max-width:100%;
  max-width:none !important;width:100% !important;padding:0 !important;margin:0 !important
}
""".strip()


def source_file() -> Path:
    files = list(ROOT.glob("hepta-home-v*.html"))
    if not files:
        sys.exit("No hay hepta-home-v*.html en la raíz.")

    def version(path: Path) -> tuple[int, ...]:
        match = re.search(r"v(\d+(?:_\d+)*)", path.name)
        if not match:
            return (0,)
        return tuple(int(part) for part in match.group(1).split("_"))

    return max(files, key=version)


def skip_string(css: str, i: int) -> int:
    quote = css[i]
    i += 1
    while i < len(css):
        if css[i] == "\\":
            i += 2
            continue
        if css[i] == quote:
            return i + 1
        i += 1
    return i


def matching_brace(css: str, open_idx: int) -> int:
    depth = 0
    i = open_idx
    while i < len(css):
        if css.startswith("/*", i):
            end = css.find("*/", i + 2)
            i = len(css) if end < 0 else end + 2
            continue
        char = css[i]
        if char in "\"'":
            i = skip_string(css, i)
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise SystemExit("CSS desbalanceado.")


def split_selectors(selector: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    i = 0
    while i < len(selector):
        if selector.startswith("/*", i):
            end = selector.find("*/", i + 2)
            i = len(selector) if end < 0 else end + 2
            continue
        char = selector[i]
        if char in "\"'":
            i = skip_string(selector, i)
            continue
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(selector[start:i])
            start = i + 1
        i += 1
    parts.append(selector[start:])
    return parts


def prefix_one(selector: str) -> str:
    stripped = selector.strip()
    if not stripped:
        return selector
    if stripped in (":root", "body"):
        return SCOPE
    if stripped == "html":
        return "html:has(#hepta-landing)"
    if stripped == "*":
        return f"{SCOPE}, {SCOPE} *"
    return f"{SCOPE} {stripped}"


def prefix_selector_list(selector: str) -> str:
    return ", ".join(prefix_one(part) for part in split_selectors(selector))


def rename_keyframes(css: str) -> str:
    for name in ("spin", "nudge", "ring"):
        css = css.replace(f"@keyframes {name}", f"@keyframes hepta-{name}")
        css = css.replace(f"animation:{name}", f"animation:hepta-{name}")
    return css


def prefix_block(css: str) -> str:
    out: list[str] = []
    i = 0
    n = len(css)
    while i < n:
        if css.startswith("/*", i):
            end = css.find("*/", i + 2)
            if end < 0:
                out.append(css[i:])
                break
            out.append(css[i : end + 2])
            i = end + 2
            continue
        if css[i] == "@":
            j = i
            kind = None
            while j < n:
                if css.startswith("/*", j):
                    end = css.find("*/", j + 2)
                    j = n if end < 0 else end + 2
                    continue
                if css[j] in "\"'":
                    j = skip_string(css, j)
                    continue
                if css[j] == "{":
                    kind = "block"
                    break
                if css[j] == ";":
                    kind = "semi"
                    break
                j += 1
            if kind == "semi":
                out.append(css[i : j + 1])
                i = j + 1
                continue
            if kind != "block":
                out.append(css[i:])
                break
            end = matching_brace(css, j)
            prelude = css[i:j]
            inner = css[j + 1 : end]
            if prelude.strip().lower().startswith("@keyframes"):
                out.append(prelude + "{" + inner + "}")
            else:
                out.append(prelude + "{" + prefix_block(inner) + "}")
            i = end + 1
            continue
        if css[i].isspace():
            out.append(css[i])
            i += 1
            continue
        j = i
        while j < n and css[j] != "{":
            if css.startswith("/*", j):
                end = css.find("*/", j + 2)
                j = n if end < 0 else end + 2
                continue
            if css[j] in "\"'":
                j = skip_string(css, j)
                continue
            j += 1
        if j >= n:
            out.append(css[i:])
            break
        end = matching_brace(css, j)
        out.append(prefix_selector_list(css[i:j]) + "{" + css[j + 1 : end] + "}")
        i = end + 1
    return "".join(out)


def rewrite_assets(text: str) -> str:
    for folder in ("Imagenes/", "Public/"):
        text = text.replace(f"url('{folder}", f"url('{ASSET_BASE}/{folder}")
        text = text.replace(f'url("{folder}', f'url("{ASSET_BASE}/{folder}')
        text = text.replace(f'src="{folder}', f'src="{ASSET_BASE}/{folder}')
        text = text.replace(f"src='{folder}", f"src='{ASSET_BASE}/{folder}")
    return text


def rewrite_ids(text: str) -> str:
    for name in sorted(IDS, key=len, reverse=True):
        text = text.replace(f'id="{name}"', f'id="hepta-{name}"')
        text = text.replace(f"id='{name}'", f"id='hepta-{name}'")
        text = text.replace(f'href="#{name}"', f'href="#hepta-{name}"')
        text = text.replace(f"href='#{name}'", f"href='#hepta-{name}'")
        text = text.replace(f'aria-controls="{name}"', f'aria-controls="hepta-{name}"')
        text = text.replace(f"getElementById('{name}')", f"getElementById('hepta-{name}')")
        text = text.replace(f'getElementById("{name}")', f'getElementById("hepta-{name}")')
    return text


def scope_script(script: str) -> str:
    script = script.replace("document.querySelector", "root.querySelector")
    script = re.sub(
        r"document\.getElementById\((['\"])(.+?)\1\)",
        r"root.querySelector('#\2')",
        script,
    )
    script = re.sub(
        r"(?<![\w.])addEventListener\('resize'",
        "window.addEventListener('resize'",
        script,
    )
    return (
        "(function(){\n"
        "  var root=document.getElementById('hepta-landing');\n"
        "  if(!root) return;\n"
        + script
        + "\n})();\n"
    )


def selectors_outside_keyframes(css: str) -> list[str]:
    found: list[str] = []

    def walk(block: str) -> None:
        i = 0
        n = len(block)
        while i < n:
            if block.startswith("/*", i):
                end = block.find("*/", i + 2)
                i = n if end < 0 else end + 2
                continue
            if block[i].isspace():
                i += 1
                continue
            if block[i] == "@":
                j = i
                while j < n and block[j] not in "{;":
                    j += 1
                if j >= n:
                    return
                if block[j] == ";":
                    i = j + 1
                    continue
                end = matching_brace(block, j)
                prelude = block[i:j].strip().lower()
                if not prelude.startswith("@keyframes"):
                    walk(block[j + 1 : end])
                i = end + 1
                continue
            j = i
            while j < n and block[j] != "{":
                j += 1
            if j >= n:
                return
            found.append(block[i:j].strip())
            i = matching_brace(block, j) + 1

    walk(css)
    return found


def validate(css: str, document: str, source_name: str) -> None:
    errors: list[str] = []
    for selector in selectors_outside_keyframes(css):
        for part in split_selectors(selector):
            piece = part.strip()
            if not piece:
                continue
            allowed = (
                "#hepta-landing" in piece
                or piece.startswith("html:has(#hepta-landing)")
                or piece.startswith("body:has(#hepta-landing)")
                or piece.startswith("body.admin-bar")
                or ":has(#hepta-landing)" in piece
            )
            if not allowed:
                errors.append(f"selector sin alcance: {piece}")
    if "src=\"Imagenes/" in document or "url('Imagenes/" in document or "url(\"Imagenes/" in document:
        errors.append("quedó una ruta relativa a Imagenes/")
    if re.search(r'href="https://heptachile\.cl/"(?![A-Za-z0-9])', document):
        errors.append("quedó un enlace a la home https://heptachile.cl/")
    if 'href="https://heptachile.cl/tienda/"' in document:
        errors.append("quedó un enlace a /tienda/; la tienda general va a /home-tienda/")
    if 'class="wa"' in document or ".wa{" in css:
        errors.append("quedó el botón flotante de WhatsApp")
    for needle in (
        'href="https://heptachile.cl/home-tienda/"',
        'href="/"',
        'data-zentru-form="774691286/solicitud-de-cotizaci-n-landing-hepta"',
        "https://beta.hapee.ai/static/form-embed.js",
        "https://wa.me/56987690593",
        "https://heptachile.cl/blog/",
        "https://heptachile.cl/categoria-producto/andamios/",
        "id=\"hepta-landing\"",
        f"{ASSET_BASE}/Imagenes/Banners/banner-asesoria-terreno.webp",
    ):
        if needle not in document:
            errors.append(f"falta {needle}")
    if f"Generado desde {source_name}" not in document:
        errors.append("falta la marca de origen")
    if errors:
        sys.exit("El fragmento no pasó las comprobaciones:\n- " + "\n- ".join(errors))


def build() -> None:
    source = source_file()
    html = source.read_text(encoding="utf-8")
    style_match = re.search(r"<style>(.*?)</style>", html, re.S)
    json_match = re.search(r'<script type="application/ld\+json">.*?</script>', html, re.S)
    body_match = re.search(r"<body>(.*?)</body>", html, re.S)
    if not style_match or not json_match or not body_match:
        sys.exit(f"No pude leer style, JSON-LD o body de {source.name}.")

    css = prefix_block(rename_keyframes(style_match.group(1)))
    css = rewrite_assets(css)
    # overflow-x en el bloque crea un scrollport y anula position:sticky / fixed.
    css = css.replace(f"{SCOPE}{{overflow-x:clip;", f"{SCOPE}{{", 1)
    body = rewrite_assets(rewrite_ids(body_match.group(1)))
    inline = list(
        re.finditer(
            r"<script(?![^>]*\bsrc=)(?![^>]*application/ld\+json)[^>]*>(.*?)</script>",
            body,
            re.S,
        )
    )
    if len(inline) != 1:
        sys.exit(f"Esperaba un solo <script> inline y hay {len(inline)}.")
    script = scope_script(inline[0].group(1))
    body = body[: inline[0].start()] + body[inline[0].end() :]
    lcp = f"{ASSET_BASE}/Imagenes/Banners/banner-asesoria-terreno.webp"
    document = f"""<!--
Hepta Chile — fragmento para pegar en WordPress. No es una página completa.
Origen: {source.name}. Regenerar con: python3 scripts/build-wp-landing.py
No editar este archivo a mano.
Assets: {ASSET_BASE}/ (Imagenes/ y Public/, subidos por el administrador de archivos, no por la mediateca).
Publicación: DEPLOY-WP.md
El <title>, la meta description, el canonical y Open Graph se configuran en el plugin SEO:
la portada queda en https://www.heptachile.cl/ y la tienda en https://heptachile.cl/tienda/.
-->
<div id="hepta-landing">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,700;125,800;125,900&family=Lexend:wght@200;300;400;500;600&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{lcp}" fetchpriority="high">
{json_match.group(0)}
<style>
/* Generado desde {source.name} por scripts/build-wp-landing.py. No editar a mano. */
{PREPEND_CSS}
{css}
{EXTRA_CSS}
</style>
{body.strip()}
<script>
{script}</script>
</div>
"""
    validate(PREPEND_CSS + "\n" + css + "\n" + EXTRA_CSS, document, source.name)
    destination = ROOT / OUT_NAME
    destination.write_text(document, encoding="utf-8")
    print(f"{source.name} -> {destination.name} ({len(document)} bytes)")


if __name__ == "__main__":
    build()
