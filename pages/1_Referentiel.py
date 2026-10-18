import json
from html import escape
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st

from judo_utils import filter_techniques, get_theme_styles


ROOT = Path(__file__).resolve().parent.parent
TECHNIQUES = json.loads((ROOT / "techniques.json").read_text(encoding="utf-8"))
JUDO_MARK_SVG = (ROOT / "assets/judo_mark.svg").read_text(encoding="utf-8")
OFFICIAL_PDF_URL = (
    "https://www.ffjudo.com/resource-file/document/"
    "1789035361_068de2d2976847c37f5a.pdf"
)
OFFICIAL_RULES_URL = (
    "https://www.ffjudo.com/resource-file/document/"
    "1790927392_ff301db31bacdcbb3b21.pdf"
)
GROUND_CATEGORIES = {"Osaekomi", "Shime waza", "Kansetsu waza"}
DESCRIPTIONS = {
    "Koshi waza": "Techniques de hanche",
    "Te waza": "Techniques de bras",
    "Ashi waza": "Techniques de jambe",
    "Sutemi waza": "Techniques de sacrifice",
    "Osaekomi": "Immobilisations",
    "Shime waza": "Étranglements",
    "Kansetsu waza": "Clés de coude",
}

st.set_page_config(
    page_title="Référentiel des techniques - Gokyo",
    page_icon="🥋",
    layout="centered",
)

theme_mode = st.query_params.get("theme", "system")
if theme_mode not in {"dark", "light"}:
    theme_mode = "system"

