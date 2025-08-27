import time
import requests





def countdown(seconds):
    for s in range(int(seconds), 0, -1):
        print(f"\rretry in {s}s ", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 20 + "\r", end="", flush=True)

def getJsonWithRetry(url, delaySeconds=400, timeoutSeconds=15):
    while True:
        try:
            response = requests.get(url, timeout=timeoutSeconds)
            if response.status_code == 429:
                print(f"rate limited (429). waiting {delaySeconds}s then trying again...")
                countdown(delaySeconds)
                continue
            response.raise_for_status()
        
        except requests.exceptions.Timeout:
            print(f"timeout. waiting {delaySeconds}s then trying again...")
            countdown(delaySeconds)
        
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred:", e)
        
        except requests.exceptions.RequestException as e:
            print("A request error occurred:", e)

        except Exception as e:
            print(f"Fatal error for {url}: {e}")
        
        return response.json()



