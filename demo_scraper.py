"""
Demo scraper with mock data to show how the project works
"""
import random
from datetime import datetime
from db.db import session
from db.models import Race, Horse, Runner, Odds

def generate_mock_race_data():
    """Generate mock horse racing data for demonstration"""
    race_names = [
        "3:30 Newmarket - Handicap Stakes",
        "4:15 Cheltenham - Chase",
        "5:00 Aintree - Hurdle",
        "2:45 Kempton - Maiden Stakes",
        "6:30 Lingfield - All Weather"
    ]
    
    horse_names = [
        "Thunder Strike", "Lightning Bolt", "Storm Chaser", "Wind Runner",
        "Fire Storm", "Ice Queen", "Golden Arrow", "Silver Bullet",
        "Midnight Express", "Dawn Patrol", "Sunset Rider", "Moon Walker"
    ]
    
    races = []
    for race_name in race_names:
        runners = []
        num_runners = random.randint(6, 12)
        selected_horses = random.sample(horse_names, num_runners)
        
        for horse_name in selected_horses:
            # Generate realistic odds (fractional format)
            odds_fractions = ["2/1", "3/1", "4/1", "5/1", "6/1", "7/1", "8/1", "10/1", "12/1", "16/1", "20/1", "25/1", "33/1"]
            odds_raw = random.choice(odds_fractions)
            
            # Convert to decimal
            if "/" in odds_raw:
                num, denom = odds_raw.split("/")
                odds_decimal = 1 + float(num)/float(denom)
            else:
                odds_decimal = float(odds_raw)
            
            runners.append({
                "horse_name": horse_name,
                "odds_raw": odds_raw,
                "odds_decimal": odds_decimal
            })
        
        races.append({
            "race_name": race_name,
            "runners": runners
        })
    
    return races

def scrape_demo():
    """Demo scraper that generates mock data"""
    print("Generating mock horse racing data...")
    races_data = generate_mock_race_data()
    
    for race in races_data:
        print(f"Processing race: {race['race_name']}")
        race_obj = Race(bookmaker="Demo", race_name=race["race_name"])
        session.add(race_obj)
        session.commit()  # to get race_obj.id

        for r in race["runners"]:
            horse_obj = session.query(Horse).filter_by(name=r["horse_name"]).first()
            if not horse_obj:
                horse_obj = Horse(name=r["horse_name"])
                session.add(horse_obj)
                session.commit()
            
            runner_obj = Runner(race_id=race_obj.id, horse_id=horse_obj.id, horse_name=r["horse_name"])
            session.add(runner_obj)
            session.commit()
            
            odds_obj = Odds(runner_id=runner_obj.id, bookmaker="Demo", odds_decimal=r["odds_decimal"], odds_raw=r["odds_raw"])
            session.add(odds_obj)
            session.commit()

    print("Demo scraping complete!")

if __name__ == "__main__":
    scrape_demo()
