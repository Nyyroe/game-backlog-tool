"""
Fetches the Steam library of an authenticated usert via Steam Web API,
saving raw response to disk.
"""

import os
import json
import requests
from dotenv import load_dotenv


# imports api key and steam id from .env file
load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

STEAM_API_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
OUTPUT_PATH = "data/raw_steam_library.json"

def get_owned_games(steam_id: str) -> list[dict]:
    """
    Return every game owned by the given Steam ID
    include_appinfo - gives us game names rather than numeric IDs
    """
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True,
        "format": "json",
    }
    response = requests.get(STEAM_API_URL, params=params)
    response.raise_for_status() # checks HTTP response code
    return response.json()["response"]["games"]

def save_library(games: list[dict], path: str = OUTPUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: 
        json.dump(games, f, indent=2)

# test statement
if __name__ == "__main__":
    games = get_owned_games(STEAM_ID)
    save_library(games)
    print(f"Fetched {len(games)} games. Saved to {OUTPUT_PATH}")
