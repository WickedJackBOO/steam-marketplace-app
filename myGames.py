import requests
from bs4 import BeautifulSoup
import xmltodict
import json
from datetime import datetime,timedelta
import os
import time

apiInfo = {
    "account":{
        "infoType":"xml", # account name here V V V V
        "url":"https://steamcommunity.com/id/WickedJackBOO/games?xml=1",
        "fileSaveName":"cards.json"
    },
    "cards":{
        "infoType":"json",
        "url":"https://raw.githubusercontent.com/nolddor/steam-badges-db/main/data/badges.json",
        "fileSaveName":"myGames.json"
    }
}
startRunTime = datetime.now()
print(f"Start time {startRunTime}")

for info in apiInfo:
    infoType = apiInfo[info]["infoType"]
    url = apiInfo[info]["url"]
    fileSaveName = apiInfo[info]["fileSaveName"]
    modTime = datetime.fromtimestamp(os.path.getmtime(fileSaveName))
    ping = (startRunTime-modTime)>timedelta(days=7)
    # print(infoType);print(url);print(fileSaveName);print(ping)
    if ping:
        print(f"{fileSaveName} is {startRunTime-modTime} old and will be updated")
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


# print (startRunTime - modTime)


# for game in jsonData["gamesList"]["games"]["game"]:
#     if game["appID"] in GamesWithCardsData:
#         print (game["name"])


