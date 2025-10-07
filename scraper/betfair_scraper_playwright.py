import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from scraper.utils import convert_to_decimal
from config import BETFAIR_URL, HEADERS

async def scrape_betfair():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(extra_http_headers=HEADERS)
        await page.goto(BETFAIR_URL, timeout=60000)
        # Wait until at least one race card loads
        await page.wait_for_selector(".f425ac14765f5c6e-swimlaneItemContainer", timeout=20000)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "lxml")
    races = []

    for race_card in soup.select(".f425ac14765f5c6e-swimlaneItemContainer"):
        race_name_tag = race_card.select_one("._5603ba10916efca5-topSectionLeft")
        if not race_name_tag:
            continue
        race_name = race_name_tag.get_text(strip=True)

        runners = []
        for runner_tag in race_card.select("._96a500251e65e85a-runner"):
            horse_name_tag = runner_tag.select_one("._96a500251e65e85a-horseName")
            odds_tag = runner_tag.select_one(".c84e4011151df22b-labelTwoLines")

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
    results = asyncio.run(scrape_betfair())
    for race in results:
        print("Race:", race["race_name"])
        for runner in race["runners"]:
            print("  Horse:", runner["horse_name"], "| Odds:", runner["odds_raw"], "(", runner["odds_decimal"], ")")
