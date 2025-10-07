import asyncio
from scraper.coral_scraper_playwright import scrape_coral
from scraper.ladbrokes_scraper_playwright import scrape_ladbrokes
from scraper.skybet_scraper_playwright import scrape_skybet
from scraper.paddypower_scraper_playwright import scrape_paddypower
from scraper.betfair_scraper_playwright import scrape_betfair
from scraper.comparison import find_value_opportunities

async def main():
    while True:
        coral_data = await scrape_coral()
        ladbrokes_data = await scrape_ladbrokes()
        skybet_data = await scrape_skybet()
        paddypower_data = await scrape_paddypower()
        betfair_data = await scrape_betfair()

        races_by_bookmaker = {"Coral": coral_data, "Ladbrokes": ladbrokes_data, "Skybet": skybet_data, "Paddypower": paddypower_data, "Betfair": betfair_data}
        alerts = find_value_opportunities(races_by_bookmaker, threshold=0.01)

        if alerts:
            for alert in alerts:
                print(
                    f"📢 Value Alert!\n"
                    f"🏇 {alert['race']} | 🐎 {alert['horse']}\n"
                    f"💰 Best: {alert['best']['odds_raw']} ({alert['best']['bookmaker']})\n"
                    f"❌ Worst: {alert['worst']['odds_raw']} ({alert['worst']['bookmaker']})\n"
                    f"📈 Diff: {alert['diff_pct']}%\n"
                )
        else:
            print("No opportunities this round.")

        # Wait 60 seconds before scraping again
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
