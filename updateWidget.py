import json
import requests
import os
from dotenv import load_dotenv
from tmdb import generate_new_movie_data, generate_new_tv_data

load_dotenv()
bot_token = os.getenv("discord_bot")
app_id = os.getenv("discord_app")
test_user = os.getenv("discord_user")

def update_widget(user_id, new_data):
    url = f"https://discord.com/api/v9/applications/{app_id}/users/{user_id}/identities/0/profile"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    response = requests.patch(url, headers=headers, json=new_data)
    return response

#update_widget(test_user, generate_new_movie_data(1083381, 23))
#update_widget(test_user, generate_new_tv_data(94997, 69, 2, 3))