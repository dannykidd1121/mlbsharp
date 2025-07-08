import requests
import pandas as pd
from datetime import datetime

# Your Odds API key
API_KEY = '45d9c600747e23bf3799600342f8ce52'

# Build URL
url = (
    'https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/'
    f'?regions=us&markets=h2h,spreads,totals&apiKey={API_KEY}'
)

# Request odds data
response = requests.get(url)
if response.status_code != 200:
    print("❌ Error:", response.status_code, response.text)
    exit()

data = response.json()
rows = []

# Loop through games
for game in data:
    home = game['home_team']
    away = game['away_team']
    time = game['commence_time'].replace('Z', '')  # ISO8601 without Z
    dt = datetime.fromisoformat(time)

    # Unique game ID: Away_Home_YYYYMMDD_HHMM
    game_id = f"{away}_{home}_{dt.strftime('%Y%m%d_%H%M')}"

    for book in game['bookmakers']:
        book_name = book['title']

        for market in book['markets']:
            market_type = market['key']  # h2h, spreads, totals

            for outcome in market['outcomes']:
                team = outcome.get('name', '')
                odds = outcome['price']
                point = outcome.get('point', '')

                rows.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'game_id': game_id,
                    'matchup': f"{away} @ {home}",
                    'team': team,
                    'bookmaker': book_name,
                    'market': market_type,
                    'odds': odds,
                    'point': point,
                    'game_time': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'game_date': dt.date(),
                    'game_hour': dt.hour,
                    'game_minute': dt.minute
                })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Append to line_log.csv or create it if missing
try:
    existing = pd.read_csv('line_log.csv')
    df = pd.concat([existing, df], ignore_index=True)
except FileNotFoundError:
    pass

df.to_csv('line_log.csv', index=False)
print("✅ Logged current snapshot to line_log.csv")