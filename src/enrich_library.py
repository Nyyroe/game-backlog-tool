"""
Enriches the cleaned library with additional data from a public steam dataset,
with estimated completion times drawn from HowLongToBeat
"""
import numpy as np
import pandas as pd
from howlongtobeatpy import HowLongToBeat

CLEAN_PATH = "data/clean_library.csv"
KAGGLE_DATASET_PATH = "data/steam_games_dataset.csv"
ENRICHED_PATH = "data/enriched_library.csv"

def add_genre_data(library_df: pd.DataFrame) -> pd.DataFrame:

    # Left join keeps every owned game, even if it doesn't find a match in the dataset
    genres_df = pd.read_csv(KAGGLE_DATASET_PATH)

    # Declutter so we are only using necessary columns from steam dataset
    genres_df = genres_df[["AppID", "Genres", "Positive", "Negative"]]

    genres_df["AppID"] = pd.to_numeric(genres_df["AppID"], errors="coerce")
    genres_df = genres_df[np.isfinite(genres_df["AppID"])]

    genres_df["AppID"] = genres_df["AppID"].astype("int64")

    merged = pd.merge(
        library_df, genres_df, left_on="appid", right_on="AppID", how="left"
    )    
    merged = merged.drop(columns=["AppID"])

    # Get rating score
    merged["rating_pct"] = round(
        merged["Positive"] / (merged["Positive"] + merged["Negative"]) * 100, 1, 
    )

    return merged

def get_time_to_beat(game_name: str) -> float | None:

    print(f"Looking up: {game_name}")    # TEMP PROGRESS TRACKER
    # If found, return estimated main story completion time
    results = HowLongToBeat().search(game_name)
    if not results:
        return None
    best_match = max(results, key=lambda r: r.similarity)
    return best_match.main_story

def add_completion_times(df: pd.DataFrame) -> pd.DataFrame:
    df["hours_to_beat"] = df["name"].apply(get_time_to_beat)
    return df

# yay more test statements
if __name__ == "__main__":
    library = pd.read_csv(CLEAN_PATH)
    enriched = add_genre_data(library)
    enriched = add_completion_times(enriched)
    enriched.to_csv(ENRICHED_PATH, index=False)

    print(f"Enriched {len(enriched)} games. Saved to {ENRICHED_PATH}")
