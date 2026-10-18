from __future__ import annotations

import os

from playwright.sync_api import expect, sync_playwright


APP_URL = os.environ.get("APP_URL", "http://localhost:8501")
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def assert_card_corner_navigation(page) -> None:
    panel_box = page.locator(".tech-panel").evaluate(
        "element => element.getBoundingClientRect()"
    )
    nav_box = page.locator(".standard-navigation").first.evaluate(
        "element => element.getBoundingClientRect()"
    )
    nav_style = page.locator(".standard-navigation").first.evaluate(
        """element => ({
            background: getComputedStyle(element).backgroundColor,
            borderTopWidth: getComputedStyle(element).borderTopWidth,
            boxShadow: getComputedStyle(element).boxShadow,
        })"""
    )
    button_style = page.locator(".standard-nav-next").first.evaluate(
        """element => ({
            background: getComputedStyle(element).backgroundColor,
            borderTopWidth: getComputedStyle(element).borderTopWidth,
            boxShadow: getComputedStyle(element).boxShadow,
        })"""
    )

    assert nav_box["left"] >= panel_box["left"], (panel_box, nav_box)
    assert nav_box["right"] <= panel_box["right"], (panel_box, nav_box)
    assert nav_box["top"] >= panel_box["top"], (panel_box, nav_box)
    assert nav_box["top"] <= panel_box["top"] + 20, (panel_box, nav_box)
    assert panel_box["right"] - nav_box["right"] <= 20, (
        panel_box,
        nav_box,
    )
    assert nav_style["background"] == "rgba(0, 0, 0, 0)"
    assert nav_style["borderTopWidth"] == "0px"
    assert nav_style["boxShadow"] == "none"
    assert button_style["background"] == "rgba(0, 0, 0, 0)"
    assert button_style["borderTopWidth"] == "0px"
    assert button_style["boxShadow"] == "none"


