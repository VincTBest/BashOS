import apps.fancylib as flib

about = {
    "name"   : "Pack-Man",
    "desc"   : "A package manager for BashOS.",
    "ver"    : "0.0.0",
    "hidden" : False
}

app = flib.FancyApp(about)

def has_func(obj, name):
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        return False

def get_about():
    return app.get_about()

def run(MODULES: dict, _STORE: dict, SANDBOXED: bool, COMMAND: dict):
    if SANDBOXED:
        app.printc("Pack-Man needs to be unsandboxed to work!", app.c.ERROR)
        return None, app.DEF_APP, None, None

    apps = flib.get_apps(MODULES, True)
    commands = flib.get_commands(COMMAND)
    before_spacing = "  "

    app.printc("Apps:", app.c.ACCENT)
    for k,v in apps:
        app_about = v.get_about()
        app_name = app_about["name"]
        app_ver = app_about["ver"]
        app.printc(f"{before_spacing}{app_name}: {app.c.MID}{app_ver}", app.c.DARK)

    app.printc("Commands:", app.c.ACCENT)
    for k,v in commands:
        command_ver = "?"
        if has_func(v, "ver"):
            command_ver = v.ver()
        app.printc(f"{before_spacing}{k}: {app.c.MID}{command_ver}", app.c.DARK)

    app.printc("Pack-Man", app.c.ACCENT)
    key = flib.read_input("input")
    if flib.is_indirect_match(key, app.command_exit):
        return None, app.DEF_APP, None, None

    app.clr()
    return None, None, None, None
