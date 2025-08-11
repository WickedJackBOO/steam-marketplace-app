import requests
from bs4 import BeautifulSoup
import xmltodict
import json

accountUrl = "https://steamcommunity.com/id/WickedJackBOO/games?xml=1"
cardsUrl = "https://raw.githubusercontent.com/nolddor/steam-badges-db/main/data/badges.json"

response = requests.get(accountUrl)
soup = BeautifulSoup(response.content, "xml")
xmlStr = str(soup)

jsonData = xmltodict.parse(xmlStr)
# jsonStr = json.dumps(jsonData, indent=1)

# with open('myGames.json', 'w') as f:
    # json.dump(jsonData, f)




response = requests.get(cardsUrl)
GamesWithCardsData = response.json()
# with open('cards.json', 'w') as f:
    # json.dump(GamesWithCardsData, f)




for game in jsonData["gamesList"]["games"]["game"]:
    if game["appID"] in GamesWithCardsData:
        print (game["name"])
