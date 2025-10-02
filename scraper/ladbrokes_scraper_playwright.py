import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from scraper.utils import convert_to_decimal
from config import LADBROKES_URL, HEADERS

async def scrape_ladbrokes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(extra_http_headers=HEADERS)
        await page.goto(LADBROKES_URL, timeout=60000)
        await page.wait_for_selector("slide[data-crlat='raceCard.event']", timeout=20000)
        html = await page.content()
        await browser.close()

    await page.screenshot(path="ladbrokes_debug.png", full_page=True)
    html = await page.content()
    with open("ladbrokes_debug.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    
    soup = BeautifulSoup(html, "lxml")
    races = []

    for race_card in soup.select("slide[data-crlat='raceCard.event']"):
        race_name_tag = race_card.select_one("[data-crlat='raceCard.eventName']")
        if not race_name_tag:
            continue
        race_name = race_name_tag.get_text(strip=True)

        runners = []
        for runner in race_card.select("[data-crlat='raceCard.runnerName']"):
            name = runner.get_text(strip=True)
            odds_tag = runner.find_parent("div", class_="odds-names").find_next("span", {"data-crlat": "oddsPrice"})
            odds_raw = odds_tag.get_text(strip=True) if odds_tag else None
            odds_decimal = convert_to_decimal(odds_raw) if odds_raw else None
            runners.append({"horse_name": name, "odds_raw": odds_raw, "odds_decimal": odds_decimal})

        races.append({"race_name": race_name, "runners": runners})

    return races

if __name__ == "__main__":
    results = asyncio.run(scrape_ladbrokes())
    for race in results[:1]:
        print("Race:", race["race_name"])
        for runner in race["runners"]:
            print("  Horse:", runner["horse_name"], "| Odds:", runner["odds_raw"], "(", runner["odds_decimal"], ")")
