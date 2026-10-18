from unittest import TestCase, main

from random import Random

from judo_utils import draw_techniques_by_category, extract_youtube_id, filter_techniques


class ExtractYoutubeIdTest(TestCase):
    def test_extracts_watch_id_when_v_is_not_first_query_parameter(self) -> None:
        self.assertEqual(
            extract_youtube_id("https://www.youtube.com/watch?feature=shared&v=abc123"),
            "abc123",
        )

    def test_extracts_supported_youtube_url_forms(self) -> None:
        cases = {
            "https://www.youtube.com/watch?v=watch123&list=playlist": "watch123",
            "https://youtu.be/short123?si=share": "short123",
            "https://www.youtube.com/shorts/shorts123?feature=share": "shorts123",
        }

        for url, expected_id in cases.items():
            with self.subTest(url=url):
                self.assertEqual(extract_youtube_id(url), expected_id)


class FilterTechniquesTest(TestCase):
    techniques = [
        {"name": "O-soto-gari", "category": "Ashi waza"},
        {"name": "Seoi-nage", "category": "Te waza"},
        {"name": "Juji-gatame", "category": "Kansetsu waza"},
    ]

    def test_filters_by_name_ignoring_case_and_hyphens(self) -> None:
        self.assertEqual(
            filter_techniques(self.techniques, "o soto"),
            [self.techniques[0]],
        )

    def test_filters_by_category_ignoring_accents(self) -> None:
        self.assertEqual(
            filter_techniques(self.techniques, "Kansét"),
            [self.techniques[2]],
        )

    def test_empty_query_returns_all_techniques(self) -> None:
        self.assertEqual(filter_techniques(self.techniques, "  "), self.techniques)


class DrawTechniquesByCategoryTest(TestCase):
    techniques = [
        {"name": "Technique A1", "category": "A"},
        {"name": "Technique A2", "category": "A"},
        {"name": "Technique A3", "category": "A"},
        {"name": "Technique B1", "category": "B"},
        {"name": "Technique B2", "category": "B"},
        {"name": "Technique C1", "category": "C"},
        {"name": "Technique C2", "category": "C"},
    ]

    def test_draw_covers_every_category_without_repeats(self) -> None:
        draw = draw_techniques_by_category(
            self.techniques,
            ["A", "B", "C"],
            5,
            rng=Random(12),
        )

        self.assertEqual(len(draw), 5)
        self.assertEqual(len({item["name"] for item in draw}), 5)
        self.assertEqual(
            {item["category"] for item in draw},
            {"A", "B", "C"},
        )

    def test_draw_rejects_count_that_cannot_cover_every_category(self) -> None:
        with self.assertRaises(ValueError):
            draw_techniques_by_category(
                self.techniques,
                ["A", "B", "C"],
                2,
                rng=Random(12),
            )


if __name__ == "__main__":
    main()
