from main import save_store, load_store
import const

def get_about():
    return {"name": "StoreFinder", "desc": "Read and modify values form the global store.", "ver": "0.1.0", "hidden": False}

def print_dict(printable_dict: dict):
    for key, value in printable_dict.items():
        print(key+": "+value)


def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    new_store = STORE
    sand_str = ""
    if SANDBOXED: sand_str = "SANDBOXED "
    action = input(sand_str+get_about()["name"]+" > ")
    s_action = action.split(" ")
    if s_action[0] == "set":
        can=False
        try: can=s_action[1] and s_action[2]
        except IndexError: pass
        if can:
            new_store[s_action[1]] = s_action[2]
    elif s_action[0] == "get":
        can=False
        try: can=s_action[1]
        except IndexError: pass
        if can:
            value = "Not Found!"
            try: value=new_store[s_action[1]]
            except KeyError: pass
            print(value)
    elif s_action[0] == "exit":
        return None, const.DEFAULT_APP, new_store, None
    elif s_action[0] == "get_whole":
        print(new_store)
    elif s_action[0] == "save_store":
        save_store()
    elif s_action[0] == "load_store":
        new_store = load_store()
    else:
        print("set [key] [value]")
        print("get [key]")
        print("get_whole")
        print("save_store")
        print("load_store")
        print("exit")

    return None, None, new_store, None