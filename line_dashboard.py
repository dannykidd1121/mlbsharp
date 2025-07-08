import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv('line_log.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

st.title("📊 MLB Line Movement Dashboard")

# Sidebar filters
teams = sorted(df['team'].unique())
markets = sorted(df['market'].unique())
books = sorted(df['bookmaker'].unique())

team = st.sidebar.selectbox("Team", teams)
market = st.sidebar.selectbox("Market", markets)
book = st.sidebar.selectbox("Bookmaker", books)

# Filter data
filtered = df[
    (df['team'] == team) &
    (df['market'] == market) &
    (df['bookmaker'] == book)
].sort_values(by='timestamp')

# Display line chart
st.subheader(f"{team} | {market.upper()} | {book}")
fig, ax = plt.subplots()
ax.plot(filtered['timestamp'], filtered['odds'], marker='o', linestyle='-')
ax.set_xlabel("Timestamp")
ax.set_ylabel("Odds")
ax.set_title("Line Movement Over Time")
plt.xticks(rotation=45)
st.pyplot(fig)

# Optional: display raw data
with st.expander("🔍 Show Raw Data"):
    st.dataframe(filtered[['timestamp', 'odds']])