import requests
import json
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

