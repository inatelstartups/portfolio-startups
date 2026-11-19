#!/usr/bin/env python3
"""
Script de atualização automática do Portfólio de Startups (Inatel Startups).
Busca as 4 views compartilhadas do Airtable, baixa as logos via endpoint assinado,
aplica classificação óptica de fundo, ordena alfabeticamente (A-Z)
e atualiza o index.html.
"""
import html
import http.cookiejar
import json
import os
import re
import unicodedata
import urllib.request
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGOS_DIR = os.path.join(BASE_DIR, "elementos", "logos")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")

VIEWS = {
    "ideation": ("app9mAZl7zLu7zeZb", "https://airtable.com/app9mAZl7zLu7zeZb/shr6lGlyWE9395CtX/tblAEZQFetlB1ThTe"),
    "pre-incubated": ("app9mAZl7zLu7zeZb", "https://airtable.com/app9mAZl7zLu7zeZb/shrQMcUOOgtk19ydG/tblAEZQFetlB1ThTe"),
    "incubated": ("app9mAZl7zLu7zeZb", "https://airtable.com/app9mAZl7zLu7zeZb/shrd6rAzCsgZv2elr/tblAEZQFetlB1ThTe"),
    "graduated": ("app45MMiNeduNXvUx", "https://airtable.com/app45MMiNeduNXvUx/shrHu5Ku1Q5Phv7WP/tblAEZQFetlB1ThTe"),
}

STAGE_TAG_LABEL = {
    "ideation": "Ideação",
    "pre-incubated": "Pré-Incubação",
    "incubated": "Incubadas",
    "graduated": "Graduada",
}

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

LINKEDIN_SVG = (
    '<svg class="linkedin-icon" width="13" height="13" viewBox="0 0 24 24" fill="currentColor">'
    '<path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14'
    'c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 '
    '1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.5 12.268h-3v-5.604c0-1.337-.026-2.54-'
    '1.545-2.54-1.528 0-1.766 1.216-1.766 2.473v5.671h-3v-11h2.875v1.502h.04c.4-.754 1.378-1.547 '
    '2.836-1.547 3.03 0 3.59 1.995 3.59 4.592v6.453z"/></svg>'
)

ARROW_SVG = (
    '<svg class="link-arrow-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<line x1="5" y1="12" x2="19" y2="12"></line>'
    '<polyline points="12 5 19 12 12 19"></polyline></svg>'
)

PIN_SVG = (
    '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">'
    '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>'
    '<circle cx="12" cy="10" r="3"></circle></svg>'
)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return f"logo_{text}"


def normalize_url(url):
    url = (url or "").strip()
    if not url or url.lower() in ("n/a", "-", "não possui", "nao possui"):
        return ""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url


def detect_logo_bg(img_path):
    """Detecta se a imagem tem fundo sólido nos cantos para harmonizar o container."""
    try:
        im = Image.open(img_path).convert("RGBA")
        w, h = im.size
        corners = [
            im.getpixel((2, 2)),
            im.getpixel((max(0, w - 3), 2)),
            im.getpixel((2, max(0, h - 3))),
            im.getpixel((max(0, w - 3), max(0, h - 3))),
        ]
        opaque = [c for c in corners if c[3] > 230]
        if len(opaque) >= 3:
            r = sum(c[0] for c in opaque) // len(opaque)
            g = sum(c[1] for c in opaque) // len(opaque)
            b = sum(c[2] for c in opaque) // len(opaque)
            # If corners are similar, use that hex color
            if all(abs(c[0] - r) < 25 and abs(c[1] - g) < 25 and abs(c[2] - b) < 25 for c in opaque):
                return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        pass
    return ""


def fetch_view(app_id, view_url):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    req = urllib.request.Request(view_url, headers={"User-Agent": UA})
    with opener.open(req, timeout=20) as resp:
        html_page = resp.read().decode("utf-8")

    policy_str = (
        re.search(r'"accessPolicy":\s*"(.*?)(?<!\\)"', html_page)
        .group(1)
        .encode("utf-8")
        .decode("unicode_escape")
    )
    page_load_id = re.search(r'"pageLoadId":\s*"(.*?)"', html_page).group(1)
    view_id = json.loads(policy_str)["allowedActions"][0]["modelIdSelector"]

    api_url = f"https://airtable.com/v0.3/view/{view_id}/readSharedViewData"
    headers = {
        "User-Agent": UA,
        "x-airtable-application-id": app_id,
        "x-airtable-page-load-id": page_load_id,
        "x-airtable-access-policy": policy_str,
        "x-requested-with": "XMLHttpRequest",
        "x-time-zone": "America/Sao_Paulo",
        "x-user-locale": "pt-BR",
    }
    req2 = urllib.request.Request(api_url, headers=headers)
    with opener.open(req2, timeout=20) as resp2:
        res = json.loads(resp2.read().decode("utf-8"))

    return res["data"], opener


