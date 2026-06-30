import const
import main

def get_about():
    return {"name": "System", "desc": "A basic app launcher.", "ver": "1.0.0", "hidden": True,
        "author": "VincTBest", "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/system.py"
    }

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    if SANDBOXED:
        print("System is sandboxed! Run 'def' or 'run_default' to return to the default app.")
    command = input(f"System > ").split(" ")
    if command[0] == "exit":
        return True, None, None, None
    elif command[0] == "run_default" or command[0] == "def":
        return None, const.DEFAULT_APP, None, None
    elif command[0] == "ver":
        print(get_about()["ver"])
    elif command[0] == "help":
        print("help")
        print("ver")
        print("exit")
        print("run_default")
        print("def")
        print("apps")
        print("commands")
        print("[app_name]")
        print("[app_name] run")
        print("[app_name] run_sandboxed")
        print("[app_name] name")
        print("[app_name] desc")
        print("[app_name] ver")
        print("[app_name] author")
        print("[app_name] upgrade_url")
        print("[app_name] about")
        print("[app_name] about_kv")
    elif command[0] == "apps":
        for k,v in MODULES.items():
            if not v.get_about()["hidden"]:
                print(k)
    elif command[0] == "commands":
        for k,v in COMMANDS.items():
            print(k)
    elif command[0] == "__Escape1":
        const.DEFAULT_APP = "system"
        return None, " ^ do not abuse this ^ ", None, None
        # This works because when a sandboxed app sets the current app, it quits to the default app no matter what.
        # This sets the default app to itself so when setting the current app it essentially relaunches itself.
        # Detecting and stopping this is very easy and is already implemented in main.py.
    elif command[0] == "__Escape2":
        const.DEFAULT_APP = "system"
        main.main()
        const.DEFAULT_APP = "system"
        return None, "what", None, None
        # This sets the default app to itself, then relaunches main.
        # This works because the new main process only ever knew that default app is 'system'.
        # This is also easy to stop and is implemented.
    elif command[0] == "__Escape3":
        const.DEFAULT_APP = "system"
        main.first_default._value = "system"
        return None, "what", None, None
        # A const.Const() will raise an error when any change is made to it, so it is secure.
    else:
        try:
            new_com = COMMANDS[command[0]]
            new_com.run(command)
        except KeyError:
            try:
                new_mod = MODULES[command[0]]
                if len(command) == 1:
                    print("Running app: " + command[0])
                    return None, command[0], None, None
                elif len(command) == 2:
                    if command[1] == "run":
                        print("Running app: " + command[0])
                        return None, command[0], None, None
                    elif command[1] == "run_sandboxed":
                        print("Running app sandboxed: " + command[0])
                        return None, command[0], None, True
                    elif command[1] == "ver":
                        print(new_mod.get_about()["ver"])
                    elif command[1] == "name":
                        print(new_mod.get_about()["name"])
                    elif command[1] == "author":
                        print(new_mod.get_about()["author"])
                    elif command[1] == "upgrade_url":
                        print(new_mod.get_about()["upgrade_url"])
                    elif command[1] == "desc":
                        print(new_mod.get_about()["desc"])
                    elif command[1] == "about_kv":
                        about = new_mod.get_about()
                        print(about)
                    elif command[1] == "about":
                        about = new_mod.get_about()
                        print(f"{about["name"]} by {about["author"]}: {about["desc"]} v{about["ver"]}")
            except:
                print("Command or app was not found.")

    return None, None, None, None
