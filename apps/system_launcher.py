import apps.system as system

def get_about():
    return {"name": "System", "desc": "A basic app launcher and terminal.", "ver": system.get_about()["ver"], "hidden": False,
    "author" : system.get_about()["author"],
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/system_launcher.py",} # The URL to your app. (for upgrades, set it to None if you don't have one.)

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    return None, "system", None, None
