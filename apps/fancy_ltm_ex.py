import apps.fancylib as fl

self_about = {
    "name": "Fancy LTM Example", "desc": "An Example App, but with FancyLib using LegacyTextMode.", "ver": "1.0.0", "hidden": False,
    "author" : "Your Name",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/fancy_ex.py",
}
ltm = fl.LTMApp(self_about)
ltm.setup(234,51)

def get_about():
    return ltm.app.about

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    ltm.begin()

    box = fl.Drawable(x=0, y=0, w=232, h=49, prefab="box-noclip")
    # Create the background box. The prefab has 2 parts. The type e.g: box, and the property e.g: noclip.

    label = fl.Drawable(text=self_about.get("name", "Noname App"), x=2)
    # Create a label. Prefab defaults to: "label"

    desc = fl.Drawable(text=self_about.get("desc")+" Made by "+self_about.get("author", "Unknown")+".", x=3, y=2)
    # Create a label.

    box2 = fl.Drawable(x=3, y=4, w=32, h=12)
    # FancyLib will try to guess the prefab based on the parameters.

    ltm.add_item(box)
    ltm.add_item(label)
    ltm.add_item(desc)
    ltm.add_item(box2)

    ltm.draw()

    return ltm.end()
