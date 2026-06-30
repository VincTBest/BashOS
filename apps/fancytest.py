import apps.fancylib as fl

def dbp(idx: int, mode: str):
    print(mode.capitalize()+": "+str(idx))

self_about = {
    "name": "Fancy Example", "desc": "An Example App, but with FancyLib.", "ver": "1.0.0", "hidden": False,
    "author" : "Your Name",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/fancy_ex.py",
}
app = fl.FancyApp(self_about)
app.make_button(0, "This is a Button!", dbp)
app.make_button(1, "Another Button!", dbp)
app.make_checkbox(2, "Check me", True)
app.make_slider(3,  1, 10, 1)

LTex = fl.LTex()

def get_about():
    return app.about

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    app.clr()

    app.title("Title")
    app.subtitle("Subtitle")
    app.separator()
    app.display(0)
    app.separator()
    app.display(1)
    app.display(2)
    app.display(3)
    app.separator()

    box = LTex.box(4, 190, 16, False)
    for i in box:
        print(i)

    key = fl.read_input()
    app.process_nav(key)

    return None, None, None, None
