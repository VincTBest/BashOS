import apps.fancylib as fl
import time
import main
import datetime
import readchar

self_about = {"name": "FancyStats", "desc": "See system info and statistics.", "ver": "1.0.0", "hidden": False,
    "author" : "VincTBest",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/stats.py",}
app = fl.FancyApp(self_about)

def get_about():
    return app.about

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    app.printc("Stats:", app.c.ACCENT)

    apps = str(len(MODULES))
    if SANDBOXED: apps = "Sandboxed, can't display."
    app.printc("Apps: "+apps)

    commands = str(len(COMMANDS))
    if SANDBOXED: commands = "Sandboxed, can't display."
    app.printc("Commands: "+commands)

    uptime = datetime.timedelta(seconds=time.time()-main.START_TIME)
    app.printc("Uptime: "+str(uptime))

    action = readchar.readkey()
    if app.get_action(action, "quit"):
        return None, app.DEF_APP, None, None
    app.clr()

    return None, None, None, None
