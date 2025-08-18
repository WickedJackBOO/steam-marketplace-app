import json
import requests
import time

print("Start")

def countdown(seconds):
    for s in range(int(seconds), 0, -1):
        print(f"\rretry in {s}s ", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 20 + "\r", end="", flush=True)

def getJsonWithRetry(url, delaySeconds=400):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 429:
                print(f"rate limited (429). waiting {delaySeconds}s then trying again...")
                countdown(delaySeconds)
                continue
            response.raise_for_status()
        
        except requests.exceptions.Timeout:
            print(f"timeout. waiting {delaySeconds}s then trying again...")
            countdown(delaySeconds)
            delaySeconds = min(delaySeconds * 2, 30)
        
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred:", e)
        
        except requests.exceptions.RequestException as e:
            print("A request error occurred:", e)

        except Exception as e:
            print(f"Fatal error for {url}: {e}")
        
        jsonDump = response.json()
        return jsonDump


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
                "sell_listings": item.get("sell_listings",""),
                "tradable": assetDescription.get("tradable",""),
                "icon_url": assetDescription.get("icon_url",""),
                "commodity": assetDescription.get("commodity","")
            }
            cards.append(saveJsonDump)
    savedGames[game]["cards"] = cards
    

with open("savedGames.json", "w") as file:
    json.dump(savedGames, file, indent=4)
