from html import escape
import base64
from functools import lru_cache
import json
from pathlib import Path

import streamlit as st

from judo_utils import draw_techniques_by_category, get_theme_styles, nav_links_html


ROOT = Path(__file__).resolve().parent.parent
TECHNIQUES = json.loads((ROOT / "techniques.json").read_text(encoding="utf-8"))
IMAGES_PATH = ROOT / "assets" / "techniques"
GROUND_CATEGORIES = {"Osaekomi", "Shime waza", "Kansetsu waza"}
ALL_CATEGORIES = list(dict.fromkeys(item["category"] for item in TECHNIQUES))
STANDING_CATEGORIES = [
    category for category in ALL_CATEGORIES if category not in GROUND_CATEGORIES
]
GROUND_CATEGORY_ORDER = [
    category for category in ALL_CATEGORIES if category in GROUND_CATEGORIES
]


@lru_cache(maxsize=None)
def technique_image_uri(name: str) -> str | None:
    path = IMAGES_PATH / f"{name.lower()}.jpg"
    if not path.exists():
        return None
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def draw_item_html(index: int, technique: dict) -> str:
    label = escape(technique["name"].replace("-", " "))
    number = f'<span class="draw-number">{index}</span>'
    image = technique_image_uri(technique["name"])
    if image is None:
        return f'<li class="draw-item"><div class="draw-row">{number}<span>{label}</span></div></li>'
    return (
        f'<li class="draw-item"><details>'
        f'<summary class="draw-row">{number}<span class="draw-name">{label}</span>'
        f'<span class="draw-help">💡 Aide</span></summary>'
        f'<img class="draw-photo" src="{image}" alt="Photo de {label}" loading="lazy">'
        f'</details></li>'
    )

st.set_page_config(
    page_title="Défi UV2 - Gokyo",
    page_icon="🥋",
    layout="centered",
)

theme_mode = st.query_params.get("theme", "system")
if theme_mode not in {"dark", "light"}:
    theme_mode = "system"

