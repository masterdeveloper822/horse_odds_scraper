import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from scraper.utils import convert_to_decimal
from config import PADDYPOWER_URL, HEADERS

async def scrape_paddypower():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(extra_http_headers=HEADERS)
        await page.goto(PADDYPOWER_URL, timeout=60000)
        # Wait until at least one race card loads
        await page.wait_for_selector(".abc-card", timeout=20000)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "lxml")
    races = []

    for race_card in soup.select(".abc-card"):
        race_name_tag = race_card.select_one(".abc-race-header__title")
        if not race_name_tag:
            continue
        race_name = race_name_tag.get_text(strip=True)

        runners = []
        for runner_tag in race_card.select(".racing-runner"):
            horse_name_tag = runner_tag.select_one(".racing-runner__selection-name")
            odds_tag = runner_tag.select_one(".btn-odds__label")

            if horse_name_tag and odds_tag:
                horse_name = horse_name_tag.get_text(strip=True)
                odds_raw = odds_tag.get_text(strip=True)
                odds_decimal = convert_to_decimal(odds_raw)

                runners.append({
                    "horse_name": horse_name,
                    "odds_raw": odds_raw,
                    "odds_decimal": odds_decimal
                })

        races.append({"race_name": race_name, "runners": runners})

    return races

# For testing directly
if __name__ == "__main__":
    results = asyncio.run(scrape_paddypower())
    for race in results:
        print("Race:", race["race_name"])
        for runner in race["runners"]:
            print("  Horse:", runner["horse_name"], "| Odds:", runner["odds_raw"], "(", runner["odds_decimal"], ")")
