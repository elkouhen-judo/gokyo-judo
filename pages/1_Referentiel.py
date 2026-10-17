import json
from html import escape
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
TECHNIQUES = json.loads((ROOT / "techniques.json").read_text(encoding="utf-8"))
JUDO_MARK_SVG = (ROOT / "assets/judo_mark.svg").read_text(encoding="utf-8")
OFFICIAL_PDF_URL = (
    "https://www.ffjudo.com/resource-file/document/"
    "1789035361_068de2d2976847c37f5a.pdf"
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
    page_title="Référentiel des prises - Gokyo",
    page_icon="🥋",
    layout="centered",
)

st.markdown(
    """
    <style>
        :root { --ink:#1c1b1a; --muted:#69645e; --paper:#faf8f3; --red:#ad2528; --line:#e7e1d8; }
        .stApp { background:var(--paper); color:var(--ink); }
        [data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display:none !important; }
        .block-container { max-width:760px; padding:1.1rem 1rem 4rem; }
        .ref-topbar { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:1.65rem; }
        .ref-brand { display:inline-flex; align-items:center; gap:.55rem; font-size:1rem; font-weight:850; color:var(--ink); }
        .ref-brand-icon { display:grid; place-items:center; width:2.15rem; height:2.15rem; border:1px solid var(--line); border-radius:50%; background:#fff; }
        .ref-brand-icon svg { width:1.55rem; height:1.55rem; }
        .ref-back { display:inline-flex; align-items:center; justify-content:center; min-height:2.75rem; padding:.3rem .9rem; border:1px solid var(--line); border-radius:999px; background:#fff; color:var(--ink)!important; font-size:.84rem; font-weight:750; text-decoration:none!important; }
        .ref-back:hover, .ref-back:focus-visible { border-color:var(--red); }
        .ref-hero { margin-bottom:2rem; }
        .ref-eyebrow { margin:0 0 .5rem; color:var(--red); font-size:.72rem; font-weight:850; letter-spacing:.12em; text-transform:uppercase; }
        .ref-title { margin:0; color:var(--ink); font-size:clamp(2rem,8vw,3.3rem); font-weight:900; letter-spacing:-.055em; line-height:1.06; }
        .ref-intro { max-width:34rem; margin:.75rem 0 1.1rem; color:var(--muted); font-size:.96rem; line-height:1.5; }
        .ref-pdf { display:inline-flex; align-items:center; justify-content:space-between; gap:1rem; min-height:2.9rem; padding:.65rem .9rem; border-radius:10px; background:var(--ink); color:#fff!important; font-size:.88rem; font-weight:750; text-decoration:none!important; }
        .ref-pdf:hover, .ref-pdf:focus-visible { background:var(--red); color:#fff!important; }
        .ref-group { margin-top:1.8rem; }
        .ref-group-head { display:flex; align-items:baseline; justify-content:space-between; gap:.5rem; margin-bottom:.65rem; }
        .ref-group-head h2 { margin:0; color:var(--ink); font-size:1.35rem; font-weight:850; letter-spacing:-.035em; }
        .ref-group-head span { color:var(--muted); font-size:.8rem; font-weight:700; }
        .ref-grid { display:grid; gap:.6rem; }
        .ref-category { overflow:hidden; border:1px solid var(--line); border-radius:13px; background:#fff; box-shadow:0 3px 12px rgba(33,24,18,.035); }
        .ref-category[open] { border-color:#d8cbc0; }
        .ref-category summary { display:flex; align-items:center; gap:.75rem; min-height:4.25rem; padding:.7rem .9rem; cursor:pointer; list-style:none; -webkit-tap-highlight-color:transparent; }
        .ref-category summary::-webkit-details-marker { display:none; }
        .ref-category summary:focus-visible, .ref-tech:focus-visible { outline:2px solid var(--red); outline-offset:-2px; }
        .ref-category-icon { display:grid; flex:0 0 auto; place-items:center; width:2.35rem; height:2.35rem; border-radius:9px; background:#f8eeee; color:var(--red); font-size:.85rem; font-weight:900; }
        .ref-category-text { display:grid; min-width:0; gap:.12rem; }
        .ref-category-name { color:var(--ink); font-size:.97rem; font-weight:850; line-height:1.15; }
        .ref-category-description { color:var(--muted); font-size:.75rem; line-height:1.2; }
        .ref-category-count { margin-left:auto; color:var(--muted); font-size:.8rem; font-weight:750; }
        .ref-category-chevron { color:var(--muted); font-size:1.15rem; transition:transform .15s ease; }
        .ref-category[open] .ref-category-chevron { transform:rotate(180deg); }
        .ref-techniques { border-top:1px solid var(--line); padding:0 .9rem .2rem 3.95rem; }
        .ref-tech { display:flex; align-items:center; justify-content:space-between; gap:.5rem; min-height:2.9rem; border-bottom:1px solid #f0ece7; color:var(--ink)!important; font-size:.88rem; font-weight:650; text-decoration:none!important; }
        .ref-tech:last-child { border-bottom:0; }
        .ref-tech:hover { color:var(--red)!important; }
        .ref-tech-arrow { color:var(--red); font-size:1.1rem; }
        @media (min-width:700px) {
            .block-container { padding-top:2.5rem; }
            .ref-grid { grid-template-columns:repeat(2,minmax(0,1fr)); align-items:start; }
        }
        @media (max-width:360px) { .ref-category-description { display:none; } }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_category(category: str, is_open: bool) -> str:
    items = sorted(
        (item for item in TECHNIQUES if item["category"] == category),
        key=lambda item: item["name"],
    )
    links = []
    for item in items:
        query = escape(urlencode({"category": category, "technique": item["name"]}))
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


def render_group(title: str, categories: list[str]) -> str:
    if not categories:
        return ""
    count = sum(item["category"] in categories for item in TECHNIQUES)
    cards = "".join(
        render_category(category, is_open=index == 0)
        for index, category in enumerate(categories)
    )
    return (
        '<section class="ref-group"><div class="ref-group-head">'
        f'<h2>{escape(title)}</h2><span>{count} prises</span></div>'
        f'<div class="ref-grid">{cards}</div></section>'
    )


categories = list(dict.fromkeys(item["category"] for item in TECHNIQUES))
standing = [category for category in categories if category not in GROUND_CATEGORIES]
ground = [category for category in categories if category in GROUND_CATEGORIES]

st.markdown(
    f"""
    <div class="ref-topbar">
        <span class="ref-brand"><span class="ref-brand-icon" aria-hidden="true">{JUDO_MARK_SVG}</span>Gokyo</span>
        <a class="ref-back" href="/" target="_self">← Réviser</a>
    </div>
    <main>
        <section class="ref-hero">
            <p class="ref-eyebrow">UV2 · 1er dan</p>
            <h1 class="ref-title">Toutes les prises<br>à réviser</h1>
            <p class="ref-intro">{len(TECHNIQUES)} prises, classées par famille. Ouvre une famille puis touche une prise pour voir sa fiche et sa vidéo.</p>
            <a class="ref-pdf" href="{escape(OFFICIAL_PDF_URL)}" target="_blank" rel="noopener noreferrer">
                <span>📄 &nbsp; PDF officiel de France Judo</span><span aria-hidden="true">↗</span>
            </a>
        </section>
        {render_group("Debout", standing)}
        {render_group("Au sol", ground)}
    </main>
    """,
    unsafe_allow_html=True,
)
