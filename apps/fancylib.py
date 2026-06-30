import builtins

import const
import readchar

# ℱ𝒶𝓃𝒸𝓎Lib

def get_about():
    return {"name":"FancyLib","desc":"A library for making Fancy apps.","ver":"2.0a-3","hidden":True,
    "author" : "VincTBest",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/fancylib.py",}

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
        self.clamp = const.clamp
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
            "press": ["e", "o", "9", "______", readchar.key.ENTER]
        }
        # About
        if about is None:
            about = {"name":"FancyApp","desc":"An app made with FancyLib.","ver":"1.0","hidden":False}
        self.about = about
        # Commands
        self.command_exit = "exit"
        self.command_help = "help"
        # UI
        self.button_func = None
        self.button_idx = 0
        self.buttons = {}
        self.checkbox_chars = ["-","X"]

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

    # TODO: Add buttons           DONE
    # TODO: Add checkboxes        DONE
    # TODO: Add sliders           DONE
    # TODO: Add input fields      x
    # TODO: Add horizontal layout x
    # TODO: Add BIOS-like look    x

    def title(self, text):
        self.printc(text, self.c.ACCENT)

    def subtitle(self, text):
        self.printc(text, self.c.BRIGHT)

    def separator(self, length=20):
        self.printc("―"*length, self.c.DARK)

    def _elem_slider(self, idx, mode: str):
        this = self.buttons[idx]
        ex = this["extra"]

        # update value
        if mode == "left":
            ex["value"] -= ex["step"]
        elif mode == "right":
            ex["value"] += ex["step"]

        # clamp value
        ex["value"] = max(ex["low"], min(ex["high"], ex["value"]))

        # build slider bar
        total_steps = int((ex["high"] - ex["low"]) / ex["step"])
        pos = int((ex["value"] - ex["low"]) / ex["step"])

        bar = ["―"] * (total_steps+1)
        if 0 <= pos < total_steps+1:
            bar[pos] = "O"

        this["text"] = "[" + "".join(bar) + f"] {ex['value']}"

    def get_slider(self, idx):
        return int(self.buttons[idx]["extra"]["value"])

    def make_slider(self, idx: int, low=0, high=10, step=1, default_value=None):
        self.make_button(idx, "", self._elem_slider, {"value": low or default_value, "low": low, "high": high, "step": step})
        self.buttons[idx]["text"] = ""
        self._elem_slider(idx, "wake")

    def _elem_checkbox(self, idx, mode):
        this = self.buttons[idx]
        if mode == "press":
            this["extra"]["state"] = not this["extra"]["state"]
            if this["extra"]["state"]:
                this["text"] = this["extra"]["o_text"]+f" [{self.checkbox_chars[1]}]"
            else:
                this["text"] = this["extra"]["o_text"]+f" [{self.checkbox_chars[0]}]"

    def get_checkbox(self, idx):
        return self.buttons[idx]["extra"]["state"]==True

    def make_checkbox(self, identifyer: int, text: str, default_state=False):
        self.make_button(identifyer, "", self._elem_checkbox, {"state": default_state, "o_text": text})
        self.buttons[identifyer]["text"] = text+f" [{self.checkbox_chars[0]}]"
        if default_state: self.buttons[identifyer]["text"] = text+f" [{self.checkbox_chars[1]}]"

    def make_button(self, identifyer: int, text: str, func: object, extra: dict=None):
        self.buttons[identifyer] = {"text": f"[{text}]", "sel": False, "func": func, "extra": extra}

    def display(self, identifyer: int):
        """
        Displays and updates an element.
        :param identifyer: Integer; The identifyer the element was defined as. Only display an element once.
        :return: None
        """
        button = self.buttons[identifyer]
        button["sel"] = identifyer == self.button_idx
        color = self.c.cols["RESET"]
        if not button["sel"]:
            color = self.c.MID
        else:
            self.button_func = button["func"]
        self.printc(f"{button["text"]}", color)

    def process_nav(self, key):
        if self.get_action(key, "s_run"): # Up
            self.button_idx -= 1

        elif self.get_action(key, "run"): # Down
            self.button_idx += 1

        elif self.get_action(key, "left"): # Left
            if self.button_func is not None:
                self.button_func(self.button_idx, "left")

        elif self.get_action(key, "right"): # Right
            if self.button_func is not None:
                self.button_func(self.button_idx, "right")

        elif self.get_action(key, "press"):
            if self.button_func is not None:
                self.button_func(self.button_idx, "press")

        self.button_idx = self.clamp(self.button_idx, 0, len(self.buttons)-1)

