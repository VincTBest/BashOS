import const

def get_about():
    return {"name": "Example", "desc": "An Example App.", "ver": "1.0.0", "hidden": False}

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    print("Hello!") # Print a message
    return None, const.DEFAULT_APP, None, None
    # Open the default app (return stop_running: Bool; new_module_name: String (Always const.DEFAULT_APP when sandboxed); new_store: Dict; run_sandboxed: Bool)
