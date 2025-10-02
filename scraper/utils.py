def convert_to_decimal(odds_raw):
    odds_raw = odds_raw.strip()
    # Fractional e.g. "5/2"
    if "/" in odds_raw:
        num, denom = odds_raw.split("/")
        return 1 + float(num)/float(denom)
    # American e.g. "+250" or "-150"
    if odds_raw.startswith("+"):
        return 1 + int(odds_raw[1:])/100
    if odds_raw.startswith("-"):
        return 1 + 100/abs(int(odds_raw))
    # Decimal
    try:
        return float(odds_raw)
    except:
        return None
