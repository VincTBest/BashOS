import const
import time
import main
import datetime
import readchar

c = const.Colors()


def get_about():
    return {"name": "FancyStats", "desc": "See system info and statistics.", "ver": "1.0.0", "hidden": False}

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    global c
    print(f"{c.YELLOW}Stats:{c.RESET}")
    apps = str(len(MODULES))
    if SANDBOXED: apps = "Sandboxed, can't display."
    print(f"Apps: "+apps)
    uptime = datetime.timedelta(seconds=time.time()-main.START_TIME)
    print(f"Uptime: {str(uptime)}")
    action = readchar.readkey()
    if action == "q" or action == "u" or action == "7" or action == readchar.key.PAGE_UP:
        return None, const.DEFAULT_APP, None, None
    const.clr()
    return None, None, None, None