st.markdown(get_theme_styles(theme_mode), unsafe_allow_html=True)
st.markdown(
    """
    <style>
        [data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display:none !important; }
        .block-container { max-width:760px; padding:1.1rem 1rem 4rem; }
        .ref-topbar { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1.65rem; }
        .ref-topbar-actions { display:flex; align-items:center; gap:.45rem; }
        .ref-brand { display:inline-flex; align-items:center; gap:.55rem; font-size:1rem; font-weight:850; color:var(--ink); }
        .ref-brand-icon { display:grid; place-items:center; width:2.15rem; height:2.15rem; border:1px solid var(--line); border-radius:50%; background:var(--icon-bg); }
        .ref-brand-icon svg { width:1.55rem; height:1.55rem; }
        .ref-theme-toggle { display:flex; gap:.35rem; }
        .ref-theme-link { display:inline-flex; align-items:center; justify-content:center; min-height:2.75rem; padding:.2rem .7rem; border:1px solid var(--line); border-radius:999px; background:var(--panel); color:var(--ink)!important; font-size:.78rem; font-weight:800; text-decoration:none!important; white-space:nowrap; }
        .ref-theme-link:hover, .ref-theme-link:focus-visible { border-color:var(--accent); background:var(--accent-soft); }
        .ref-theme-light, .ref-theme-dark { display:none; }
        .ref-theme-toggle.is-system .ref-theme-dark { display:inline-flex; }
        @media (prefers-color-scheme:dark) { .ref-theme-toggle.is-system .ref-theme-light { display:inline-flex; } .ref-theme-toggle.is-system .ref-theme-dark { display:none; } }
        .ref-back { display:inline-flex; flex:0 0 auto; align-items:center; justify-content:center; gap:.4rem; min-height:2.75rem; padding:.3rem .9rem; border:1px solid var(--accent); border-radius:999px; background:var(--accent); color:#fff!important; font-size:.84rem; font-weight:800; text-decoration:none!important; white-space:nowrap; }
        .ref-back:hover, .ref-back:focus-visible { border-color:#1d4fb2; background:#1d4fb2; }
        .ref-challenge { display:inline-flex; align-items:center; justify-content:center; gap:.35rem; min-height:2.75rem; padding:.2rem .75rem; border:1px solid var(--line); border-radius:999px; background:var(--panel); color:var(--ink)!important; font-size:.82rem; font-weight:800; text-decoration:none!important; white-space:nowrap; }
        .ref-hero { margin-bottom:1.1rem; }
        .ref-eyebrow { display:inline-block; margin:0 0 .45rem; padding:.25rem .5rem; border-radius:999px; background:var(--accent-soft); color:var(--accent); font-size:.72rem; font-weight:900; letter-spacing:.1em; text-transform:uppercase; }
        .ref-title { margin:0; color:var(--ink); font-size:clamp(1.8rem,7vw,2.6rem); font-weight:900; letter-spacing:-.045em; line-height:1.08; }
        .ref-intro { max-width:34rem; margin:.55rem 0 .8rem; color:var(--muted); font-size:.92rem; line-height:1.45; }
        .ref-pdf { display:inline-flex; align-items:center; justify-content:space-between; gap:1rem; min-height:2.75rem; padding:.5rem .8rem; border:1px solid var(--line); border-radius:12px; background:var(--panel); color:var(--accent)!important; font-size:.84rem; font-weight:800; text-decoration:none!important; }
        .ref-pdf:hover, .ref-pdf:focus-visible { border-color:var(--accent); background:var(--accent-soft); color:var(--accent)!important; }
        [data-testid="stTextInput"] { margin:1rem 0 .25rem; }
        [data-testid="stTextInput"] label { color:var(--ink)!important; font-weight:750; }
        [data-testid="stTextInput"] input { border-color:var(--line); background:var(--panel); color:var(--ink); }
        .ref-empty { margin:1rem 0; padding:1rem; border:1px solid var(--line); border-radius:14px; background:var(--panel); color:var(--muted); }
        .ref-exam { margin:1rem 0 1.15rem; padding:1rem; border:1px solid rgba(40,100,220,.18); border-radius:18px; background:linear-gradient(145deg,rgba(40,100,220,.07),var(--exam-bg) 72%); }
        .ref-exam h2 { margin:0 0 .65rem; color:var(--ink); font-size:1.08rem; font-weight:850; letter-spacing:-.025em; }
        .ref-exam ul { margin:0; padding-left:1.15rem; color:var(--ink); font-size:.88rem; line-height:1.5; }
        .ref-exam li + li { margin-top:.25rem; }
        .ref-exam blockquote { margin:.8rem 0 .45rem; padding:.6rem .75rem; border-left:3px solid var(--accent); border-radius:0 10px 10px 0; background:var(--quote-bg); color:var(--muted); font-size:.82rem; line-height:1.45; }
        .ref-exam blockquote p { margin:0; }
        .ref-exam-source { color:var(--accent)!important; font-size:.77rem; font-weight:750; text-decoration:none!important; }
        .ref-group { margin-top:1.1rem; }
        .ref-group-head { display:flex; align-items:baseline; justify-content:space-between; gap:.5rem; margin-bottom:.65rem; }
        .ref-group-head h2 { margin:0; color:var(--ink); font-size:1.25rem; font-weight:850; letter-spacing:-.035em; }
        .ref-group-head span { color:var(--muted); font-size:.8rem; font-weight:700; }
        .ref-grid { display:grid; gap:.6rem; }
        .ref-category { overflow:hidden; border:1px solid var(--line); border-radius:18px; background:var(--panel); box-shadow:0 5px 16px rgba(31,52,83,.06); }
        .ref-category[open] { border-color:rgba(40,100,220,.35); box-shadow:0 8px 22px rgba(40,100,220,.08); }
        .ref-category summary { display:flex; align-items:center; gap:.75rem; min-height:4.25rem; padding:.7rem .9rem; cursor:pointer; list-style:none; -webkit-tap-highlight-color:transparent; }
        .ref-category summary::-webkit-details-marker { display:none; }
        .ref-category summary:focus-visible, .ref-tech:focus-visible { outline:3px solid var(--accent); outline-offset:-2px; }
        .ref-category-icon { display:grid; flex:0 0 auto; place-items:center; width:2.35rem; height:2.35rem; border-radius:12px; background:var(--accent-soft); color:var(--accent); font-size:.85rem; font-weight:900; }
        .ref-category-text { display:grid; min-width:0; gap:.12rem; }
        .ref-category-name { color:var(--ink); font-size:.97rem; font-weight:850; line-height:1.15; }
        .ref-category-description { color:var(--muted); font-size:.75rem; line-height:1.2; }
        .ref-category-count { margin-left:auto; color:var(--muted); font-size:.8rem; font-weight:750; }
        .ref-category-chevron { color:var(--muted); font-size:1.15rem; transition:transform .15s ease; }
        .ref-category[open] .ref-category-chevron { transform:rotate(180deg); }
        .ref-techniques { border-top:1px solid var(--line); padding:0 .9rem .2rem 3.95rem; }
        .ref-tech { display:flex; align-items:center; justify-content:space-between; gap:.5rem; min-height:2.9rem; border-bottom:1px solid var(--divider); color:var(--ink)!important; font-size:.88rem; font-weight:650; text-decoration:none!important; }
        .ref-tech:last-child { border-bottom:0; }
        .ref-tech:hover { color:var(--accent)!important; }
        .ref-tech-arrow { color:var(--accent); font-size:1.1rem; }
        @media (min-width:700px) {
            .block-container { padding-top:2.5rem; }
            .ref-grid { grid-template-columns:repeat(2,minmax(0,1fr)); align-items:start; }
        }
        @media (max-width:360px) { .ref-category-description { display:none; } }
        @media (max-width:480px) { .ref-topbar-actions { gap:.3rem; } .ref-theme-link, .ref-challenge { width:2.75rem; padding:.2rem; font-size:1rem; } .ref-theme-label, .ref-back-label, .ref-challenge-label { display:none; } }
    </style>
    """,
    unsafe_allow_html=True,
)

