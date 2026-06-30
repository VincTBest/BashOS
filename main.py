import os
import importlib
import json
import time
import const

import readchar
import requests
import psutil
import urllib
import pyperclip

START_TIME = time.time()
MODULES = {}
EXT_COMMANDS = {}
RUNNING = True
STORE = {}
SANDBOX_NEXT = False
MONITOR = []
c = const.Colors()

CURRENT_APP = "default"

const.init()

first_default = const.Const(const.DEFAULT_APP)

def save_store():
    global STORE
    print("Saving Store...")
    file = open("store.json", "w")
    new_store = STORE
    new_stored = json.dumps(new_store)
    file.write(new_stored)
    return STORE


def load_store():
    global STORE
    print("Loading Store...")
    try:
        json_load = open("store.json", "r")
        json_loaded = json.load(json_load)
        STORE = json_loaded
        json_load.close()
        print("Store Loaded.")
    except FileNotFoundError:
        print("Creating JSON File.")
        file = open("store.json", "w")
        file.write("{}")
        file.close()
    return STORE


def load_modules():
    global MODULES, MONITOR
    cwd = os.getcwd()
    apps_dir = os.path.join(cwd, "apps")
    apps_files = os.listdir(apps_dir)
    for i in range(len(apps_files)):
        file = apps_files[i]
        if file.endswith(".py"):
            # This is a python file. Import it.
            filename = file.removesuffix(".py")
            module = importlib.import_module("apps."+filename)

            try: has_run = module.__getattribute__("run")
            except AttributeError: has_run = False

            try: has_about = module.__getattribute__("get_about")
            except AttributeError: has_about = False

            try: has_info = module.__getattribute__("get_info")
            except AttributeError: has_info = False

            if has_run and has_about:
                print(f"{c.cols["DARK_GRAY"]}Imported package: "+file+" as "+filename+" into MODULES."+c.cols["RESET"])
                MODULES[filename] = module # Add package to global packages
            else:
                if not has_info:
                    if not has_run: print(f"{c.cols["RED"]}Module {file} does not have a run() function! See an example in ex.py.{c.cols["RESET"]}")
                    if not has_about: print(f"{c.cols["RED"]}Module {file} does not have a get_about() function! See an example in ex.py.{c.cols["RESET"]}")
                    print(f"{c.cols["RED"]}{file} will not be imported.{c.cols["RESET"]}")
                else:
                    print(f"{c.cols["DARK_GRAY"]}Imported monitor: {file}.{c.cols["RESET"]}")
                    a1,a2,a3=module.get_info()
                    MONITOR = [a1,a2,a3]
            # print(module.get_about())
        else:
            print(f"{c.cols["CYAN"]}Not a package: "+file+c.cols["RESET"])


def load_external_commands():
    global EXT_COMMANDS
    cwd = os.getcwd()
    apps_dir = os.path.join(cwd, "commands")
    apps_files = os.listdir(apps_dir)
    for i in range(len(apps_files)):
        file = apps_files[i]
        if file.endswith(".py"):
            # This is a python file. Import it.
            filename = file.removesuffix(".py")
            module = importlib.import_module("commands."+filename)
            print(f"{c.cols["DARK_GRAY"]}Imported external command: "+file+" as "+filename+f" into EXT_COMMANDS.{c.cols["RESET"]}")
            EXT_COMMANDS[filename] = module # Add package to global packages
            # print(module.get_about())
        else:
            print(f"{c.cols["CYAN"]}Not an external command: "+file+f"{c.cols["RESET"]}")


def main():
    global MODULES, EXT_COMMANDS, CURRENT_APP, RUNNING, STORE, SANDBOX_NEXT, first_default, MONITOR, START_TIME
    START_TIME = time.time()
    load_store()

    load_modules()
    load_external_commands()

    default = const.DEFAULT_APP
    while RUNNING:
        if first_default.value != const.DEFAULT_APP:
            print(f"{c.cols["RED"]}Default app was modified by an app. Resetting and exiting to it...{c.cols["RESET"]}")
            CURRENT_APP = first_default.value
            const.DEFAULT_APP = first_default.value

        if CURRENT_APP == "default":
            CURRENT_APP = const.DEFAULT_APP
            print("Launching default app.")
        try:
            module = MODULES[CURRENT_APP]
            giveMODULES = {}
            giveSTORE = {}
            giveCOMMANDS = {}
            sandbox_this = SANDBOX_NEXT
            if not SANDBOX_NEXT:
                giveMODULES = MODULES
                giveSTORE = STORE
                giveCOMMANDS = EXT_COMMANDS

            if len(MONITOR) > 2:
                MONITOR[1](sandbox_this, MODULES, STORE, SANDBOX_NEXT, EXT_COMMANDS)
            stop_running, new_module_name, new_store, run_sandboxed = module.run(giveMODULES, giveSTORE, sandbox_this, giveCOMMANDS)
            if len(MONITOR) > 3:
                MONITOR[2](stop_running, new_module_name, new_store, run_sandboxed, sandbox_this, MODULES, STORE, SANDBOX_NEXT, EXT_COMMANDS)

            if stop_running: RUNNING = False

            if new_module_name:
                if not sandbox_this: # This is to stop a sandboxed app from launching itself without sandbox.
                    CURRENT_APP = new_module_name
                    SANDBOX_NEXT = False
                else:
                    CURRENT_APP = const.DEFAULT_APP
                    SANDBOX_NEXT = False

            if not sandbox_this:
                if new_store: STORE = new_store
                if run_sandboxed: SANDBOX_NEXT = True
        except KeyError as e:
            print("App not found!")
            CURRENT_APP = const.DEFAULT_APP
            #RUNNING = False
        default = const.DEFAULT_APP
    save_store()
    print("Exiting...")


if __name__ == '__main__':
    main()
