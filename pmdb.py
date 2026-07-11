import requests
import json
import datetime

pmdb_api = "https://publicmetadb.com/api"

def parse_pmdb_timestamp(timestamp_value):
    if not timestamp_value:
        return None

    normalized_timestamp = timestamp_value.replace(" ", "T")

    if normalized_timestamp.endswith("Z"):
        normalized_timestamp = normalized_timestamp[:-1] + "+00:00"

    try:
        return datetime.datetime.fromisoformat(normalized_timestamp)
    except ValueError:
        return None

def get_resume_points(pmdb_key):
    url = f"{pmdb_api}/external/resume"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pmdb_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()

def get_watch_history(pmdb_key):
    url = f"{pmdb_api}/external/watched"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {pmdb_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()

def get_pmdb_data(pmdb_key):
    resume_points = get_resume_points(pmdb_key)
    history = get_watch_history(pmdb_key)

    if resume_points and resume_points.get("total", 0) > 0:
        resume_point = resume_points.get("items", [{}])[0]
        updated_at = parse_pmdb_timestamp(resume_point.get("updated", "2000-03-10T09:30:00Z"))

        if history and history.get("total", 0) > 0:
            history_point = history.get("items", [{}])[0]
            history_point["progress"] = 100

            watched_at = parse_pmdb_timestamp(history_point.get("watched_at", "2000-03-10T09:30:00Z"))
            point = history_point if watched_at and watched_at > updated_at else resume_point

            if point:
                return point

        if updated_at and updated_at > datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=12):
            return resume_point

    if history and history.get("total", 0) > 0:
        point = history.get("items", [{}])[0]

        if point:
            point["progress"] = 100
            return point