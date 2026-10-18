from html import escape
import json
from pathlib import Path

import streamlit as st

from judo_utils import draw_techniques_by_category, get_theme_styles


ROOT = Path(__file__).resolve().parent.parent
TECHNIQUES = json.loads((ROOT / "techniques.json").read_text(encoding="utf-8"))
GROUND_CATEGORIES = {"Osaekomi", "Shime waza", "Kansetsu waza"}
ALL_CATEGORIES = list(dict.fromkeys(item["category"] for item in TECHNIQUES))
STANDING_CATEGORIES = [
    category for category in ALL_CATEGORIES if category not in GROUND_CATEGORIES
]
GROUND_CATEGORY_ORDER = [
    category for category in ALL_CATEGORIES if category in GROUND_CATEGORIES
]

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
        .challenge-link-primary {{
            border-color:var(--accent); background:var(--accent); color:#fff!important;
        }}
        .challenge-link-primary:hover,
        .challenge-link-primary:focus-visible {{
            background:#1d4fb2;
        }}
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
            gap:.55rem; margin:0; padding:0; list-style:none;
        }}
        .draw-item {{
            display:flex; align-items:center; gap:.65rem;
            min-height:3rem; padding:.55rem .7rem;
            border:1px solid var(--line); border-radius:12px;
            color:var(--ink); font-size:.9rem; font-weight:700;
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

theme_query = f"?theme={theme_mode}" if theme_mode != "system" else ""

st.markdown(
    f"""
    <header class="challenge-header">
        <span class="challenge-brand">Gokyo</span>
        <div class="challenge-actions">
            <nav class="challenge-theme-toggle{theme_toggle_class}" aria-label="Thème">{theme_toggle_links}</nav>
            <a class="challenge-link challenge-link-primary" href="/{theme_query}" target="_self" aria-label="Retour à la révision">
                <span aria-hidden="true">←</span><span class="challenge-link-label"> Réviser</span>
            </a>
            <a class="challenge-link" href="/Referentiel{theme_query}" target="_self" aria-label="Ouvrir le Référentiel">
                <span aria-hidden="true">☷</span><span class="challenge-link-label"> Référentiel</span>
            </a>
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
            f'<li class="draw-item"><span class="draw-number">{index}</span>'
            f'<span>{escape(technique["name"].replace("-", " "))}</span></li>'
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
