import requests
import json
import time
from usefulFunctions import getJsonWithRetry # type: ignore

print("Start")


with open("savedGames.json", "r") as file:
    savedGames = json.load(file)

for game in savedGames:
    cards = []
    print(savedGames[game]["name"])
    url = f"https://steamcommunity.com/market/search/render/?appid=753&norender=1&category_753_Game[]=tag_app_{game}&query=booster%20pack"
    jsonDump = getJsonWithRetry(url)
    results = jsonDump["results"]
    for item in results:
        saveJsonDump = {
            "name": item.get("name",""),
            "hash_name": item.get("hash_name",""),
            "icon_url": item.get("icon_url",""),
        }
        cards.append(saveJsonDump)
    savedGames[game]["cardPack"] = cards

with open("savedGames.json", "w") as file:
    json.dump(savedGames, file, indent=4)

