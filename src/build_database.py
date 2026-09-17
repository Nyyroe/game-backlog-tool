"""
Loads enriched library into SQLite database
"""

import sqlite3
import pandas as pd

ENRICHED_PATH = "data/enriched_library.csv"
DB_PATH = "data/games.db"

def build_database(csv_path: str = ENRICHED_PATH, db_path: str = DB_PATH) -> None:
    df = pd.read_csv(csv_path)

    # Opens/Creates database at path
    conn = sqlite3.connect(db_path)
    df.to_sql("games", conn, if_exists="replace", index=False)

    # Close db connection
    conn.close()

if __name__ == "__main__":
    build_database()
    print(f"Database built at {DB_PATH}")