st.markdown(get_theme_styles(theme_mode), unsafe_allow_html=True)
st.markdown(
    f"""
    <style>
        [data-testid="stHeader"], [data-testid="stToolbar"],
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {{
            display:none !important;
        }}
        .block-container {{ max-width:760px; padding:1.1rem 1rem 3rem; }}
        .challenge-header {{
            display:flex; align-items:center; justify-content:space-between;
            gap:.7rem; margin:0 0 1.5rem;
        }}
        .challenge-brand {{ color:var(--ink); font-weight:850; font-size:1rem; }}
        .challenge-actions {{ display:flex; align-items:center; gap:.4rem; }}
        .challenge-link {{
            display:inline-flex; align-items:center; justify-content:center;
            min-height:2.75rem; padding:.2rem .8rem;
            border:1px solid var(--line); border-radius:999px;
            background:var(--panel); color:var(--ink)!important;
            font-size:.82rem; font-weight:800; text-decoration:none!important;
            white-space:nowrap;
        }}
        .challenge-theme-toggle {{ display:flex; gap:.25rem; }}
        .challenge-theme-light, .challenge-theme-dark {{ display:none; }}
        .challenge-theme-toggle.is-system .challenge-theme-dark {{ display:inline-flex; }}
        @media (prefers-color-scheme:dark) {{
            .challenge-theme-toggle.is-system .challenge-theme-light {{ display:inline-flex; }}
            .challenge-theme-toggle.is-system .challenge-theme-dark {{ display:none; }}
        }}
        .challenge-hero {{ margin:0 0 1.25rem; }}
        .challenge-kicker {{
            margin:0 0 .4rem; color:var(--accent); font-size:.74rem;
            font-weight:900; letter-spacing:.1em; text-transform:uppercase;
        }}
        .challenge-title {{
            margin:0; color:var(--ink); font-size:clamp(2rem,8vw,2.7rem);
            font-weight:900; letter-spacing:-.045em; line-height:1.05;
        }}
        .challenge-intro {{
            max-width:38rem; margin:.65rem 0 0; color:var(--muted);
            font-size:.96rem; line-height:1.5;
        }}
        .draw-instructions {{
            margin:0 0 1rem; padding:.85rem 1rem;
            border:1px solid var(--line); border-radius:14px;
            background:var(--panel); color:var(--muted);
            font-size:.88rem; line-height:1.5;
        }}
        .draw-instructions strong {{ color:var(--ink); }}
        [data-testid="stButton"] button {{
            min-height:3rem; border-radius:999px; font-weight:850;
        }}
        .draw-section {{
            margin:1rem 0; padding:1rem;
            border:1px solid var(--line); border-radius:18px;
            background:var(--panel); box-shadow:var(--shadow-soft);
        }}
        .draw-section h2 {{
            margin:0 0 .75rem; color:var(--ink);
            font-size:1.15rem; font-weight:850;
        }}
        .draw-list {{
            display:grid; grid-template-columns:repeat(2,minmax(0,1fr));
            gap:.55rem; margin:0 !important; padding:0 !important; list-style:none;
        }}
        .draw-list {{ align-items:start; }}
        .draw-item {{
            margin:0 !important; padding:0 !important;
            border:1px solid var(--line); border-radius:12px;
            color:var(--ink); font-size:.9rem; font-weight:700;
        }}
        .draw-row {{
            display:flex; align-items:center; gap:.65rem;
            min-height:3rem; padding:.55rem .7rem; list-style:none; cursor:pointer;
        }}
        .draw-row::-webkit-details-marker {{ display:none; }}
        .draw-name {{ flex:1 1 auto; }}
        .draw-help {{
            flex:0 0 auto; padding:.25rem .6rem; border-radius:999px;
            background:var(--accent-soft); color:var(--accent);
            font-size:.75rem; font-weight:800;
        }}
        details[open] .draw-help {{ background:var(--accent); color:#fff; }}
        .draw-photo {{
            display:block; width:100%; max-height:22rem; object-fit:contain;
            border-radius:0 0 11px 11px; background:var(--surface);
        }}
        .draw-number {{
            display:grid; flex:0 0 auto; place-items:center;
            width:1.65rem; height:1.65rem; border-radius:50%;
            background:var(--accent-soft); color:var(--accent);
            font-size:.78rem; font-weight:900;
        }}
        .draw-empty {{
            margin:0; padding:1rem; border:1px dashed var(--line);
            border-radius:14px; color:var(--muted); line-height:1.5;
        }}
        @media (max-width:480px) {{
            .challenge-header {{ gap:.4rem; }}
            .challenge-actions {{ gap:.25rem; }}
            .challenge-link {{ width:2.75rem; padding:.2rem; font-size:1rem; }}
            .challenge-link-label {{ display:none; }}
            .draw-list {{ grid-template-columns:1fr; }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

if theme_mode == "dark":
    theme_toggle_links = (
        '<a class="challenge-link" href="?theme=light" '
        'aria-label="Activer le thème clair">☀</a>'
    )
    theme_toggle_class = ""
elif theme_mode == "light":
    theme_toggle_links = (
        '<a class="challenge-link" href="?theme=dark" '
        'aria-label="Activer le thème sombre">☾</a>'
    )
    theme_toggle_class = ""
else:
    theme_toggle_links = (
        '<a class="challenge-link challenge-theme-light" href="?theme=light" '
        'aria-label="Activer le thème clair">☀</a>'
        '<a class="challenge-link challenge-theme-dark" href="?theme=dark" '
        'aria-label="Activer le thème sombre">☾</a>'
    )
    theme_toggle_class = " is-system"

st.markdown(
    f"""
    <header class="challenge-header">
        <span class="challenge-brand">Gokyo</span>
        <div class="challenge-actions">
            <nav class="challenge-theme-toggle{theme_toggle_class}" aria-label="Thème">{theme_toggle_links}</nav>
            {nav_links_html("uv2", theme_mode)}
        </div>
    </header>
    <section class="challenge-hero">
        <p class="challenge-kicker">Entraînement à l’examen</p>
        <h1 class="challenge-title">Défi UV2</h1>
        <p class="challenge-intro">Tire les techniques comme le jour de l’examen, puis essaie de les réaliser dans ton dojo.</p>
    </section>
    <p class="draw-instructions">
        <strong>Le tirage :</strong> 6 techniques debout et 4 au sol.
        Chaque famille est représentée. Pas de chrono ni de score : à toi de jouer.
    </p>
    """,
    unsafe_allow_html=True,
)

if st.button(
    "🎲  Nouveau tirage",
    type="primary",
    use_container_width=True,
    key="draw_uv2_exam",
):
    st.session_state.exam_draw = {
        "standing": draw_techniques_by_category(
            TECHNIQUES,
            STANDING_CATEGORIES,
            6,
        ),
        "ground": draw_techniques_by_category(
            TECHNIQUES,
            GROUND_CATEGORY_ORDER,
            4,
        ),
    }

exam_draw = st.session_state.get("exam_draw")
if exam_draw is None:
    st.markdown(
        '<p class="draw-empty">Appuie sur « Nouveau tirage » pour obtenir tes 10 techniques.</p>',
        unsafe_allow_html=True,
    )
else:
    for title, key in (("Debout · 6 techniques", "standing"), ("Au sol · 4 techniques", "ground")):
        techniques = exam_draw[key]
        items = "".join(
            draw_item_html(index, technique)
            for index, technique in enumerate(techniques, start=1)
        )
        st.markdown(
            f"""
            <section class="draw-section" aria-label="{title}">
                <h2>{title}</h2>
                <ol class="draw-list">{items}</ol>
            </section>
            """,
            unsafe_allow_html=True,
        )
