import os

import httpx
import json
import uuid


def create_dirs(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


async def fetch_and_save_data(base_url: str, endpoint: str, filename: str) -> dict:
    results = []
    next_page = f"{base_url}/{endpoint}"

    async with httpx.AsyncClient() as client:
        while next_page:
            response = await client.get(next_page)
            response_data = response.json()
            results.extend(response_data.get("results", []))
            next_page = response_data.get("info", {}).get("next")

    create_dirs(filename)
    data = {"id": str(uuid.uuid4()), "RawData": results}

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    return data
