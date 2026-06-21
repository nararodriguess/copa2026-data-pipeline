import streamlit as st
import psycopg2
import pandas as pd
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "database": os.getenv("DB_NAME", "copa2026"),
    "user": os.getenv("DB_USER", "copa"),
    "password": os.getenv("DB_PASSWORD", "copa123")
}

@st.cache_data(ttl=300)
def load_rankings():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM team_rankings ORDER BY points DESC, goal_difference DESC", conn)
    conn.close()
    return df

@st.cache_data(ttl=300)
def load_matches():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM matches WHERE status = 'FINISHED' ORDER BY match_date DESC", conn)
    conn.close()
    return df

st.set_page_config(page_title="Copa 2026 Dashboard", page_icon="⚽", layout="wide")

st.title("⚽ FIFA World Cup 2026")
st.caption("Data updated hourly via football-data.org API")

col1, col2, col3 = st.columns(3)

rankings = load_rankings()
matches = load_matches()

with col1:
    st.metric("Teams", len(rankings))
with col2:
    st.metric("Matches Played", len(matches))
with col3:
    st.metric("Goals Scored", int(matches["home_score"].sum() + matches["away_score"].sum()))

st.subheader("🏆 Team Rankings")
st.dataframe(rankings, use_container_width=True, hide_index=True)

st.subheader("📅 Recent Matches")
st.dataframe(matches[["match_date", "home_team", "home_score", "away_score", "away_team", "stage"]],
             use_container_width=True, hide_index=True)