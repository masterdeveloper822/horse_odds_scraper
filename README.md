# Horse Odds Scraper

A Python application that scrapes horse racing odds from multiple UK betting sites and identifies value betting opportunities by comparing odds across different bookmakers.

## Overview

This project continuously monitors horse racing odds from five major UK bookmakers (Coral, Ladbrokes, Skybet, Paddypower, and Betfair) and alerts users when significant price differences are detected between bookmakers. The application uses web scraping with Playwright to extract real-time odds data and stores it in a PostgreSQL database for analysis.

## Features

- **Multi-Bookmaker Scraping**: Collects odds from 5 different betting sites simultaneously
- **Value Opportunity Detection**: Identifies horses with significant odds differences across bookmakers
- **Fuzzy Horse Matching**: Uses fuzzy string matching to match horses across different bookmakers even when names vary slightly
- **Database Storage**: Stores all scraped data in PostgreSQL for historical analysis
- **Continuous Monitoring**: Runs continuously, checking for new opportunities every 60 seconds
- **Odds Conversion**: Supports fractional, decimal, and American odds formats

## Technology Stack

- **Python 3.x**
- **Playwright**: Browser automation for web scraping
- **BeautifulSoup**: HTML parsing
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Relational database
- **rapidfuzz**: Fuzzy string matching for horse name matching

## Project Structure

```
horse_odds_scraper/
├── main.py                          # Main entry point - runs continuous scraping loop
├── config.py                        # Configuration (database URL, bookmaker URLs, headers)
├── requirements.txt                 # Python dependencies
├── check_data.py                    # Utility script to view scraped data
├── demo_scraper.py                  # Demo scraper with mock data for testing
├── db/
│   ├── db.py                        # Database connection and session setup
│   └── models.py                    # SQLAlchemy models (Race, Horse, Runner, Odds)
└── scraper/
    ├── coral_scraper_playwright.py  # Coral bookmaker scraper
    ├── ladbrokes_scraper_playwright.py
    ├── skybet_scraper_playwright.py
    ├── paddypower_scraper_playwright.py
    ├── betfair_scraper_playwright.py
    ├── comparison.py                # Value opportunity detection logic
    └── utils.py                     # Utility functions (odds conversion)
```

## Installation

### Prerequisites

- Python 3.7 or higher
- PostgreSQL database
- Playwright browsers (installed automatically with dependencies)

### Setup Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd horse_odds_scraper
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

4. Configure the database connection in `config.py`:
```python
DB_URL = "postgresql://username:password@localhost:5432/horse_odds"
```

5. Create the PostgreSQL database:
```bash
createdb horse_odds
```

6. The database tables will be created automatically on first run.

## Usage

### Running the Main Scraper

Start the continuous scraping and monitoring process:

```bash
python main.py
```

The application will:
- Scrape odds from all 5 bookmakers
- Compare odds across bookmakers
- Display value opportunities (odds differences >= 1%)
- Wait 60 seconds before the next iteration

### Testing Individual Scrapers

You can test individual scrapers directly:

```bash
python scraper/coral_scraper_playwright.py
python scraper/betfair_scraper_playwright.py
```

### Checking Stored Data

View all scraped data in the database:

```bash
python check_data.py
```

### Demo Mode

Test the system with mock data:

```bash
python demo_scraper.py
```

## Database Schema

The application uses four main tables:

- **races**: Stores race information (bookmaker, race name, start time)
- **horses**: Stores unique horse names
- **runners**: Links horses to races
- **odds**: Stores odds data (decimal and raw format) with timestamps

## Value Opportunity Detection

The system identifies value opportunities by:

1. Grouping races by race name
2. Matching horses across bookmakers using fuzzy string matching (85% similarity threshold)
3. Calculating the percentage difference between best and worst odds
4. Alerting when the difference exceeds the threshold (default: 1% in main.py, 20% in comparison.py)

Example alert output:
```
Value Alert!
Race: 3:30 Newmarket - Handicap Stakes | Horse: Thunder Strike
Best: 5/1 (Coral)
Worst: 3/1 (Ladbrokes)
Diff: 66.7%
```

## Configuration

Edit `config.py` to customize:

- Database connection string
- Bookmaker URLs
- HTTP headers
- Scraping intervals (in `main.py`)

## Notes

- The scrapers use Playwright with headless browsers to handle JavaScript-rendered content
- Horse name matching uses fuzzy string matching to handle variations in naming across bookmakers
- The system requires at least 2 bookmakers to have data for a race to detect opportunities
- Odds are stored in both raw format (as displayed) and decimal format (for calculations)

## Dependencies

See `requirements.txt` for the complete list. Key dependencies include:

- `playwright`: Browser automation
- `beautifulsoup4`: HTML parsing
- `sqlalchemy`: Database ORM
- `psycopg2-binary`: PostgreSQL adapter
- `rapidfuzz`: Fuzzy string matching

## Disclaimer

This tool is for educational and research purposes only. Always ensure compliance with the terms of service of the websites being scraped. Be respectful of server resources and implement appropriate rate limiting.

