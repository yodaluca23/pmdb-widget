import os
import requests
from dotenv import load_dotenv
import json
load_dotenv()
fanart_api_key = os.getenv("fanart_api_key")
pmdb_api_key = os.getenv("pmdb_key")

def tmdb_to_tvdb(tmdb_id):
    api_endpoint = f"https://publicmetadb.com/api/external/mappings?tmdb_id={tmdb_id}&media_type=tv"
    headers = {
        "Authorization": f"Bearer {pmdb_api_key}"
    }
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("mappings", {}).get("tvdb", [{}])[0].get("value", None)
    return None

def fetch_fanart_poster(tmdb_id, isTv, season=None):
    media_type = "tv" if isTv else "movies"
    id = tmdb_to_tvdb(tmdb_id) if isTv else tmdb_id
    #print(f"TMDB ID: {tmdb_id}, TVDB ID: {id}, Media Type: {media_type}, Season: {season}")
    if id is None:
        return None

    #print(f"Fetching fanart poster for TMDB ID: {tmdb_id}, TVDB ID: {id}, Media Type: {media_type}, Season: {season}")

    url = f"https://webservice.fanart.tv/v3.2/{media_type}/{id}" 
    querystring = {"api_key": fanart_api_key}
    response = requests.get(url, params=querystring)
    data = response.json()
    if season is not None and "seasonposter" in data:
        season_posters = data["seasonposter"]
        sorted_season_posters = sorted(season_posters, key=lambda x: x["likes"], reverse=True)
        season_poster = next((poster for poster in sorted_season_posters if poster["season"] == season), None)
        if season_poster:
            print(f"Season Poster URL: {season_poster['url']}")
            return season_poster["url"]
    
    show_posters = data.get("tvposter", data.get("movieposter", []))
    sorted_show_posters = sorted(show_posters, key=lambda x: x["likes"], reverse=True)
    show_poster = next((poster for poster in sorted_show_posters if poster["lang"] == "00"), None)
    if show_poster:
        print(f"Show Poster URL: {show_poster['url']}")
        return show_poster["url"]

    #print(json.dumps(data, indent=4))  # Print the response for debugging
    return None