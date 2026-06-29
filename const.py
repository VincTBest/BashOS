import os
import json

# Constant, throws and error when trying to change it.
class Const:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __setattr__(self, name, value):
        if hasattr(self, "_value"):
            raise AttributeError("Immutable value, can't change!")
        super().__setattr__(name, value)

DEFAULT_APP = "fancy"
CONFIG_FILE = None

def init():
    global DEFAULT_APP, CONFIG_FILE
    config_file = open("config.json", "r")
    config_parsed = json.load(config_file)
    CONFIG_FILE = Const(config_parsed)
    DEFAULT_APP = CONFIG_FILE.value["default_app"]

class Colors:
    # Colors from: https://github.com/rene-d
    cols = {
        "BLACK" : "\033[0;30m",
        "RED" : "\033[0;31m",
        "GREEN" : "\033[0;32m",
        "BROWN" : "\033[0;33m",
        "BLUE" : "\033[0;34m",
        "PURPLE" : "\033[0;35m",
        "CYAN" : "\033[0;36m",
        "LIGHT_GRAY" : "\033[0;37m",
        #"DARK_GRAY" : "\033[1;30m",
        "DARK_GRAY" : "\033[1;90m",
        "LIGHT_RED" : "\033[1;31m",
        "LIGHT_GREEN" : "\033[1;32m",
        "YELLOW" : "\033[1;33m",
        "LIGHT_BLUE" : "\033[1;34m",
        "LIGHT_PURPLE" : "\033[1;35m",
        "LIGHT_CYAN" : "\033[1;36m",
        "LIGHT_WHITE" : "\033[1;37m",
        "BOLD" : "\033[1m",
        "FAINT" : "\033[2m",
        "ITALIC" : "\033[3m",
        "UNDERLINE" : "\033[4m",
        "BLINK" : "\033[5m",
        "NEGATIVE" : "\033[7m",
        "CROSSED" : "\033[9m",
        "END" : "\033[0m",
        "RESET" : "\033[1;37m"+"\033[0m", # LIGHT_WHITE + END
    }
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')
