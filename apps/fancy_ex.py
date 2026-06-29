import apps.fancylib as fl

self_about = {
    "name": "Fancy Example", "desc": "An Example App, but with FancyLib.", "ver": "1.0.0", "hidden": False,
    "author" : "Your Name",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/fancy_ex.py",
}
app = fl.FancyApp(self_about)

def get_about():
    return app.about

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    app.printc("Hello!", app.c.ACCENT) # Print a message with the accent color.
    return None, app.DEF_APP, None, None
    # Open the default app (return stop_running: Bool; new_module_name: String (Always const.DEFAULT_APP when sandboxed); new_store: Dict; run_sandboxed: Bool)