class LTex:
    # Box drawing
    BOX = {
        "H": "─",
        "V": "│",
        "TL": "┌",
        "TR": "┐",
        "BL": "└",
        "BR": "┘",
        "L": "├",
        "R": "┤",
        "T": "┬",
        "B": "┴",
        "C": "┼",
    }

    # Double box drawing
    DBOX = {
        "H": "═",
        "V": "║",
        "TL": "╔",
        "TR": "╗",
        "BL": "╚",
        "BR": "╝",
        "L": "╠",
        "R": "╣",
        "T": "╦",
        "B": "╩",
        "C": "╬",
    }

    # Block elements
    BLOCK = {
        "FULL": "█",
        "DARK": "▓",
        "MEDIUM": "▒",
        "LIGHT": "░",
        "UPPER": "▀",
        "LOWER": "▄",
        "SQUARE": "■",
    }

    # Arrows
    ARROW = {
        "UP": "↑",
        "DOWN": "↓",
        "LEFT": "←",
        "RIGHT": "→",
        "TRI_RIGHT": "►",
        "TRI_LEFT": "◄",
        "TRI_UP": "▲",
        "TRI_DOWN": "▼",
    }

    # Geometric
    SHAPE = {
        "CIRCLE": "○",
        "CIRCLE_FILLED": "●",
        "SQUARE": "□",
        "SQUARE_FILLED": "■",
        "DIAMOND": "♦",
        "TRIANGLE": "▲",
    }

    # Card suits
    SUIT = {
        "SPADE": "♠",
        "HEART": "♥",
        "DIAMOND": "♦",
        "CLUB": "♣",
    }

    # Symbols
    SYMBOL = {
        "CHECK": "√",
        "PLUS_MINUS": "±",
        "DEGREE": "°",
        "INFINITY": "∞",
        "APPROX": "≈",
        "LE": "≤",
        "GE": "≥",
        "PI": "π",
        "SIGMA": "Σ",
        "ALPHA": "α",
        "BETA": "β",
    }

    # CP437 classics
    CLASSIC = {
        "SMILE": "☺",
        "SMILE_FILLED": "☻",
        "NOTE": "♪",
        "NOTES": "♫",
        "MALE": "♂",
        "FEMALE": "♀",
    }

    @staticmethod
    def box(x, y, w, h, double=False):
        """
        Returns a list of strings representing a box.

        :param x: left padding (spaces)
        :param y: above padding (empty lines)
        :param w: interior width
        :param h: interior height
        :param double: use double-line borders
        :returns: list
        """
        b = LTex.DBOX if double else LTex.BOX
        pad = " " * x

        lines = []

        for i in range(y):
            lines.append("")

        lines.append(
            pad + b["TL"] + b["H"] * w + b["TR"]
        )

        for _ in range(h):
            lines.append(
                pad + b["V"] + (" " * w) + b["V"]
            )

        lines.append(
            pad + b["BL"] + b["H"] * w + b["BR"]
        )

        return lines

    @staticmethod
    def progress(value, maximum, x, invert=False):
        """
        Returns a progress bar string.

        :param value: current value
        :param maximum: maximum value
        :param x: width of the bar
        :param invert: draw empty-first instead of full-first
        :returns: str
        """
        if maximum <= 0:
            maximum = 1

        value = max(0, min(value, maximum))
        filled = round((value / maximum) * x)

        if invert:
            left = LTex.BLOCK["LIGHT"] * (x - filled)
            right = LTex.BLOCK["FULL"] * filled
            return left + right

        return (
                LTex.BLOCK["FULL"] * filled +
                LTex.BLOCK["LIGHT"] * (x - filled)
        )

class Drawable:
    def __init__(self, x=None, y=None, w=None, h=None, text=None, prefab=None):
        if x is None: x = 0
        if y is None: y = 0
        if w is None: w = 0
        if h is None: h = 0
        if text is None: text = ""
        if prefab is None: prefab = "label"
        self.pos = (x,y)
        self.size = (w, h)
        self.text = text
        self.prefab = prefab
        self.lines = []

    def render_dont_clip(self, ltx: LTex):
        if self.prefab.startswith("label"):
            return [self.text]
        elif self.prefab.startswith("box"):
            return ltx.box(self.pos[0], self.pos[1], self.size[0], self.size[1])
        return None

    def render(self, ltx: LTex):
        renderable = self.render_dont_clip(ltx)

        if self.size == (0, 0):
            self.lines = renderable
        else:
            new_renderable = []
            for line in renderable:
                new_renderable.append(line[:self.size[0]])
            self.lines = new_renderable

        if self.prefab.endswith("noclip"):
            self.lines = self.render_dont_clip(ltx)
            return self.lines
        return self.lines

    def get_lines(self):
        return self.lines

class LTMApp:
    def __init__(self, about: dict):
        self.app = FancyApp(about)
        self.ltx = LTex()
        self.screen = (0, 0)
        self.key = ""
        self.items = []

    def setup(self, screen_w=270, screen_h=60):
        self.screen = (screen_w, screen_h)

    def begin(self):
        self.app.clr()

    def end(self):
        self.key = read_input()

    def add_item(self, item: Drawable):
        self.items.append(item)
        self.items[-1].lines = self.items[-1].render(self.ltx)

    def draw(self):
        width, height = self.screen

        # Create an empty framebuffer
        buffer = [[" " for _ in range(width)] for _ in range(height)]

        # Draw every item (first added = back)
        for item in self.items:
            lines = item.get_lines()
            x0, y0 = item.pos

            for y, line in enumerate(lines):
                sy = y0 + y
                if sy < 0 or sy >= height:
                    continue

                for x, ch in enumerate(line):
                    sx = x0 + x
                    if sx < 0 or sx >= width:
                        continue

                    # Transparent pixels
                    if ch == " ":
                        continue

                    buffer[sy][sx] = ch

        # Display framebuffer
        for row in buffer:
            print("".join(row))
