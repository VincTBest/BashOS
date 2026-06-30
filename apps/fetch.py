import const
import requests

about = {"name": "Fetch", "desc": "Fetch APIs from the web.", "ver": "1.0.2", "hidden": False,
    "author" : "VincTBest",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/fetch.py",}

c = const.Colors()

def get_about():
    return about

def run(*args):
    action = input("Fetch : ")
    const.clr()
    if action != "exit":
        print(c.cols["DARK_GRAY"]+"Fetching from "+action+"..."+c.cols["RESET"])
        try:
            response = requests.get(action)
            if response.status_code == 200:
                print(response.json())
            else:
                print(c.cols["red"]+"Error! Status code: "+str(response.status_code)+"."+c.cols["RESET"])

            response.close()
        except:
            print(c.cols["red"]+f"Error! Could not fetch from {action}."+c.cols["RESET"])
    else:
        return None, const.DEFAULT_APP, None, None

    return None, None, None, None
