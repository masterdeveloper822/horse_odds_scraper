import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from scraper.utils import convert_to_decimal
from config import LADBROKES_URL, HEADERS


async def scrape_ladbrokes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(extra_http_headers=HEADERS)

        # Navigate and wait for race cards to appear
        await page.goto(LADBROKES_URL, timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_selector("race-card-home", timeout=30000)

        html = await page.content()

        await browser.close()

    # Parse HTML
    soup = BeautifulSoup(html, "lxml")
    races = []

    for race_card in soup.select("race-card-home"):
        # Try different selectors for race name
        race_name_tag = race_card.select_one(
            '[data-crlat="raceCard.eventName"], .race-title'
        )
        race_name = race_name_tag.get_text(strip=True) if race_name_tag else "Unknown Race"

        runners = []
        for odd in race_card.select('[data-crlat="raceCard.odds"]'):
            name_tag = odd.select_one('[data-crlat="raceCard.runnerName"]')
            name = name_tag.get_text(strip=True) if name_tag else None

            # Odds are inside the bet button > oddsPrice span
            odds_tag = odd.select_one('button[data-crlat="betButton"] span[data-crlat="oddsPrice"]')
            odds_raw = odds_tag.get_text(strip=True) if odds_tag else None

            # Only accept fractional odds (ignore "SP" or text like jockey names)
            if odds_raw and "/" not in odds_raw:
                odds_raw = None

            odds_decimal = convert_to_decimal(odds_raw) if odds_raw else None

            if name:
                runners.append({
                    "horse_name": name,
                    "odds_raw": odds_raw,
                    "odds_decimal": odds_decimal
                })

        if runners:
            races.append({"race_name": race_name, "runners": runners})

    return races


if __name__ == "__main__":
    results = asyncio.run(scrape_ladbrokes())
    for race in results[:2]:  # print first 2 races for testing
        print("Race:", race["race_name"])
        for runner in race["runners"][:5]:  # print first 5 runners
            print("  Horse:", runner["horse_name"], "| Odds:", runner["odds_raw"], "(", runner["odds_decimal"], ")")
