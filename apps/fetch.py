import const
import readchar
import requests

about = {"name": "Fetch", "desc": "Fetch APIs from the web.", "ver": "1.0.0", "hidden": False}
c = const.Colors()

def get_about():
    return about

def run(*args):
    action = input("Fetch : ")
    const.clr()
    if action != "exit":
        print(c.DARK_GRAY+"Fetching from "+action+"..."+c.RESET)
        response = requests.get(action)
        if response.status_code == 200:
            print(response.json())
        else:
            print(c.RED+"Error! Status code: "+str(response.status_code)+"."+c.RESET)

        response.close()
    else:
        return None, const.DEFAULT_APP, None, None

    return None, None, None, None
