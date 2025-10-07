from rapidfuzz import fuzz, process

def normalize_horse_name(name: str) -> str:
    """Basic cleanup for horse names."""
    return name.strip().lower().replace("'", "").replace("-", "").replace(" ", "")


def match_horses(runners_by_bookmaker):
    # Get unique horse names from all bookmakers
    all_names = []
    for bookmaker, runners in runners_by_bookmaker.items():
        for r in runners:
            if r["horse_name"]:
                all_names.append(r["horse_name"])
    unique_names = list(set(all_names))

    matches = {}
    for bookmaker, runners in runners_by_bookmaker.items():
        for r in runners:
            if not r["horse_name"]:
                continue
            # Try to match each name to master list
            match, score, _ = process.extractOne(
                r["horse_name"], unique_names, scorer=fuzz.token_sort_ratio
            )
            if score > 85:  # threshold
                matches.setdefault(match, []).append({
                    "bookmaker": bookmaker,
                    "horse_name": r["horse_name"],
                    "odds_decimal": r["odds_decimal"],
                    "odds_raw": r["odds_raw"]
                })
    return matches


def find_value_opportunities(races_by_bookmaker, threshold=0.20):
    alerts = []

    # Group by race name for now (can be improved with fuzzy race matching)
    race_names = set()
    for bookmaker, races in races_by_bookmaker.items():
        for r in races:
            race_names.add(r["race_name"])

    for race_name in race_names:
        runners_by_bookmaker = {}
        for bookmaker, races in races_by_bookmaker.items():
            for r in races:
                if r["race_name"] == race_name:
                    runners_by_bookmaker[bookmaker] = r["runners"]

        if len(runners_by_bookmaker) < 2:
            continue  # need at least 2 bookmakers

        horse_matches = match_horses(runners_by_bookmaker)

        for canonical_name, offers in horse_matches.items():
            odds = [o["odds_decimal"] for o in offers if o["odds_decimal"]]
            if len(odds) < 2:
                continue

            best_offer = max(offers, key=lambda x: x["odds_decimal"])
            worst_offer = min(offers, key=lambda x: x["odds_decimal"])

            diff = (best_offer["odds_decimal"] - worst_offer["odds_decimal"]) / worst_offer["odds_decimal"]

            if diff >= threshold:
                alerts.append({
                    "race": race_name,
                    "horse": canonical_name,
                    "best": best_offer,
                    "worst": worst_offer,
                    "diff_pct": round(diff * 100, 1)
                })

    return alerts
