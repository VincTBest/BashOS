import importlib
from importlib.machinery import SourceFileLoader
import importlib.util
import apps.fancylib as flib
import urllib.request
import os
import shutil

about = {
    "name"   : "Pack-Man",
    "desc"   : "A package manager for BashOS.",
    "ver"    : "0.0.0",
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

def check_for_update(app_name, url, MODULES):
    if url is not None:
        upgrade_url = url
        response = urllib.request.urlretrieve(upgrade_url)
        path = response[0]

        loader = SourceFileLoader("updated_app", path)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        updated = importlib.util.module_from_spec(spec)
        loader.exec_module(updated)

        new_ver = updated.get_about()["ver"]
        old_ver = MODULES[app_name].get_about()["ver"]
        return new_ver!=old_ver, path, new_ver, old_ver
    return False, "", "", ""

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
            upgrade_url = MODULES[s_action[1]].get_about()["upgrade_url"]
            response = urllib.request.urlretrieve(upgrade_url)
            path = response[0]

            loader = SourceFileLoader("updated_app", path)
            spec = importlib.util.spec_from_loader(loader.name, loader)
            updated = importlib.util.module_from_spec(spec)
            loader.exec_module(updated)

            new_ver = updated.get_about()["ver"]
            old_ver = MODULES[s_action[1]].get_about()["ver"]
            clear = False
            app.clr()
            if new_ver != old_ver:
                new_path = os.getcwd()+"/apps/"+s_action[1]+".py"
                shutil.copyfile(path, new_path)
                app.printc("App was upgraded! Relaunch BashOS for the changes to take affect.", app.c.cols["GREEN"])
                #os.remove(path)
            else:
                app.printc("Already on the latest version.", app.c.ERROR)
            os.remove(path)

        elif s_action[0] == "install":
            upgrade_url = s_action[1]
            response = urllib.request.urlretrieve(upgrade_url)
            path = response[0]

            new_path = os.getcwd()+"/apps/"+s_action[1].split("/")[-1]
            shutil.copyfile(path, new_path)
            clear = False
            app.clr()
            app.printc("App was installed! Relaunch BashOS for the changes to take affect.", app.c.cols["GREEN"])
            #os.remove(path)

        elif s_action[0] == "remove":
            if input("Are you sure? (y/n) ").lower() == "y":
                os.remove(os.getcwd()+"/apps/"+s_action[1]+".py")

        elif s_action[0] == "check_for_update":
            has_update, path, _, _ = check_for_update(s_action[1], MODULES[s_action[1]].get_about()["upgrade_url"], MODULES)
            if has_update:
                app.clr()
                clear = False
                print("There is an update available!")

        elif s_action[0] == "check_for_updates":
            app.clr()
            for k,v in MODULES.items():
                has_update, path, _, _ = check_for_update(k, MODULES[k].get_about()["upgrade_url"], MODULES)
                if has_update:
                    clear = False
                    print(f"There is an update available for {k}!")

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