def render_category(
    category: str,
    items: list[dict[str, str]],
    is_open: bool,
) -> str:
    links = []
    for item in items:
        query_params = {"category": category, "technique": item["name"]}
        if theme_mode != "system":
            query_params["theme"] = theme_mode
        query = escape(urlencode(query_params))
        links.append(
            f'<a class="ref-tech" href="/?{query}" target="_self">'
            f'<span>{escape(item["name"])}</span>'
            '<span class="ref-tech-arrow" aria-hidden="true">→</span></a>'
        )
    open_attribute = " open" if is_open else ""
    description = escape(DESCRIPTIONS.get(category, "Techniques de judo"))
    return (
        f'<details class="ref-category"{open_attribute}><summary>'
        f'<span class="ref-category-icon" aria-hidden="true">{escape(category[0].upper())}</span>'
        '<span class="ref-category-text">'
        f'<span class="ref-category-name">{escape(category)}</span>'
        f'<span class="ref-category-description">{description}</span></span>'
        f'<span class="ref-category-count">{len(items)}</span>'
        '<span class="ref-category-chevron" aria-hidden="true">⌄</span>'
        f'</summary><div class="ref-techniques">{"".join(links)}</div></details>'
    )


def render_group(
    title: str,
    categories: list[str],
    techniques: list[dict[str, str]],
    expand_matches: bool,
) -> str:
    if not categories:
        return ""
    count = sum(item["category"] in categories for item in techniques)
    cards = []
    for category in categories:
        items = sorted(
            (item for item in techniques if item["category"] == category),
            key=lambda item: item["name"],
        )
        cards.append(
            render_category(
                category,
                items,
                is_open=expand_matches or not cards,
            )
        )
    return (
        '<section class="ref-group"><div class="ref-group-head">'
        f'<h2>{escape(title)}</h2><span>{count} techniques</span></div>'
        f'<div class="ref-grid">{"".join(cards)}</div></section>'
    )


if theme_mode == "dark":
    theme_toggle_links = (
        '<a class="ref-theme-link" href="?theme=light" aria-label="Activer le thème clair">'
        '<span aria-hidden="true">☀</span><span class="ref-theme-label"> Clair</span></a>'
    )
    theme_toggle_class = ""