def main():
    os.makedirs(LOGOS_DIR, exist_ok=True)
    existing_logos = set(os.listdir(LOGOS_DIR))

    # Preserva estilos de container já ajustados manualmente no index.html
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        current_html = f.read()

    preserved_styles = {}
    for m in re.finditer(
        r'<div class="(portfolio-logo-container[^"]*)"([^>]*)>\s*<img src="elementos/logos/([^"?]+)',
        current_html,
    ):
        preserved_styles[m.group(3)] = (m.group(1), m.group(2))

    cards_html = []
    counts = {}

    for stage, (app_id, view_url) in VIEWS.items():
        print(f"Buscando view: {stage}...")
        data, opener = fetch_view(app_id, view_url)
        rows = data.get("rows", [])
        cols = data.get("columns", [])
        col_map = {c["id"]: c["name"] for c in cols}
        signed_urls = data.get("signedUserContentUrls", {})

        # Map multiSelect choices (ex: Estado da startup)
        choice_maps = {}
        for c in cols:
            choices = (c.get("typeOptions") or {}).get("choices") or {}
            if choices:
                choice_maps[c["name"]] = {cid: cinfo.get("name", "") for cid, cinfo in choices.items()}

        stage_items = []
        for r in rows:
            vals = r.get("cellValuesByColumnId", {})
            row_data = {col_map.get(k, k): v for k, v in vals.items()}
            nome = (row_data.get("Nome da Startup") or row_data.get("Nome da Empresa") or "").strip()
            if not nome:
                continue

            slug = slugify(nome)
            fotos = row_data.get("Logo da Startup") or row_data.get("Logo da Empresa") or []
            logo_filename = None
            for ext in (".png", ".jpg", ".jpeg", ".webp"):
                if f"{slug}{ext}" in existing_logos:
                    logo_filename = f"{slug}{ext}"
                    break

            if not logo_filename and fotos:
                foto = fotos[0]
                dl_key = foto.get("largeThumbUrl") or foto.get("fullThumbUrl") or foto.get("url")
                signed_dl = signed_urls.get(dl_key)
                if signed_dl:
                    ftype = (foto.get("type") or "").lower()
                    fname = (foto.get("filename") or "").lower()
                    ext = ".png" if ("png" in ftype or fname.endswith(".png")) else ".jpg"
                    logo_filename = f"{slug}{ext}"
                    out_path = os.path.join(LOGOS_DIR, logo_filename)
                    try:
                        r_img = urllib.request.Request(signed_dl, headers={"User-Agent": UA})
                        with opener.open(r_img, timeout=15) as resp_img:
                            with open(out_path, "wb") as f_out:
                                f_out.write(resp_img.read())
                        existing_logos.add(logo_filename)
                    except Exception as e:
                        print(f"  Erro ao baixar logo de {nome}: {e}")
                        logo_filename = None

            # Estado
            raw_estado = row_data.get("Estado da startup")
            estado_str = ""
            if isinstance(raw_estado, list) and raw_estado:
                cmap = choice_maps.get("Estado da startup", {})
                estado_str = cmap.get(raw_estado[0], "")
            elif isinstance(raw_estado, str):
                cmap = choice_maps.get("Estado da startup", {})
                estado_str = cmap.get(raw_estado, raw_estado)

            cidade = (row_data.get("Cidade da startup") or "").strip()
            location = f"{cidade}, {estado_str}" if (cidade and estado_str) else (cidade or estado_str)

            stage_items.append(
                {
                    "stage": stage,
                    "name": nome,
                    "solucao": (row_data.get("Solução") or "").strip(),
                    "location": location,
                    "linkedin": normalize_url(row_data.get("LinkedIn da Startup")),
                    "website": normalize_url(
                        row_data.get("Website da Startup") or row_data.get("Website da Empresa")
                    ),
                    "data_entrada": (row_data.get("Data de entrada") or "").strip(),
                    "data_graduacao": (row_data.get("Data de graduação") or "").strip(),
                    "logo": logo_filename,
                }
            )

        stage_items.sort(
            key=lambda s: unicodedata.normalize("NFKD", s["name"]).encode("ascii", "ignore").decode("ascii").lower()
        )
        counts[stage] = len(stage_items)
        print(f"  -> {stage}: {len(stage_items)} startups")

        tag_label = STAGE_TAG_LABEL[stage]
        for s in stage_items:
            name_esc = html.escape(s["name"])
            if s["logo"]:
                if s["logo"] in preserved_styles:
                    c_class, c_style = preserved_styles[s["logo"]]
                    img_class = "portfolio-logo logo-cover" if "cover-bg" in c_class else "portfolio-logo"
                else:
                    bg = detect_logo_bg(os.path.join(LOGOS_DIR, s["logo"]))
                    c_class = "portfolio-logo-container"
                    c_style = f' style="background-color: {bg};"' if bg else ""
                    img_class = "portfolio-logo"
                logo_block = (
                    f'                        <div class="{c_class}"{c_style}>\n'
                    f'                            <img src="elementos/logos/{s["logo"]}?v=6" alt="Logo da {name_esc}" class="{img_class}" loading="lazy">\n'
                    f'                        </div>'
                )
            else:
                initials = "".join(w[0] for w in s["name"].split()[:2]).upper()
                logo_block = (
                    f'                        <div class="portfolio-logo-container" style="background-color: #111827; color: #f8fafc; font-weight: 700; font-size: 18px;">\n'
                    f'                            <span>{html.escape(initials)}</span>\n'
                    f'                        </div>'
                )

            if stage == "graduated":
                dates_parts = []
                if s["data_entrada"]:
                    dates_parts.append(f'Incubação: {html.escape(s["data_entrada"])}')
                if s["data_graduacao"]:
                    dates_parts.append(f'Graduação: {html.escape(s["data_graduacao"])}')
                dates_html = (
                    f'                        <p class="portfolio-dates">{" <br> ".join(dates_parts)}</p>'
                    if dates_parts
                    else ""
                )
                body_lines = [f"                        <h4>{name_esc}</h4>"]
                if dates_html:
                    body_lines.append(dates_html)
            else:
                body_lines = [f"                        <h4>{name_esc}</h4>"]
                if s["location"]:
                    body_lines.append(
                        f'                        <div class="portfolio-location">{PIN_SVG}<span>{html.escape(s["location"])}</span></div>'
                    )
                if s["solucao"]:
                    body_lines.append(f'                        <p>{html.escape(s["solucao"])}</p>')

            links = []
            if s["website"]:
                links.append(
                    f'<a href="{html.escape(s["website"])}" target="_blank" rel="noopener noreferrer" class="portfolio-link-item">'
                    f"<span>Visitar site</span>{ARROW_SVG}</a>"
                )
            if s["linkedin"]:
                links.append(
                    f'<a href="{html.escape(s["linkedin"])}" target="_blank" rel="noopener noreferrer" class="portfolio-link-item portfolio-linkedin">'
                    f"{LINKEDIN_SVG}<span>LinkedIn</span>{ARROW_SVG}</a>"
                )

            if len(links) == 1:
                links_html = f'                    <div class="portfolio-links-row single-link">{links[0]}</div>'
            elif len(links) >= 2:
                links_html = f'                    <div class="portfolio-links-row">{"".join(links)}</div>'
            else:
                links_html = ""

            card = (
                f'                <!-- CARD: {tag_label} - {name_esc} -->\n'
                f'                <div class="portfolio-card {stage}">\n'
                f'                    <div class="portfolio-header">\n'
                f'                        <span class="portfolio-tag {stage}">{tag_label}</span>\n'
                f"{logo_block}\n"
                f"                    </div>\n"
                f'                    <div class="portfolio-body">\n'
                + "\n".join(body_lines)
                + "\n                    </div>"
                + (f"\n{links_html}" if links_html else "")
                + "\n                </div>"
            )
            cards_html.append(card)

    new_block = "<!-- START_PORTFOLIO_CARDS -->\n" + "\n\n".join(cards_html) + "\n                <!-- END_PORTFOLIO_CARDS -->"
    updated_html = re.sub(
        r"<!-- START_PORTFOLIO_CARDS -->.*?<!-- END_PORTFOLIO_CARDS -->",
        lambda _: new_block,
        current_html,
        flags=re.DOTALL,
    )
    updated_html = re.sub(r"style\.css\?v=\d+", "style.css?v=36", updated_html)

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(updated_html)

    total = sum(counts.values())
    print(f"\nSUCESSO! index.html atualizado com {total} startups: {counts}")


if __name__ == "__main__":
    main()
