import apps.fancylib as fl
import re

SEL_IDX = 0
SEL_ID = "system"
SEL_FAV = False
SHOW_HIDDEN = False

self_about = {
    "name": "Fancy App Selector", "desc": "A simple and fancy app selector.", "ver": "1.0.2", "hidden": False,
    "author" : "VincTBest",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/fancy.py",
}
app = fl.FancyApp(self_about)
app.add_action("toggle_hidden", ["h"])
app.add_action("favourite", ["f"])

def get_about():
    return app.about

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, _COMMANDS: dict):
    global SEL_IDX, SEL_ID, SHOW_HIDDEN, SEL_FAV
    SEL_FAV = False
    new_store = None

    if SANDBOXED:
        app.printc(f"Fancy App Selector is Sandboxed. To open it run 'fancy' in 'system'!{app.c.DARK} Exiting to default app...", app.c.ERROR)
        return None, ":(", None, None  # Number 2 can be anything, because when sandboxed it will always go to the default app.

    apps = fl.get_apps(MODULES, SHOW_HIDDEN)
    print_str = ""
    idx = 0
    for k,v in apps:
        name = v.get_about()["name"]
        favourite = ""
        this_fav = k in STORE.get("fancyFavourites", [])
        if this_fav:
            favourite = app.c.ACCENT+" * "

        if idx == SEL_IDX:
            name = f"{app.c.ACCENT}> "+favourite+app.c.BRIGHT+name+f"{app.c.ACCENT} <"
            SEL_ID = k
            SEL_FAV = this_fav
        else:
            name = favourite + app.c.DARK + name
        print_str = print_str+"  "+name
        idx += 1

    app.printc(print_str)

    this_about = MODULES[SEL_ID].get_about()
    this_author = this_about.get("author", "Unknown")
    about_str = str(this_about["desc"])
    ansi = re.compile(r'\x1b\[[0-9;]*m')
    print_len = len(ansi.sub("", print_str))
    for i in range(print_len-len(about_str)-2-3-5-len(this_author)-len(this_about["ver"])-2-1-1):
        about_str = about_str + " "

    app.printc(f"  {about_str}  Made by {app.c.BRIGHT}{this_author}  {app.c.ACCENT}{this_about["ver"]}", app.c.MID)
    #action = input(f"{c.RESET}FancyAppSelector : {c.RESET}")

    key = fl.read_input("key")

    app.clr()

    # Control Scheme
    # WASD / IJKL / 8456 (Numpad)
    # Quit: Q / U / 7 (Numpad)
    if app.get_action(key, "left"):
        SEL_IDX = (SEL_IDX - 1) % len(apps)
    elif app.get_action(key, "right"):
        SEL_IDX = (SEL_IDX + 1) % len(apps)
    elif app.get_action(key, "run"):
        # Run Normally
        app.printc(f"Running {this_about['name']}.", app.c.MID)
        return None, SEL_ID, None, None
    elif app.get_action(key, "s_run"):
        # Run Sandboxed
        app.printc(f"Running {this_about['name']} sandboxed.", app.c.MID)
        return None, SEL_ID, None, True
    elif app.get_action(key, "quit"):
        # Quit
        if new_store is not None:
            app.printc("Saving Store...", app.c.MID)
            return True, None, None, new_store
        return True, None, None, None
    elif app.get_action(key, "toggle_hidden"):
        SHOW_HIDDEN = not SHOW_HIDDEN
    elif app.get_action(key, "favourite"):
        new_store = STORE
        if SEL_FAV:
            new_store["fancyFavourites"].remove(SEL_ID)
        else:
            if not new_store.get("fancyFavourites"):
                new_store["fancyFavourites"] = []
            new_store["fancyFavourites"].append(SEL_ID)
    else:
        app.printc(f"Control Scheme:", app.c.cols["GREEN"])
        app.printc(f"  Left / Right  : A;D / J;L / 4;6 (Numpad) / Left;Right (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"  Quit          : Q   / U   / 7   (Numpad) / PageUp     (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"  Run           : S   / K   / 5   (Numpad) / Down       (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"  Run Sandboxed : W   / I   / 8   (Numpad) / Up         (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"  Show Hidden   : H (Toggle)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"  Favourite     : F", app.c.cols["LIGHT_GREEN"])
        print()

    if new_store is not None:
        app.printc("Saving Store...", app.c.MID)
        return None, None, None, new_store

    return None, None, None, None
