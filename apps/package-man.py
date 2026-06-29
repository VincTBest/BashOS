import importlib
from importlib.machinery import SourceFileLoader
import importlib.util
import urllib.request
from urllib.parse import urlparse
import os
import shutil
import apps.fancylib as flib

about = {
    "name"   : "Pack-Man",
    "desc"   : "A package manager for BashOS.",
    "ver"    : "1.0.0",
    "hidden" : False,
    "author" : "VincTBest",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/package-man.py",
}

app = flib.FancyApp(about)

def has_func(obj, name):
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        return False

def load_remote_module(url):
    path, _ = urllib.request.urlretrieve(url)

    loader = SourceFileLoader("updated_app", path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)

    return module, path

def check_for_update(app_name, url, MODULES):
    if url is None:
        return False, "", "", ""

    updated, path = load_remote_module(url)

    new_ver = updated.get_about()["ver"]
    old_ver = MODULES[app_name].get_about()["ver"]

    return new_ver != old_ver, path, new_ver, old_ver

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
        app.printc(f"{before_spacing}{app_name}: {app.c.BRIGHT}({k}) {app.c.MID}{app_ver}", app.c.DARK)

    app.printc("Commands:", app.c.ACCENT)
    for k,v in commands:
        command_ver = "?"
        if has_func(v, "ver"):
            command_ver = v.ver()
        app.printc(f"{before_spacing}{k}: {app.c.MID}{command_ver}", app.c.DARK)

    app.printc("Pack-Man", app.c.ACCENT)
    key = flib.read_input("input")
    clear = True
    if flib.is_indirect_match(key, app.command_exit):
        return None, app.DEF_APP, None, None
    else:
        action = key
        s_action = action.split(" ")
        if s_action[0] == "upgrade":
            if len(s_action) < 2:
                return None, None, None, None

            if s_action[1] not in MODULES:
                app.printc("Unknown app.", app.c.ERROR)
                return None, None, None, None

            upgrade_url = MODULES[s_action[1]].get_about().get("upgrade_url")
            if not upgrade_url:
                app.printc("This app cannot be upgraded.", app.c.ERROR)
                return None, None, None, None

            upgrade_url = MODULES[s_action[1]].get_about()["upgrade_url"]
            updated, path = load_remote_module(upgrade_url)

            new_ver = updated.get_about()["ver"]
            old_ver = MODULES[s_action[1]].get_about()["ver"]
            clear = False
            app.clr()
            if new_ver != old_ver:
                new_path = os.path.join(os.getcwd(), "apps", s_action[1] + ".py")
                shutil.copyfile(path, new_path)
                app.printc("App was upgraded! Relaunch BashOS for the changes to take affect.", app.c.cols["GREEN"])
                #os.remove(path)
            else:
                app.printc("Already on the latest version.", app.c.ERROR)
            os.remove(path)

        elif s_action[0] == "install":
            if len(s_action) < 2:
                return None, None, None, None

            upgrade_url = s_action[1]
            response = urllib.request.urlretrieve(upgrade_url)
            path = response[0]

            filename = os.path.basename(urlparse(upgrade_url).path)
            new_path = os.path.join(os.getcwd(), "apps", filename)
            shutil.copyfile(path, new_path)
            clear = False
            app.clr()
            app.printc("App was installed! Relaunch BashOS for the changes to take affect.", app.c.cols["GREEN"])
            os.remove(path)

        elif s_action[0] == "remove":
            if len(s_action) < 2:
                return None, None, None, None

            if input("Are you sure? (y/n) ").lower() == "y":
                os.remove(os.path.join(os.getcwd(), "apps", s_action[1] + ".py"))

        elif s_action[0] == "check_for_update":
            if len(s_action) < 2:
                return None, None, None, None

            has_update, path, _, _ = check_for_update(s_action[1], MODULES[s_action[1]].get_about()["upgrade_url"], MODULES)
            if has_update:
                app.clr()
                clear = False
                print("There is an update available!")
            os.remove(path)

        elif s_action[0] == "check_for_updates":
            app.clr()
            for k,v in MODULES.items():
                has_update, path, _, _ = check_for_update(k, MODULES[k].get_about()["upgrade_url"], MODULES)
                if has_update:
                    clear = False
                    print(f"There is an update available for {k}!")
                os.remove(path)

        elif s_action[0] == "help":
            app.clr()
            app.printc("Help:", app.c.cols["GREEN"])
            app.printc("  upgrade [app-name]", app.c.cols["LIGHT_GREEN"])
            app.printc("  remove [app-name]", app.c.cols["LIGHT_GREEN"])
            app.printc("  install [url-to-file]", app.c.cols["LIGHT_GREEN"])
            app.printc("  check_for_update [app-name]", app.c.cols["LIGHT_GREEN"])
            app.printc("  check_for_updates", app.c.cols["LIGHT_GREEN"])
            print("")
            clear = False

    if clear:
        app.clr()
    return None, None, None, None