elif theme_mode == "light":
    theme_toggle_links = (
        '<a class="ref-theme-link" href="?theme=dark" aria-label="Activer le thème sombre">'
        '<span aria-hidden="true">☾</span><span class="ref-theme-label"> Sombre</span></a>'
    )
    theme_toggle_class = ""
else:
    theme_toggle_links = (
        '<a class="ref-theme-link ref-theme-light" href="?theme=light" aria-label="Activer le thème clair">'
        '<span aria-hidden="true">☀</span><span class="ref-theme-label"> Clair</span></a>'
        '<a class="ref-theme-link ref-theme-dark" href="?theme=dark" aria-label="Activer le thème sombre">'
        '<span aria-hidden="true">☾</span><span class="ref-theme-label"> Sombre</span></a>'
    )
    theme_toggle_class = " is-system"

st.markdown(
    f"""
    <div class="ref-topbar">
        <span class="ref-brand"><span class="ref-brand-icon" aria-hidden="true">{JUDO_MARK_SVG}</span>Gokyo</span>
        <div class="ref-topbar-actions">
            <nav class="ref-theme-toggle{theme_toggle_class}" aria-label="Thème">{theme_toggle_links}</nav>
            <a class="ref-challenge" href="/Defi_UV2{f'?theme={theme_mode}' if theme_mode != 'system' else ''}" target="_self" aria-label="Ouvrir le Défi UV2"><span aria-hidden="true">🎲</span><span class="ref-challenge-label"> Défi</span></a>
            <a class="ref-back" href="{f'/?theme={theme_mode}' if theme_mode != 'system' else '/'}" target="_self" aria-label="Retour à la révision"><span aria-hidden="true">←</span><span class="ref-back-label"> Réviser</span></a>
        </div>
    </div>
    <section class="ref-hero">
        <p class="ref-eyebrow">UV2 · 1er dan</p>
        <h1 class="ref-title">Référentiel UV2</h1>
        <p class="ref-intro">{len(TECHNIQUES)} techniques, classées par famille. Ouvre une famille pour choisir une technique.</p>
        <a class="ref-pdf" href="{escape(OFFICIAL_PDF_URL)}" target="_blank" rel="noopener noreferrer">
            <span>Annexe technique officielle</span><span aria-hidden="true">↗</span>
        </a>
    </section>
    """,
    unsafe_allow_html=True,
)


search_query = st.text_input(
    "Rechercher une technique ou une famille",
    placeholder="Ex. O-soto-gari",
    key="technique_search",
)
filtered_techniques = filter_techniques(TECHNIQUES, search_query)
has_search_query = bool(search_query.strip())
categories = list(dict.fromkeys(item["category"] for item in filtered_techniques))
standing = [category for category in categories if category not in GROUND_CATEGORIES]
ground = [category for category in categories if category in GROUND_CATEGORIES]

if filtered_techniques:
    st.markdown(
        render_group("Debout", standing, filtered_techniques, has_search_query)
        + render_group("Au sol", ground, filtered_techniques, has_search_query),
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<p class="ref-empty">Aucune technique ne correspond à cette recherche.</p>',
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <section class="ref-exam" aria-labelledby="ref-exam-title">
        <h2 id="ref-exam-title">Le jour de l’UV2</h2>
        <ul>
            <li>Le jury demande 6 techniques debout (nage-waza) et 4 au sol (ne-waza), une par une, en couvrant toutes les familles.</li>
            <li>Montre les projections en déplacement et les techniques au sol en situation d’étude (renversement ou position quadrupédique).</li>
            <li>Une méconnaissance est admise dans chacun des deux domaines. L’épreuve dure 5 minutes au maximum.</li>
        </ul>
        <blockquote><p>« Modalités : pour les techniques en nage-waza et ne-waza, le jury impose des techniques qui couvriront l’ensemble des familles. »</p></blockquote>
        <a class="ref-exam-source" href="{escape(OFFICIAL_RULES_URL)}" target="_blank" rel="noopener noreferrer">Texte exact · Textes officiels 2026/2027, règlement des grades, p. 98 ↗</a>
    </section>
    """,
    unsafe_allow_html=True,
)
