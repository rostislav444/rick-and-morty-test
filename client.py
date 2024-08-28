import json
import os
from fastapi import HTTPException

from typing import Any

import httpx

from utils.fetch_and_save_data import fetch_and_save_data


class Client:
    BASE_URL = "https://rickandmortyapi.com/api"

    async def _fetch_data(self, endpoint: str, force_update: bool = False) -> Any:
        filename = f"data/{endpoint}.json"

        if not force_update and os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)

        try:
            return await fetch_and_save_data(self.BASE_URL, endpoint, filename)
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"API request error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    async def _get_data(self, endpoint: str, force_update: bool) -> Any:
        data = await self._fetch_data(endpoint, force_update)
        return data["RawData"]

    async def fetch_all_data(self) -> Any:
        characters = await self._fetch_data("character", True)
        locations = await self._fetch_data("location", True)
        episodes = await self._fetch_data("episode", True)
        return {"characters": characters, "locations": locations, "episodes": episodes}

    async def get_characters(self, force_update: bool = False) -> Any:
        return await self._get_data("character", force_update)

    async def get_locations(self, force_update: bool = False) -> Any:
        return await self._get_data("location", force_update)

    async def get_episodes(self, force_update: bool = False) -> Any:
        return await self._get_data("episode", force_update)
