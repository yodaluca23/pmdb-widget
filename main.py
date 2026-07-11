from pmdb import get_pmdb_data
from tmdb import generate_new_movie_data, generate_new_tv_data
from updateWidget import update_widget
import json
from dotenv import load_dotenv
import os
from time import sleep
load_dotenv()

test_pmdb_key = os.getenv("pmdb_key")
test_user = os.getenv("discord_user")

old_data = None

def update(pmdb_key, user_id):
    global old_data
    pmdb_data = get_pmdb_data(pmdb_key)

    if pmdb_data:
        if old_data is not None and pmdb_data == old_data:
            print("No changes detected. Widget not updated.")
            return
        else:
            old_data = pmdb_data

        tmdb_id = pmdb_data.get("tmdb_id")
        progress = pmdb_data.get("progress", 0)
        media_type = pmdb_data.get("media_type")

        if media_type == "movie":
            new_data = generate_new_movie_data(tmdb_id, progress, pmdb_data.get("runtime_ms", 0)/60000)
        elif media_type == "tv":
            season = pmdb_data.get("season", 1)
            episode = pmdb_data.get("episode", 1)
            new_data = generate_new_tv_data(tmdb_id, progress, pmdb_data.get("runtime_ms", 0)/60000, season, episode)
        else:
            print(f"Unsupported media type: {media_type}")
            return

        if new_data:
            response = update_widget(user_id, new_data)
            print(f"Widget updated for user {user_id}. Response: {response.status_code}")
        else:
            print(f"No new data generated for TMDB ID: {tmdb_id}")
    else:
        print("No PMDB data found or no recent resume/watch history.")

if __name__ == "__main__":

    while True:
        try:
            update(test_pmdb_key, test_user)
        except Exception as e:
            print(f"Error occurred: {e}")
            
        sleep(15)  # Wait for 15 seconds before the next update