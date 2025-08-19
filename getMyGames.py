import requests
from bs4 import BeautifulSoup
import xmltodict
import json
from datetime import datetime,timedelta
import os

accountName = "WickedJackBOO"

apiInfo = {
    "account":{
        "infoType":"xml", # account name here V V V V
        "url":f"https://steamcommunity.com/id/{accountName}/games?xml=1",
        "fileSaveName":"account.json"
    },
    "cards":{
        "infoType":"json",
        "url":"https://raw.githubusercontent.com/nolddor/steam-badges-db/main/data/badges.json",
        "fileSaveName":"cards.json"
    }
}
startRunTime = datetime.now()
print(f"Start time {startRunTime}")

for info in apiInfo:
    exists = os.path.exists(apiInfo["account"]["fileSaveName"]) and os.path.exists(apiInfo["cards"]["fileSaveName"]) 
    infoType = apiInfo[info]["infoType"]
    url = apiInfo[info]["url"]
    fileSaveName = apiInfo[info]["fileSaveName"]
    if exists:
        modTime = datetime.fromtimestamp(os.path.getmtime(fileSaveName))
        ping = (startRunTime-modTime)>timedelta(days=7)
    else:
        ping = True
    if ping:
        if exists:
            print(f"{fileSaveName} is {startRunTime-modTime} old and will be updated")
        else:
            print(f"A file is missing getting info for {fileSaveName}")
        try:
            response = requests.get(url)
            if infoType == "xml":
                soup = BeautifulSoup(response.content, "xml")
                xmlStr = str(soup)
                dataDump = xmltodict.parse(xmlStr)
            if infoType == "json":
                dataDump = response.json()
            
            with open(fileSaveName, 'w') as f:
                json.dump(dataDump, f)
        except Exception as e:
            print(f"oops something happened \n{e}")
    
with open(apiInfo["account"]["fileSaveName"]) as file:
    accountJson = json.load(file)
with open(apiInfo["cards"]["fileSaveName"]) as file:
    cardsJson = json.load(file)

savedGames = {}

for game in accountJson["gamesList"]["games"]["game"]:
    if game["appID"] in cardsJson:
        savedGames[game["appID"]] = {
            "name": cardsJson[game["appID"]]["name"],
            "numberOfCards": cardsJson[game["appID"]]["size"],
            "cards": [],
            "cardPack": []
        }
        print(game["name"])

with open("savedGames.json", "w") as file:
    json.dump(savedGames, file, indent=4) 

print("game info saved")

