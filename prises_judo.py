from html import escape
import json
from pathlib import Path
from urllib.parse import quote

import streamlit as st

from judo_utils import extract_youtube_id, get_theme_styles, nav_links_html

ASSETS_PATH = Path(__file__).with_name("assets")
JUDO_MARK_ICON_PATH = ASSETS_PATH / "judo_mark.svg"
JUDO_MARK_SVG = JUDO_MARK_ICON_PATH.read_text(encoding="utf-8").replace("\n", "").replace("\r", "")

st.set_page_config(
    page_title="Gokyo - nomenclature judo",
    page_icon="🥋",
    layout="wide",
)

DATA_PATH = Path(__file__).with_name("techniques.json")
JUDO_TECHNIQUES = json.loads(DATA_PATH.read_text(encoding="utf-8"))
theme_mode = st.query_params.get("theme", "system")
if theme_mode not in {"dark", "light"}:
    theme_mode = "system"

st.markdown(get_theme_styles(theme_mode), unsafe_allow_html=True)
st.markdown(
    """
    <style>
        .block-container {
            max-width: 820px;
            padding: 0.85rem 1rem 2.25rem;
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }

        .app-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            margin: 0.15rem 0 1rem;
        }

        .app-header .app-title {
            flex-wrap: nowrap;
            margin: 0;
            font-size: 1.45rem !important;
        }

        .app-header .app-title-mark {
            width: 2.35rem;
            height: 2.35rem;
        }

        .app-header .app-title-text {
            transform: none;
            white-space: nowrap;
        }

        .app-header-actions {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            flex: 0 0 auto;
        }

        .app-theme-toggle {
            display: flex;
            gap: 0.35rem;
        }

        .app-theme-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 2.75rem;
            padding: 0.2rem 0.7rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: var(--panel);
            color: var(--ink) !important;
            font-size: 0.78rem;
            font-weight: 800;
            text-decoration: none !important;
            white-space: nowrap;
        }

        .app-theme-link:hover,
        .app-theme-link:focus-visible {
            border-color: var(--accent);
            background: var(--accent-soft);
        }

        .app-theme-light,
        .app-theme-dark {
            display: none;
        }

        .app-theme-toggle.is-system .app-theme-dark {
            display: inline-flex;
        }

        @media (prefers-color-scheme: dark) {
            .app-theme-toggle.is-system .app-theme-light {
                display: inline-flex;
            }

            .app-theme-toggle.is-system .app-theme-dark {
                display: none;
            }
        }

        .tech-panel {
            position: relative;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: var(--panel);
            box-shadow: var(--shadow-soft);
            margin-top: 0.65rem;
            padding: 0.9rem;
        }

        .technique-name {
            display: block;
            margin: 0 0 0.25rem;
            color: var(--ink);
            font-size: 1.45rem !important;
            font-weight: 850 !important;
            line-height: 1.12 !important;
            letter-spacing: 0 !important;
        }

        .technique-position {
            margin-left: 0.35rem;
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 750;
            white-space: nowrap;
            vertical-align: middle;
        }

        .video-wrapper {
            position: relative;
            width: 100%;
            aspect-ratio: 16 / 9;
            overflow: hidden;
            background: #12100f;
            border-radius: 16px;
            box-shadow: 0 12px 24px rgba(31, 26, 18, 0.16);
        }

        .video-frame {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }

        .app-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 0 0 0.8rem;
            color: var(--ink);
            font-size: 1.65rem !important;
            font-weight: 850 !important;
            line-height: normal !important;
            letter-spacing: 0 !important;
        }

        .app-title-text {
            display: inline-flex;
            align-items: center;
            transform: translateY(2px);
        }

        .app-title-mark {
            display: inline-grid;
            place-items: center;
            flex: 0 0 auto;
            width: 2.7rem;
            height: 2.7rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: var(--icon-bg);
            box-shadow: 0 6px 14px rgba(42, 35, 24, 0.08);
            line-height: 1;
        }

        .app-title-mark svg {
            width: 1.84rem;
            height: 1.84rem;
            display: block;
        }

        .app-title-mark svg polygon {
            fill: #ffffff !important;
            stroke: var(--icon-outline) !important;
        }

        .app-title-mark svg circle {
            fill: #2864dc !important;
        }

        .tech-description {
            display: block;
            margin: 0 0 0.75rem;
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .stSelectbox div[data-baseweb="select"] > div {
            min-height: 3.1rem;
            border: 1px solid var(--line);
            border-radius: 16px;
            background: linear-gradient(180deg, var(--field-bg) 0%, var(--field-bg-end) 100%);
            box-shadow: 0 5px 14px rgba(31, 52, 83, 0.07);
            transition: border-color 140ms ease, box-shadow 140ms ease;
        }

        .stSelectbox div[data-baseweb="select"] > div:hover {
            border-color: rgba(40, 100, 220, 0.42);
            box-shadow: 0 7px 18px rgba(31, 52, 83, 0.1);
        }

        .stSelectbox div[data-baseweb="select"] > div:focus-within {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-soft);
        }

        .stSelectbox div[data-baseweb="select"] [role="combobox"],
        .stSelectbox div[data-baseweb="select"] span {
            white-space: nowrap !important;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .stSelectbox div[data-baseweb="select"] span,
        .stSelectbox div[data-baseweb="select"] input,
        .stSelectbox div[data-baseweb="select"] div,
        .stSelectbox div[data-baseweb="select"] svg {
            color: var(--ink) !important;
            fill: var(--ink) !important;
        }

        .stSelectbox div[data-baseweb="select"] svg {
            color: var(--accent) !important;
            fill: var(--accent) !important;
        }

        .stSelectbox div[data-baseweb="select"] input::placeholder {
            color: var(--muted) !important;
        }

        .stSelectbox [data-baseweb="select"] [aria-selected="true"],
        .stSelectbox [data-baseweb="select"] [data-baseweb="tag"] {
            color: var(--ink) !important;
        }

        .stSelectbox div[data-baseweb="select"] {
            min-height: 3.1rem;
        }

        .stSelectbox div[data-baseweb="select"] > div {
            align-items: center;
            min-height: 3.1rem;
        }

        .stSelectbox input {
            caret-color: transparent;
        }

        .stSelectbox {
            margin-bottom: 0.65rem;
        }

        .stSelectbox label {
            margin: 0 0 0.35rem;
            color: var(--ink) !important;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.025em;
        }

        div[data-baseweb="popover"] > div {
            overflow: hidden;
            border: 1px solid var(--line) !important;
            border-radius: 16px !important;
            background: var(--menu-bg);
            box-shadow: 0 14px 32px rgba(31, 52, 83, 0.16) !important;
        }

        [role="listbox"] {
            padding: 0.35rem !important;
            background: var(--menu-bg);
        }

        [role="option"] {
            min-height: 2.75rem !important;
            margin: 0.12rem 0;
            border-radius: 10px !important;
            color: var(--ink) !important;
            font-weight: 600;
            cursor: pointer;
        }

        [role="option"][aria-selected="true"],
        [role="option"]:hover {
            background: var(--accent-soft) !important;
            color: var(--accent) !important;
            font-weight: 800;
        }

        .field-label {
            display: block;
            margin: 0 0 0.32rem;
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0;
        }

        .st-key-landscape_previous_button,
        .st-key-landscape_next_button {
            display: none !important;
        }

        .stVerticalBlock {
            padding: 0 !important;
        }

        [data-testid="stElementContainer"]:has(iframe[height="0"]) {
            display: none;
        }

        .landscape-nav {
            display: none;
        }

        .standard-navigation-label {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 2.7rem;
            min-width: 4.3rem;
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 800;
            line-height: 1;
            text-align: center;
        }

        .standard-navigation {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.48rem;
            width: fit-content;
            max-width: 100%;
            margin: 0.85rem auto 0;
            padding: 0.32rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: var(--navigation-bg);
            box-shadow: var(--shadow-soft);
        }

        .standard-nav-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2.7rem;
            height: 2.7rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            background: var(--navigation-button-bg);
            color: var(--ink) !important;
            box-shadow: 0 7px 16px rgba(42, 35, 24, 0.07);
            font-size: 1.35rem;
            font-weight: 750;
            line-height: 1;
            text-decoration: none !important;
            -webkit-tap-highlight-color: transparent;
        }

        .standard-nav-button:hover,
        .standard-nav-button:focus,
        .standard-nav-button:active {
            border-color: rgba(40, 100, 220, 0.35);
            background: var(--accent-soft);
            color: var(--accent) !important;
            box-shadow: 0 7px 16px rgba(42, 35, 24, 0.08);
        }

        .tech-panel .standard-navigation {
            position: absolute;
            top: 0.55rem;
            right: 0.55rem;
            margin: 0;
            gap: 0.34rem;
            padding: 0.22rem;
            border: 0;
            background: transparent;
            box-shadow: none;
            z-index: 2;
        }

        .tech-panel .standard-nav-button {
            width: 2.32rem;
            height: 2.32rem;
            border: 0;
            background: transparent;
            box-shadow: none;
            font-size: 1.18rem;
        }

        .tech-panel .standard-nav-button:hover,
        .tech-panel .standard-nav-button:focus,
        .tech-panel .standard-nav-button:active {
            border: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        .tech-panel .technique-name {
            min-height: 2.85rem;
            padding-right: 6.2rem;
        }

        @media (orientation: landscape) and (max-width: 950px) and (max-height: 500px) and (pointer: coarse) {
            .block-container {
                max-width: 100% !important;
                padding: 0 !important;
            }

            [data-testid="stElementContainer"]:has(.app-title),
            [data-testid="stElementContainer"]:has(.field-label),
            [data-testid="stElementContainer"]:has(.stSelectbox) {
                display: none !important;
            }

            .tech-panel {
                margin: 0;
                padding: 0;
                border: none;
                border-radius: 0;
                background: transparent;
                box-shadow: none;
            }

            .tech-panel .technique-name,
            .tech-panel .tech-description {
                display: none;
            }

            .video-wrapper {
                position: fixed !important;
                inset: 0 !important;
                aspect-ratio: auto !important;
                width: 100vw !important;
                height: 100vh !important;
                height: 100dvh !important;
                max-width: 100vw !important;
                margin: 0 !important;
                border-radius: 0 !important;
                box-shadow: none !important;
                z-index: 9000 !important;
                background: #000 !important;
            }

            .st-key-landscape_previous_button,
            .st-key-landscape_next_button {
                display: block !important;
                position: fixed;
                top: auto;
                bottom: calc(env(safe-area-inset-bottom, 0px) + 4.25rem);
                z-index: 9999;
            }

            .standard-navigation {
                display: none !important;
            }

            .st-key-landscape_previous_button {
                left: calc(env(safe-area-inset-left, 0px) + 1rem);
                right: auto;
            }

            .st-key-landscape_next_button {
                left: auto;
                right: calc(env(safe-area-inset-right, 0px) + 1rem);
            }

            .st-key-landscape_previous_button .stButton,
            .st-key-landscape_next_button .stButton {
                display: block;
            }

            .st-key-landscape_previous_button button,
            .st-key-landscape_next_button button {
                width: 3.5rem;
                height: 3.5rem;
                min-width: 3.5rem;
                padding: 0;
                background: var(--landscape-nav-bg) !important;
                backdrop-filter: blur(4px);
                border: 0;
                border-radius: 999px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                font-size: 1.6rem;
                line-height: 1;
                color: var(--ink) !important;
                opacity: 1 !important;
                transform: none !important;
                -webkit-tap-highlight-color: transparent;
            }

            .st-key-landscape_previous_button button:hover,
            .st-key-landscape_next_button button:hover,
            .st-key-landscape_previous_button button:focus,
            .st-key-landscape_next_button button:focus,
            .st-key-landscape_previous_button button:focus-visible,
            .st-key-landscape_next_button button:focus-visible,
            .st-key-landscape_previous_button button:active,
            .st-key-landscape_next_button button:active,
            .st-key-landscape_previous_button button:disabled,
            .st-key-landscape_next_button button:disabled {
                background: var(--landscape-nav-bg) !important;
                color: var(--ink) !important;
                opacity: 1 !important;
                border: 0 !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
                transform: none !important;
            }

            .landscape-nav {
                display: block;
            }

            .landscape-nav-state {
                display: none;
            }

            .landscape-nav-toggle,
            .landscape-nav-close {
                position: fixed;
                z-index: 10020;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 2.75rem;
                height: 2.75rem;
                border: 0;
                border-radius: 999px;
                background: var(--landscape-nav-bg);
                color: var(--ink);
                box-shadow: 0 8px 20px rgba(20, 16, 12, 0.18);
                font-size: 1.08rem;
                font-weight: 800;
                line-height: 1;
                text-decoration: none;
                -webkit-tap-highlight-color: transparent;
            }

            .landscape-nav-toggle {
                top: calc(env(safe-area-inset-top, 0px) + 0.75rem);
                left: calc(env(safe-area-inset-left, 0px) + 0.75rem);
                transform: none;
            }

            .landscape-nav-close {
                top: calc(env(safe-area-inset-top, 0px) + 0.75rem);
                left: calc(env(safe-area-inset-left, 0px) + 0.75rem);
            }

            .landscape-nav-panel {
                position: fixed;
                top: calc(env(safe-area-inset-top, 0px) + 0.5rem);
                left: calc(env(safe-area-inset-left, 0px) + 0.5rem);
                bottom: calc(env(safe-area-inset-bottom, 0px) + 0.5rem);
                z-index: 10010;
                display: none;
                width: min(22rem, calc(100vw - 7.25rem));
                padding: 3.7rem 0.75rem 0.75rem;
                overflow: auto;
                border: 1px solid var(--line);
                border-radius: 8px;
                background: var(--landscape-nav-bg);
                backdrop-filter: blur(8px);
                box-shadow: 0 12px 32px rgba(20, 16, 12, 0.18);
            }

            .landscape-nav-state:checked ~ .landscape-nav-toggle {
                display: none;
            }

            .landscape-nav-state:checked ~ .landscape-nav-panel {
                display: block;
            }

            .landscape-nav-categories {
                display: flex;
                gap: 0.45rem;
                margin-bottom: 0.75rem;
                overflow-x: auto;
                padding-bottom: 0.15rem;
            }

            .landscape-nav-category,
            .landscape-nav-technique {
                display: inline-flex;
                align-items: center;
                border: 1px solid var(--line);
                color: var(--ink) !important;
                text-decoration: none !important;
                -webkit-tap-highlight-color: transparent;
            }

            .landscape-nav-category {
                flex: 0 0 auto;
                min-height: 2rem;
                padding: 0 0.7rem;
                border-radius: 999px;
                background: var(--field-bg);
                font-size: 0.82rem;
                font-weight: 700;
                white-space: nowrap;
            }

            .landscape-nav-category.is-active {
                border-color: rgba(40, 100, 220, 0.35);
                background: var(--accent-soft);
                color: var(--accent) !important;
            }

            .landscape-nav-techniques {
                display: grid;
                gap: 0.38rem;
            }

            .landscape-nav-technique {
                min-height: 2.25rem;
                padding: 0.4rem 0.65rem;
                border-radius: 8px;
                background: var(--field-bg);
                font-size: 0.92rem;
                font-weight: 650;
            }

            .landscape-nav-technique.is-active {
                border-color: rgba(40, 100, 220, 0.35);
                background: var(--accent-soft);
                color: var(--accent) !important;
            }
        }

        @media (max-width: 480px) and (orientation: portrait) {
            .block-container {
                padding: 0.7rem 0.65rem 2rem;
            }
        }

        @media (max-width: 360px) {
            .app-header .app-title-mark {
                display: none;
            }
        }

        @media (max-width: 480px) {
            .app-header-actions {
                gap: 0.3rem;
            }

            .app-theme-link {
                width: 2.75rem;
                padding: 0.2rem;
                font-size: 1rem;
            }

            .app-theme-link .theme-label {
                display: none;
            }
        }

        @media (max-width: 360px) {
            .app-header .app-title-text {
                font-size: 1.15rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

categories = list(dict.fromkeys(technique["category"] for technique in JUDO_TECHNIQUES))


def get_category_techniques(category: str) -> list[dict[str, str]]:
    return sorted(
        [
            technique
            for technique in JUDO_TECHNIQUES
            if technique["category"] == category
        ],
        key=lambda technique: format_technique_name(technique["name"]),
    )


def format_technique_name(name: str) -> str:
    return name.replace("-", " ")


def reset_selected_name() -> None:
    category_techniques = get_category_techniques(st.session_state.selected_category)
    st.session_state.selected_name = category_techniques[0]["name"]
    sync_selection_query_params(
        st.session_state.selected_category,
        st.session_state.selected_name,
    )


def select_technique(name: str) -> None:
    st.session_state.selected_name = name
    sync_selection_query_params(st.session_state.selected_category, name)


def sync_selected_name() -> None:
    sync_selection_query_params(
        st.session_state.selected_category,
        st.session_state.selected_name,
    )


def sync_selection_query_params(category: str, name: str) -> None:
    st.query_params["category"] = category
    st.query_params["technique"] = name


def get_selection_url(category: str, name: str) -> str:
    query = f"category={quote(category)}&technique={quote(name)}"
    if theme_mode != "system":
        query += f"&theme={theme_mode}"
    return f"?{query}"


def render_landscape_navigation_overlay(
    selected_category: str,
    selected_name: str,
    selected_category_techniques: list[dict[str, str]],
) -> None:
    category_links = []
    for category in categories:
        category_first_technique = get_category_techniques(category)[0]["name"]
        active_class = " is-active" if category == selected_category else ""
        category_links.append(
            f'<a class="landscape-nav-category{active_class}" '
            f'href="{escape(get_selection_url(category, category_first_technique))}" '
            'target="_self">'
            f"{escape(category)}</a>"
        )

    technique_links = []
    for technique in selected_category_techniques:
        name = technique["name"]
        active_class = " is-active" if name == selected_name else ""
        technique_links.append(
            f'<a class="landscape-nav-technique{active_class}" '
            f'href="{escape(get_selection_url(selected_category, name))}" '
            'target="_self">'
            f"{escape(format_technique_name(name))}</a>"
        )

    st.markdown(
        '<div class="landscape-nav" id="landscape-nav">'
        '<input class="landscape-nav-state" id="landscape-nav-state" '
        'type="checkbox" aria-hidden="true" />'
        '<label class="landscape-nav-toggle" for="landscape-nav-state" '
        'aria-label="Ouvrir la navigation">☰</label>'
        '<div class="landscape-nav-panel" aria-label="Navigation paysage">'
        '<label class="landscape-nav-close" for="landscape-nav-state" '
        'aria-label="Fermer la navigation">×</label>'
        '<nav class="landscape-nav-categories" aria-label="Catégories">'
        f"{''.join(category_links)}"
        "</nav>"
        '<nav class="landscape-nav-techniques" aria-label="Techniques">'
        f"{''.join(technique_links)}"
        "</nav>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def apply_query_param_selection() -> None:
    requested_category = st.query_params.get("category")
    requested_name = st.query_params.get("technique")

    if requested_category not in categories:
        return

    requested_techniques = get_category_techniques(requested_category)
    requested_names = [technique["name"] for technique in requested_techniques]

    st.session_state.selected_category = requested_category
    if requested_name in requested_names:
        st.session_state.selected_name = requested_name
    else:
        st.session_state.selected_name = requested_names[0]


def prevent_mobile_keyboard_on_selectboxes() -> None:
    st.html(
        """
        <script>
            function lockSelectInputs() {
                if (!window.parent.matchMedia('(pointer: coarse)').matches) {
                    return;
                }

                const doc = window.parent.document;
                const inputs = doc.querySelectorAll(
                    '[data-baseweb="select"] input'
                );

                inputs.forEach((input) => {
                    input.setAttribute('readonly', 'readonly');
                    input.setAttribute('inputmode', 'none');
                    input.setAttribute('autocomplete', 'off');
                });
            }

            lockSelectInputs();

            if (!window.parent.document._judoSelectInputLockBound) {
                window.parent.document._judoSelectInputLockBound = true;
                window.parent.setTimeout(lockSelectInputs, 250);
                window.parent.setTimeout(lockSelectInputs, 750);

                const observer = new MutationObserver(lockSelectInputs);
                observer.observe(window.parent.document.body, {
                    childList: true,
                    subtree: true
                });
            }
        </script>
        """,
        unsafe_allow_javascript=True,
    )


apply_query_param_selection()

if "selected_category" not in st.session_state:
    st.session_state.selected_category = categories[0]

category_techniques = get_category_techniques(st.session_state.selected_category)
technique_names = [technique["name"] for technique in category_techniques]

if (
    "selected_name" not in st.session_state
    or st.session_state.selected_name not in technique_names
):
    st.session_state.selected_name = technique_names[0]

current_index = technique_names.index(st.session_state.selected_name)
previous_index = (current_index - 1) % len(technique_names)
next_index = (current_index + 1) % len(technique_names)

prevent_mobile_keyboard_on_selectboxes()

def get_theme_url(target: str) -> str:
    query = (
        f"category={quote(st.session_state.selected_category)}"
        f"&technique={quote(st.session_state.selected_name)}"
        f"&theme={target}"
    )
    return f"/?{query}"


if theme_mode == "dark":
    theme_toggle_links = (
        f'<a class="app-theme-link" href="{get_theme_url("light")}" '
        'aria-label="Activer le thème clair"><span aria-hidden="true">☀</span>'
        '<span class="theme-label"> Clair</span></a>'
    )
    theme_toggle_class = ""
elif theme_mode == "light":
    theme_toggle_links = (
        f'<a class="app-theme-link" href="{get_theme_url("dark")}" '
        'aria-label="Activer le thème sombre"><span aria-hidden="true">☾</span>'
        '<span class="theme-label"> Sombre</span></a>'
    )
    theme_toggle_class = ""
else:
    theme_toggle_links = (
        f'<a class="app-theme-link app-theme-light" href="{get_theme_url("light")}" '
        'aria-label="Activer le thème clair"><span aria-hidden="true">☀</span>'
        '<span class="theme-label"> Clair</span></a>'
        f'<a class="app-theme-link app-theme-dark" href="{get_theme_url("dark")}" '
        'aria-label="Activer le thème sombre"><span aria-hidden="true">☾</span>'
        '<span class="theme-label"> Sombre</span></a>'
    )
    theme_toggle_class = " is-system"

st.markdown(
    f"""
    <header class="app-header">
        <h1 class="app-title">
            <span class="app-title-mark" aria-hidden="true">
                {JUDO_MARK_SVG}
            </span>
            <span class="app-title-text">Gokyo - Judo</span>
        </h1>
        <div class="app-header-actions">
            <nav class="app-theme-toggle{theme_toggle_class}" aria-label="Thème">{theme_toggle_links}</nav>
            {nav_links_html("home", theme_mode)}
        </div>
    </header>
    """,
    unsafe_allow_html=True,
)

selected_category = st.selectbox(
    "Catégorie",
    categories,
    key="selected_category",
    on_change=reset_selected_name,
)

category_techniques = get_category_techniques(selected_category)
technique_names = [technique["name"] for technique in category_techniques]

selected_name = st.selectbox(
    "Technique",
    technique_names,
    format_func=format_technique_name,
    key="selected_name",
    on_change=sync_selected_name,
)

selected_technique = category_techniques[technique_names.index(selected_name)]

video_id = extract_youtube_id(selected_technique["youtube"])
embed_url = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"
escaped_video_id = escape(video_id)

st.markdown(
    f"""
    <div class="tech-panel">
        <h2 class="technique-name" aria-label="{escape(format_technique_name(selected_technique["name"]))}, technique {current_index + 1} sur {len(technique_names)} dans {escape(selected_category)}">
            {escape(format_technique_name(selected_technique["name"]))}
            <span class="technique-position" aria-hidden="true">· {current_index + 1}/{len(technique_names)}</span>
        </h2>
        <p class="tech-description">{escape(selected_technique["description"])}</p>
        <div class="video-wrapper">
            <iframe id="video-{escaped_video_id}" key="{escaped_video_id}" class="video-frame" src="{escape(embed_url)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <nav class="standard-navigation" aria-label="Navigation entre les techniques">
            <a
                class="standard-nav-button standard-nav-previous"
                href="{escape(get_selection_url(selected_category, technique_names[previous_index]))}"
                target="_self"
                aria-label="Technique précédente"
            >←</a>
            <a
                class="standard-nav-button standard-nav-next"
                href="{escape(get_selection_url(selected_category, technique_names[next_index]))}"
                target="_self"
                aria-label="Technique suivante"
            >→</a>
        </nav>
    </div>
    """,
    unsafe_allow_html=True,
)

render_landscape_navigation_overlay(
    selected_category,
    selected_name,
    category_techniques,
)

st.button(
    "←",
    on_click=select_technique,
    args=(technique_names[previous_index],),
    key="landscape_previous_button",
)
st.button(
    "→",
    on_click=select_technique,
    args=(technique_names[next_index],),
    key="landscape_next_button",
)
