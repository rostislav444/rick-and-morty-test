from fastapi import FastAPI

from client import Client
from utils.filter import filter_episode_year_by_range

app = FastAPI()
client = Client()


@app.get("/fetch-data")
async def fetch_data():
    response = await client.fetch_all_data()
    return response


@app.get("/")
async def episodes_in_range():
    episodes = await client.get_episodes()
    year_start = 2017
    year_end = 2021

    filtered_names = [episode['name'] for episode in episodes if
                      filter_episode_year_by_range(episode, year_start, year_end)]
    return filtered_names
