import json
import psycopg2
import logging
import os


logger = logging.getLogger(__name__)

DB_CONFIG = { 
    "host": os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                home_team VARCHAR (100),
                away_team VARCHAR (100),
                home_score INTEGER,
                away_score INTEGER,
                status VARCHAR (50),
                stage VARCHAR (100),
                match_date TIMESTAMP
            );
        """)
        conn.commit()
        logger.info("Table 'matches' ready.")


def transform_and_load(conn):
    with open("/opt/airflow/data/raw/games.json", "r") as f:
        data = json.load(f)

    matches = data.get("matches", [])
    inserted = 0
    updated = 0

    with conn.cursor() as cur:
        for match in matches:
            score = match.get("score", {}).get("fullTime", {})  # retorna None se não existir
            cur.execute("""
                INSERT INTO matches (id, home_team, away_team, home_score, away_score, status, stage, match_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    home_score = EXCLUDED.home_score,
                    away_score = EXCLUDED.away_score,
                    status = EXCLUDED.status;
            """, (
                match["id"],
                match["homeTeam"]["name"],
                match["awayTeam"]["name"],
                score.get("home"),
                score.get("away"),
                match["status"],
                match["stage"],
                match["utcDate"]
            ))
            if cur.rowcount == 1:
                inserted += 1
            else:
                updated += 1

        conn.commit()
    logger.info(f"Inserted {inserted} new matches and updated {updated} existing matches.")


def run ():
    conn = None
    try:
        logger.info(f"Connecting to database with config: {DB_CONFIG}")
        conn = psycopg2.connect(**DB_CONFIG)
        create_table(conn)
        transform_and_load(conn)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise # relança o erro — o Airflow marca como failed
    finally:
        if conn:
            conn.close()
            logger.info("Connection closed.")
    logger.info("Process completed successfully.")