def assert_mobile_layout() -> None:
    with sync_playwright() as playwright:
        launch_options = {"headless": True}
        if os.path.exists(CHROME_PATH):
            launch_options["executable_path"] = CHROME_PATH

        browser = playwright.chromium.launch(**launch_options)

        try:
            for width, height, is_landscape in (
                (390, 844, False),
                (844, 390, True),
                (667, 375, True),
            ):
                page = browser.new_page(
                    viewport={"width": width, "height": height},
                    is_mobile=True,
                    has_touch=True,
                )
                page.goto(APP_URL, wait_until="domcontentloaded", timeout=15_000)
                page.wait_for_timeout(1_000)

                video = page.locator(".video-wrapper")
                expect(video).to_be_visible()

                next_button = page.locator(
                    ".st-key-landscape_next_button button"
                ).first
                previous_button = page.locator(
                    ".st-key-landscape_previous_button button"
                ).first
                standard_next_button = page.locator(".standard-nav-next").first
                standard_previous_button = page.locator(".standard-nav-previous").first
                if is_landscape:
                    expect(next_button).to_be_visible()
                    expect(previous_button).to_be_visible()
                    expect(standard_next_button).to_be_hidden()
                    expect(standard_previous_button).to_be_hidden()
                    expect(page.locator(".landscape-nav-toggle")).to_be_visible()
                    expect(page.locator(".landscape-nav-panel")).to_be_hidden()

                    page.locator(".landscape-nav-toggle").click()
                    expect(page.locator(".landscape-nav-panel")).to_be_visible()
                    assert page.locator(".landscape-nav-category").count() >= 1
                    assert page.locator(".landscape-nav-technique").count() >= 2

                    style = next_button.evaluate(
                        """button => ({
                            opacity: getComputedStyle(button).opacity,
                            background: getComputedStyle(button).backgroundColor,
                        })"""
                    )
                    assert style["opacity"] == "1"
                    assert style["background"] != "rgba(0, 0, 0, 0)"

                    before_src = page.locator(".video-frame").get_attribute("src")
                    page.locator(".landscape-nav-technique:not(.is-active)").first.click()
                    page.wait_for_timeout(1_500)
                    after_src = page.locator(".video-frame").get_attribute("src")
                    assert before_src != after_src
                else:
                    expect(page.locator(".field-label", has_text="Catégorie")).to_have_count(0)
                    expect(page.locator(".field-label", has_text="Technique")).to_have_count(0)
                    expect(page.locator(".technique-name")).to_be_visible()
                    expect(standard_next_button).to_be_visible()
                    expect(standard_previous_button).to_be_visible()
                    next_width = standard_next_button.evaluate(
                        "element => element.getBoundingClientRect().width"
                    )
                    video_width = video.evaluate(
                        "element => element.getBoundingClientRect().width"
                    )
                    assert next_width < video_width * 0.3
                    select_input_state = page.locator(
                        '.stSelectbox [data-baseweb="select"] input'
                    ).first.evaluate(
                        """input => ({
                            inputMode: input.getAttribute('inputmode'),
                            pointerEvents: getComputedStyle(input).pointerEvents,
                            readOnly: input.readOnly,
                            tabIndex: input.tabIndex,
                        })"""
                    )
                    assert_card_corner_navigation(page)
                    assert select_input_state["inputMode"] == "none"
                    assert select_input_state["pointerEvents"] != "none"
                    assert select_input_state["readOnly"] is True
                    assert select_input_state["tabIndex"] >= 0
                    expect(next_button).to_be_hidden()
                    expect(previous_button).to_be_hidden()
                    expect(page.locator(".landscape-nav-toggle")).to_be_hidden()

                page.close()

            desktop_page = browser.new_page(
                viewport={"width": 1280, "height": 720},
                is_mobile=False,
                has_touch=False,
            )
            desktop_page.goto(APP_URL, wait_until="domcontentloaded", timeout=15_000)
            desktop_page.wait_for_timeout(1_000)

            expect(desktop_page.locator(".video-wrapper")).to_be_visible()
            expect(desktop_page.locator(".app-title")).to_be_visible()
            expect(desktop_page.locator(".field-label", has_text="Catégorie")).to_have_count(0)
            expect(desktop_page.locator(".field-label", has_text="Technique")).to_have_count(0)
            expect(desktop_page.locator(".technique-name")).to_be_visible()
            expect(desktop_page.locator(".standard-nav-next").first).to_be_visible()
            expect(desktop_page.locator(".standard-nav-previous").first).to_be_visible()
            expect(
                desktop_page.locator(".st-key-landscape_next_button button").first
            ).to_be_hidden()
            expect(
                desktop_page.locator(".st-key-landscape_previous_button button").first
            ).to_be_hidden()
            expect(desktop_page.locator(".landscape-nav-toggle")).to_be_hidden()

            desktop_video_style = desktop_page.locator(".video-wrapper").evaluate(
                "element => getComputedStyle(element).position"
            )
            assert desktop_video_style != "fixed"
            desktop_next_width = desktop_page.locator(
                ".standard-nav-next"
            ).first.evaluate("element => element.getBoundingClientRect().width")
            desktop_video_width = desktop_page.locator(".video-wrapper").evaluate(
                "element => element.getBoundingClientRect().width"
            )
            assert desktop_next_width < desktop_video_width * 0.3
            assert_card_corner_navigation(desktop_page)

            desktop_before_src = desktop_page.locator(
                ".video-frame"
            ).get_attribute("src")
            desktop_page.locator(".standard-nav-next").first.click()
            desktop_page.wait_for_timeout(1_500)
            desktop_after_src = desktop_page.locator(
                ".video-frame"
            ).get_attribute("src")
            assert desktop_before_src != desktop_after_src
            desktop_page.close()

            compact_page = browser.new_page(
                viewport={"width": 320, "height": 700},
                is_mobile=True,
                has_touch=True,
            )
            compact_page.goto(APP_URL, wait_until="domcontentloaded", timeout=15_000)
            compact_page.wait_for_timeout(1_000)
            expect(
                compact_page.get_by_role("link", name="Ouvrir le Référentiel")
            ).to_be_visible()
            assert compact_page.evaluate(
                "document.querySelector('.app-header-actions').getBoundingClientRect().right"
                " <= window.innerWidth"
            )

            compact_page.get_by_role("link", name="Ouvrir le Défi UV2").click()
            compact_page.wait_for_timeout(1_000)
            expect(
                compact_page.get_by_role("link", name="Retour à la révision")
            ).to_be_visible()
            expect(
                compact_page.get_by_role("link", name="Ouvrir le Référentiel")
            ).to_be_visible()
            compact_page.close()
        finally:
            browser.close()


if __name__ == "__main__":
    assert_mobile_layout()
