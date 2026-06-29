import apps.fancylib as fl
import re

SEL_IDX = 0
SEL_ID = "system"

self_about = {
    "name": "Fancy App Selector", "desc": "A simple and fancy app selector.", "ver": "0.0.0", "hidden": False
}
app = fl.FancyApp(self_about)

def clamp(n, low, high):
    if n < low:
        return low
    if n > high:
        return high
    return n

def get_about():
    return app.about

def run(MODULES: dict, _STORE: dict, SANDBOXED: bool, _COMMANDS: dict):
    global SEL_IDX, SEL_ID

    if SANDBOXED:
        app.printc(f"Fancy App Selector is Sandboxed. To open it run 'fancy' in 'system'!{app.c.DARK} Exiting to default app...", app.c.ERROR)
        return None, ":(", None, None  # Number 2 can be anything, because when sandboxed it will always go to the default app.

    apps = fl.get_apps(MODULES)
    print_str = ""
    idx = 0
    for k,v in apps:
        name = v.get_about()["name"]
        if idx == SEL_IDX:
            name = f"{app.c.ACCENT}> "+app.c.BRIGHT+name+f"{app.c.ACCENT} <"
            SEL_ID = k
        else:
            name = app.c.DARK + name
        print_str = print_str+"  "+name
        idx += 1

    app.printc(print_str)

    this_about = MODULES[SEL_ID].get_about()
    about_str = str(this_about["desc"])
    ansi = re.compile(r'\x1b\[[0-9;]*m')
    print_len = len(ansi.sub("", print_str))
    for i in range(print_len-len(about_str)-len(this_about)-2-1-2): # ~40 - ~20 < ~20?
        about_str = about_str + " "

    app.printc(f"  {about_str}  {app.c.ACCENT}{this_about["ver"]}", app.c.MID)
    #action = input(f"{c.RESET}FancyAppSelector : {c.RESET}")

    key = fl.read_input("key")

    app.clr()

    # Control Scheme
    # WASD / IJKL / 8456 (Numpad)
    # Quit: Q / U / 7 (Numpad)

    if app.get_action(key, "left"):
        # Left
        SEL_IDX -= 1
        SEL_IDX = clamp(SEL_IDX, 0, len(apps)-1)
    elif app.get_action(key, "right"):
        # Right
        SEL_IDX += 1
        SEL_IDX = clamp(SEL_IDX, 0, len(apps)-1)
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
        return True, None, None, None
    else:
        app.printc(f"Control Scheme :", app.c.cols["GREEN"])
        app.printc(f"Left / Right  : A;D / J;L / 4;6 (Numpad) / Left;Right (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"Quit          : Q   / U   / 7   (Numpad) / PageUp     (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"Run           : S   / K   / 5   (Numpad) / Down       (Arrows)", app.c.cols["LIGHT_GREEN"])
        app.printc(f"Run Sandboxed : W   / I   / 8   (Numpad) / Up         (Arrows)", app.c.cols["LIGHT_GREEN"])

    return None, None, None, None
