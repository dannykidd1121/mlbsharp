import pandas as pd

# Load the full line history
df = pd.read_csv('line_log.csv')

# Convert timestamp to datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sort by time to ensure order
df = df.sort_values(by='timestamp')

# Fields that define a unique line stream
key_fields = ['game_id', 'team', 'bookmaker', 'market']

# Get opening odds (first snapshot)
open_df = df.groupby(key_fields).first().reset_index()
open_df = open_df.rename(columns={'odds': 'open_odds', 'timestamp': 'open_time'})

# Get latest odds (last snapshot)
latest_df = df.groupby(key_fields).last().reset_index()
latest_df = latest_df.rename(columns={'odds': 'latest_odds', 'timestamp': 'latest_time'})

# Merge open + latest
merged = pd.merge(open_df, latest_df, on=key_fields)

# Calculate raw delta and percent delta (keep numerics separate for logic)
merged['delta'] = (merged['latest_odds'] - merged['open_odds']).round(2)
merged['delta_pct_num'] = ((merged['delta'] / merged['open_odds']) * 100).round(2)
merged['abs_pct_num'] = merged['delta_pct_num'].abs()

# Label direction
merged['direction'] = merged['delta'].apply(
    lambda x: '🔻 down' if x < 0 else ('🔺 up' if x > 0 else '⏸ no change')
)

# Filter: keep only lines with significant % movement
merged = merged[merged['abs_pct_num'] >= 2.5]

# Sort: biggest % movers first within each market
merged = merged.sort_values(by=['market', 'abs_pct_num'], ascending=[True, False])

# Format % columns for display
merged['delta_pct'] = merged['delta_pct_num'].astype(str) + '%'
merged['abs_pct'] = merged['abs_pct_num'].astype(str) + '%'

# Save to CSV
merged.to_csv('line_delta_report.csv', index=False)
print("✅ Delta report saved to line_delta_report.csv")