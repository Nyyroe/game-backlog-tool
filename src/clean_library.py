"""
Loads the raw Steam Library JSON and produces a cleaner DataFrame with pandas
"""

import json
import pandas as pd

RAW_PATH = "data/raw_steam_library.json"
CLEAN_PATH = "data/clean_library.csv"

def load_and_clean_library(json_path: str = RAW_PATH) -> pd.DataFrame:
    with open(json_path, "r") as f:
        raw_games = json.load(f)
    df = pd.DataFrame(raw_games)
    df = df[["appid","name", "playtime_forever"]]
    # clean playtime into hours
    df["playtime_hours"] = round(df["playtime_forever"]/60, 1)
    df = df.drop(columns=["playtime_forever"])
    df = df.sort_values("name").reset_index(drop=True)
    return df

# test statement
if __name__ == "__main__":
    df = load_and_clean_library()
    df.to_csv(CLEAN_PATH, index = False)

    print(f"Cleaned {len(df)} games")
    print(f"Total Hours Played: {df['playtime_hours'].sum():.1f}")
    print(f"Saved to {CLEAN_PATH}")