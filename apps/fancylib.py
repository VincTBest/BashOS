import const
import readchar

def get_about():
    return {"name":"FancyLib","desc":"A library for making Fancy apps.","ver":"1.0","hidden":True}

def run(*unused):
    print("FancyLib is a library. Exiting...")
    return None, const.DEFAULT_APP, None, None

def get_apps(MODULES: dict, get_hidden: bool=False):
    apps = []
    for k,v in MODULES.items():
        about = v.get_about()
        hidden = about["hidden"]
        if get_hidden: hidden = False
        if not hidden:
            apps.append([k,v])
    return apps

def get_commands(COMMANDS: dict):
    commands = []
    for k,v in COMMANDS.items():
        commands.append([k,v])
    return commands

def read_input(input_type: str= "key", prompt: str= "> "):
    """
    Read input in 3 different ways.\n\n
    :arg input_type str = "key"/"char"/"input"
    :arg prompt str
    :returns The read char/key(s)
    """
    if input_type == "input":
        return input(prompt)
    elif input_type == "key":
        return readchar.readkey()
    elif input_type == "char":
        return readchar.readchar()
    return None

def is_indirect_match(string, match_this):
    return str(string).lower() == str(match_this).lower()

def is_direct_match(string, match_this):
    return str(string) == str(match_this)

class FancyApp:
    def __init__(self, about=None):
        # Got from const.py:
        self.DEF_APP = const.DEFAULT_APP
        self.clr = const.clr
        self.CONFIG = const.CONFIG_FILE.value
        # Colors:
        self.c = const.Colors()
        self.c.ACCENT = self.c.cols[str(self.CONFIG["FancyColors"]["accent"]).upper()]
        self.c.DARK   = self.c.cols[str(self.CONFIG["FancyColors"]["dark"]).upper()]
        self.c.MID    = self.c.cols[str(self.CONFIG["FancyColors"]["mid"]).upper()]
        self.c.BRIGHT = self.c.cols[str(self.CONFIG["FancyColors"]["bright"]).upper()]
        self.c.ERROR  = self.c.cols[str(self.CONFIG["FancyColors"]["error"]).upper()]
        # I/O
        self.input_actions = {
            "left" : ["a", "j", "4", "\x1b[D", readchar.key.LEFT],
            "right": ["d", "l", "6", "\x1b[C", readchar.key.RIGHT],
            "quit" : ["q", "u", "7", "\x1b[5~", readchar.key.PAGE_UP],
            "run"  : ["s", "k", "5", "\x1b[B", readchar.key.DOWN],
            "s_run": ["w", "i", "8", "\x1b[A", readchar.key.UP],
        }
        # About
        if about is None:
            about = {"name":"FancyApp","desc":"An app made with FancyLib.","ver":"1.0","hidden":False}
        self.about = about
        # Commands
        self.command_exit = "exit"
        self.command_help = "help"

    def get_about(self):
        return self.about

    def set_actions(self, actions):
        self.input_actions = actions

    def add_action(self, name, keys):
        self.input_actions[name] = keys

    def get_action(self, key, action="quit"):
        return key in self.input_actions[action]

    def read_action(self, action):
        key = readchar.readkey()
        return self.get_action(key, action)

    def printc(self, text, color=None):
        if color is None: color=self.c.cols["RESET"]
        print(color+text+self.c.cols["RESET"])
