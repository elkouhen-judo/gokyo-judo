from __future__ import annotations

from random import Random
import unicodedata
from urllib.parse import parse_qs, urlparse


LIGHT_THEME = (
    "--ink:#172033;--muted:#5f6b7d;--line:rgba(31,52,83,.14);"
    "--panel:rgba(255,255,255,.97);--surface:#f3f6fa;--page-top:#fbfcfe;"
    "--accent:#2864dc;--accent-soft:rgba(40,100,220,.08);"
    "--shadow-soft:0 12px 30px rgba(31,52,83,.09);"
    "--field-bg:#fff;--field-bg-end:#f9fbff;--menu-bg:#fff;"
    "--navigation-bg:rgba(255,255,251,.82);"
    "--navigation-button-bg:rgba(255,255,251,.98);--icon-bg:#e8efff;"
    "--icon-outline:#172033;--landscape-nav-bg:rgba(255,255,251,.94);"
    "--divider:#edf0f5;--exam-bg:rgba(255,255,255,.97);"
    "--quote-bg:rgba(255,255,255,.75);"
)
DARK_THEME = (
    "--ink:#e6edf8;--muted:#a7b3c6;--line:rgba(190,208,235,.18);"
    "--panel:rgba(23,31,45,.97);--surface:#0d1421;--page-top:#111a28;"
    "--accent:#82aaff;--accent-soft:rgba(104,153,255,.17);"
    "--shadow-soft:0 12px 30px rgba(0,0,0,.28);"
    "--field-bg:#1a2433;--field-bg-end:#151e2c;--menu-bg:#172130;"
    "--navigation-bg:rgba(23,31,45,.9);"
    "--navigation-button-bg:rgba(31,42,58,.98);--icon-bg:#1a2b49;"
    "--icon-outline:#e6edf8;--landscape-nav-bg:rgba(23,31,45,.96);"
    "--divider:rgba(190,208,235,.14);--exam-bg:rgba(23,31,45,.97);"
    "--quote-bg:rgba(31,42,58,.82);"
)


def get_theme_styles(theme_mode: str) -> str:
    forced_theme = ""
    if theme_mode == "light":
        forced_theme = f".stApp {{{LIGHT_THEME}color-scheme:light;}}"
    elif theme_mode == "dark":
        forced_theme = f".stApp {{{DARK_THEME}color-scheme:dark;}}"

    return f"""
        <style>
            :root {{{LIGHT_THEME}color-scheme:light;}}
            [data-theme="dark"] {{{DARK_THEME}color-scheme:dark;}}
            @media (prefers-color-scheme:dark) {{
                :root:not([data-theme="light"]) {{{DARK_THEME}color-scheme:dark;}}
            }}
            .stApp {{
                color:var(--ink);
                background:
                    radial-gradient(ellipse at 90% 0%,rgba(40,100,220,.07),transparent 42%),
                    linear-gradient(180deg,var(--page-top) 0%,var(--surface) 100%);
            }}
            {forced_theme}
        </style>
    """


def normalize_search_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character)
    ).replace("-", " ")


def filter_techniques(
    techniques: list[dict[str, str]],
    query: str,
) -> list[dict[str, str]]:
    normalized_query = normalize_search_text(query.strip())
    if not normalized_query:
        return techniques

    return [
        technique
        for technique in techniques
        if normalized_query
        in normalize_search_text(
            f"{technique['name']} {technique['category']}"
        )
    ]


def draw_techniques_by_category(
    techniques: list[dict[str, str]],
    categories: list[str],
    count: int,
    rng: Random | None = None,
) -> list[dict[str, str]]:
    if count < len(categories):
        raise ValueError("The draw count must cover every requested category.")

    techniques_by_category = {
        category: [
            technique
            for technique in techniques
            if technique["category"] == category
        ]
        for category in categories
    }
    if any(not items for items in techniques_by_category.values()):
        raise ValueError("Every requested category must contain techniques.")

    if count > sum(len(items) for items in techniques_by_category.values()):
        raise ValueError("The draw count cannot exceed the available techniques.")

    chooser = rng or Random()
    draw = [chooser.choice(items) for items in techniques_by_category.values()]
    draw_ids = {id(technique) for technique in draw}
    remaining = [
        technique
        for category_items in techniques_by_category.values()
        for technique in category_items
        if id(technique) not in draw_ids
    ]
    draw.extend(chooser.sample(remaining, count - len(draw)))
    return draw


def extract_youtube_id(url: str) -> str:
    parsed_url = urlparse(url)

    if parsed_url.netloc.endswith("youtu.be"):
        return parsed_url.path.lstrip("/").split("/")[0]

    if "/shorts/" in parsed_url.path:
        return parsed_url.path.split("/shorts/", 1)[1].split("/", 1)[0]

    video_ids = parse_qs(parsed_url.query).get("v")
    if video_ids:
        return video_ids[0]

    return url
