from __future__ import annotations

from random import Random
import unicodedata
from urllib.parse import parse_qs, urlparse


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
