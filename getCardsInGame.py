import json
import requests
import time
from usefulFunctions import getJsonWithRetry

print("Start")

with open("savedGames.json", "r") as file:
    savedGames = json.load(file)

for game in savedGames:
    cards = []
    print(savedGames[game]["name"])
    urls = [
        f"https://steamcommunity.com/market/search/render/?appid=753&norender=1&category_753_cardborder[]=tag_cardborder_0&category_753_Game[]=tag_app_{game}", # Normal cards
        f"https://steamcommunity.com/market/search/render/?appid=753&norender=1&category_753_cardborder[]=tag_cardborder_1&category_753_Game[]=tag_app_{game}" # Foil cards
    ]
    for url in urls:
        foil = "cardborder_1"in url
        jsonDump = getJsonWithRetry(url)
        results = jsonDump["results"]
        for item in results:
            assetDescription = item.get("asset_description", {})
            saveJsonDump = {
                "foil": foil,
                "name": item.get("name",""),
                "hash_name": item.get("hash_name",""),
                "tradable": assetDescription.get("tradable",""),
                "icon_url": assetDescription.get("icon_url",""),
                "commodity": assetDescription.get("commodity","")
            }
            cards.append(saveJsonDump)
    savedGames[game]["cards"] = cards
    

with open("savedGames.json", "w") as file:
    json.dump(savedGames, file, indent=4)
