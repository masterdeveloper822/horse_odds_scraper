from db.db import session
from db.models import Race, Horse, Runner, Odds

def check_scraped_data():
    print("=== RACES ===")
    races = session.query(Race).all()
    for race in races:
        print(f"ID: {race.id}, Bookmaker: {race.bookmaker}, Race: {race.race_name}")
    
    print("\n=== HORSES ===")
    horses = session.query(Horse).all()
    for horse in horses:
        print(f"ID: {horse.id}, Name: {horse.name}")
    
    print("\n=== RUNNERS ===")
    runners = session.query(Runner).all()
    for runner in runners:
        print(f"ID: {runner.id}, Race ID: {runner.race_id}, Horse: {runner.horse_name}")
    
    print("\n=== ODDS ===")
    odds = session.query(Odds).all()
    for odd in odds:
        print(f"ID: {odd.id}, Runner ID: {odd.runner_id}, Bookmaker: {odd.bookmaker}, Odds: {odd.odds_raw} -> {odd.odds_decimal}")

if __name__ == "__main__":
    check_scraped_data()
