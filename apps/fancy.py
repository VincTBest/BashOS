import const
import readchar
import re

SEL_IDX = 0
SEL_ID = "system"
c = const.Colors() # Create ANSI-CCs Instance

keys = {
    "left" : ["a", "j", "4", "\x1b[D", readchar.key.LEFT],
    "right": ["d", "l", "6", "\x1b[C", readchar.key.RIGHT],
    "quit" : ["q", "u", "7", "\x1b[5~", readchar.key.PAGE_UP],
    "run"  : ["s", "k", "5", "\x1b[B", readchar.key.DOWN],
    "s_run": ["w", "i", "8", "\x1b[A", readchar.key.UP],
}

def key_pressed(key: str, action: str):
    return action in keys[key]

def clamp(n, low, high):
    if n < low:
        return low
    if n > high:
        return high
    return n

def get_about():
    return {"name": "Fancy App Selector", "desc": "A simple and fancy app selector.", "ver": "0.0.0", "hidden": False}

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    global SEL_IDX, SEL_ID, c

    if SANDBOXED:
        print(f"{c.LIGHT_RED}Fancy App Selector is Sandboxed. To open it run 'fancy' in 'system'!{c.DARK_GRAY} Exiting to default app...{c.RESET}")
        return None, "fancy", None, None  # No 2 can be anything, because when sandboxed it will always go to 'system'

    apps = []
    for k,v in MODULES.items():
        hidden = v.get_about()["hidden"]
        if k=="system": hidden = False
        if not hidden:
            apps.append({"name":v.get_about()["name"],"id":k})
    print_str = ""
    idx = 0
    for i in apps:
        name = i["name"]
        if idx == SEL_IDX:
            name = f"{c.YELLOW}> "+c.LIGHT_WHITE+name+f"{c.YELLOW} <"
            SEL_ID = i["id"]
        else:
            name = c.DARK_GRAY + name
        print_str = print_str+"  "+name
        idx += 1

    print(print_str+c.RESET)

    this_about = MODULES[SEL_ID].get_about()
    about_str = str(this_about["desc"])
    ansi = re.compile(r'\x1b\[[0-9;]*m')
    print_len = len(ansi.sub("", print_str))
    for i in range(print_len-len(about_str)-len(this_about)-2-1-2): # ~40 - ~20 < ~20?
        about_str = about_str + " "

    print(f"  {c.LIGHT_GRAY}{about_str}  {c.YELLOW}{this_about["ver"]}{c.RESET}")
    #action = input(f"{c.RESET}FancyAppSelector : {c.RESET}")

    action = readchar.readkey()

    const.clr()

    # Control Scheme
    # WASD / IJKL / 8456 (Numpad)
    # Quit: Q / U / 7 (Numpad)

    if key_pressed("left", action):
        # Left
        SEL_IDX -= 1
        SEL_IDX = clamp(SEL_IDX, 0, len(apps)-1)
    elif key_pressed("right", action):
        # Right
        SEL_IDX += 1
        SEL_IDX = clamp(SEL_IDX, 0, len(apps)-1)
    elif key_pressed("run", action):
        # Run Normally
        print(f"{c.LIGHT_GRAY}Running {apps[SEL_IDX]['name']}.{c.RESET}")
        return None, SEL_ID, None, None
    elif key_pressed("s_run", action):
        # Run Sandboxed
        print(f"{c.LIGHT_GRAY}Running {apps[SEL_IDX]['name']} sandboxed.{c.RESET}")
        return None, SEL_ID, None, True
    elif key_pressed("quit", action):
        # Quit
        return True, None, None, None
    else:
        print(f"{c.GREEN}Control Schemes :{c.RESET}")
        print(f"{c.LIGHT_GREEN}Left / Right  : A;D / J;L / 4;6 (Numpad) / Left;Right (Arrows){c.RESET}")
        print(f"{c.LIGHT_GREEN}Quit          : Q   / U   / 7   (Numpad) / PageUp     (Arrows){c.RESET}")
        print(f"{c.LIGHT_GREEN}Run           : S   / K   / 5   (Numpad) / Down       (Arrows){c.RESET}")
        print(f"{c.LIGHT_GREEN}Run Sandboxed : W   / I   / 8   (Numpad) / Up         (Arrows){c.RESET}")

    return None, None, None, None
