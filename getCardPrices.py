# priceClient.py
import requests
import time
from urllib.parse import quote
from usefulFunctions import getJsonWithRetry


country = "CA"          # CA so steam does not fall back to US
language = "english"
currency = 20           # CAD
appId = 753             # community market id

results = {}
hashName = "251570-Feeling the Burn"


def makePriceUrl(hashName):
    return (
        "https://steamcommunity.com/market/priceoverview"
        f"?country={country}&language={language}&currency={currency}"
        f"&appid={appId}&market_hash_name={quote(hashName)}"
    )


url = makePriceUrl(hashName)
data = getJsonWithRetry(url)
print(data)