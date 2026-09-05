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
            return False
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
            return False

        if new_data:
            response = update_widget(user_id, new_data)
            print(f"Widget updated for user {user_id}. Response: {response.status_code}")
            return True
        else:
            print(f"No new data generated for TMDB ID: {tmdb_id}")
    else:
        print("No PMDB data found or no recent resume/watch history.")

if __name__ == "__main__":

    notUpdatedCount = 0
    sleepCounter = 20
    while True:
        try:
            updated = update(test_pmdb_key, test_user)
            if updated:
                notUpdatedCount = 0

                if sleepCounter > 30:
                    print("Updates detected. Resetting sleep time to 15 seconds.")
                sleepCounter = 20
            else:
                notUpdatedCount += 1
        except Exception as e:
            print(f"Error occurred: {e}")

        if (notUpdatedCount >= 15) and (sleepCounter < 30):
            sleepCounter = 300  # Increase sleep time to 5 minutes after 15 consecutive no updates
            print("No updates for 15 consecutive checks. Increasing sleep time to 5 minutes.")
        sleep(sleepCounter)  # Wait for the current sleep time before the next update