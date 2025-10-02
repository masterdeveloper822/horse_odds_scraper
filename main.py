import asyncio
from db.db import session
from db.models import Race, Horse, Runner, Odds
from scraper.coral_scraper_playwright import scrape_coral
from scraper.ladbrokes_scraper_playwright import scrape_ladbrokes

async def save_to_db(scraper_func, bookmaker_name):
    races_data = await scraper_func()

    for race in races_data:
        # Create Race record
        race_obj = Race(bookmaker=bookmaker_name, race_name=race["race_name"])
        session.add(race_obj)
        session.commit()  # commit to get race_obj.id

        for r in race["runners"]:
            # Check if horse already exists
            horse_obj = session.query(Horse).filter_by(name=r["horse_name"]).first()
            if not horse_obj:
                horse_obj = Horse(name=r["horse_name"])
                session.add(horse_obj)
                session.commit()

            # Link runner to race
            runner_obj = Runner(race_id=race_obj.id, horse_id=horse_obj.id, horse_name=r["horse_name"])
            session.add(runner_obj)
            session.commit()

            # Store odds
            odds_obj = Odds(
                runner_id=runner_obj.id,
                bookmaker=bookmaker_name,
                odds_decimal=r["odds_decimal"],
                odds_raw=r["odds_raw"]
            )
            session.add(odds_obj)
            session.commit()

    print(f"✅ Saved {len(races_data)} {bookmaker_name} races into DB.")

async def main():
    await save_to_db(scrape_coral, "Coral")
    await save_to_db(scrape_ladbrokes, "Ladbrokes")

if __name__ == "__main__":
    asyncio.run(main())
