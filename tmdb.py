import json
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()
tmdb = os.getenv("tmdb")
dwif = os.getenv("dwif")

def process_dwif(poster):
    poster = "https://wsrv.nl/?url=" + poster + "&w=1000&h=1000&fit=cover&a=attention&output=png"
    if dwif:
        poster = dwif + "/api/process?radius=73&url=" + quote(poster)

    return poster

def get_progress_string(progress, runtime):
    #print(f"Calculating progress string with progress: {progress}, runtime: {runtime}")
    if runtime == 0 or runtime is None:
        return "Progress: N/A"
    else:
        watched_minutes = (progress / 100) * runtime

        # Format the proggress's to "1h 13m" or "56m" format
        watched_pretty = f"{int(watched_minutes // 60)}h {int(watched_minutes % 60)}m" if watched_minutes >= 60 else f"{int(watched_minutes)}m"
        runtime_pretty = f"{int(runtime // 60)}h {int(runtime % 60)}m" if runtime >= 60 else f"{int(runtime)}m"
        return f"{watched_pretty} / {runtime_pretty}"

def generate_new_movie_data(tmdb_id, progress, pmdb_runtime):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("adult", True): 
            return None

        runtime = data.get("runtime") or pmdb_runtime
        progress_string = get_progress_string(progress, runtime)
        poster = "www.themoviedb.org/t/p/w1280" + data.get("poster_path", "")

        new_data = {
            "data": {
                "dynamic": [
                {
                    "type": 3,
                    "name": "heroImage",
                    "value": {
                        "url": process_dwif(poster)
                    }
                },
                {
                    "type": 3,
                    "name": "miniImage",
                    "value": {
                        "url": "https://wsrv.nl/?url=" + poster + "&w=1000&h=1000&fit=cover&a=attention&output=png"
                    }
                },
                {
                    "type": 1,
                    "name": "heroTitle",
                    "value": data.get("title", "") + " (" + data.get("release_date", "")[:4] + ")"
                },
                {
                    "type": 1,
                    "name": "subtitle",
                    "value": f'"{data.get("tagline", "")}"'
                },
                {
                    "type": 1,
                    "name": "progressString",
                    "value": progress_string
                },
                {
                    "type": 2,
                    "name": "progressBar",
                    "value": progress / 100
                }
                ]
            }
        }

        return new_data

def generate_new_tv_data(tmdb_id, progress, pmdb_runtime, season, episode):
    details_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={tmdb}"
    episode_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season}/episode/{episode}?api_key={tmdb}"

    details = requests.get(details_url)
    episode_details = requests.get(episode_url)
    if details.status_code == 200 and episode_details.status_code == 200:
        data = details.json()
        episode_data = episode_details.json()
        if data.get("adult", True): 
            return None

        runtime = episode_data.get("runtime") or pmdb_runtime
        progress_string = get_progress_string(progress, runtime)
        seasons = data.get("seasons", [{}])
        poster = "www.themoviedb.org/t/p/w1280/" + data.get("poster_path", "")
        for season_info in seasons:
            if season_info.get("season_number") == season:
                poster = "www.themoviedb.org/t/p/w1280" + season_info["poster_path"] if season_info.get("poster_path") else poster
                break

        new_data = {
            "data": {
                "dynamic": [
                    {
                        "type": 3,
                        "name": "heroImage",
                        "value": {
                            "url": process_dwif(poster)
                        }
                    },
                    {
                        "type": 3,
                        "name": "miniImage",
                        "value": {
                        "url": "https://wsrv.nl/?url=" + poster + "&w=1000&h=1000&fit=cover&a=attention&output=png"
                        }
                    },
                    {
                        "type": 1,
                        "name": "heroTitle",
                        "value": data.get("name", "") + f": S{season}E{episode}" + " (" + data.get("first_air_date", "")[:4] + ")"
                    },
                    {
                        "type": 1,
                        "name": "subtitle",
                        "value": f'"{data.get("tagline", "")}"' if data.get("tagline") else episode_data.get("name", "")
                    },
                    {
                        "type": 1,
                        "name": "progressString",
                        "value": progress_string
                    },
                    {
                        "type": 2,
                        "name": "progressBar",
                        "value": progress / 100
                    }
                ]
            }
        }

        #print(json.dumps(new_data, indent=4))  # Print the new_data for debugging
        return new_data