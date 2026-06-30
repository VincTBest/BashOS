import apps.fancylib as fl
import time
import main
import datetime
import readchar
import platform
import getpass
import psutil
import os
import shutil
import pyperclip
import re

copydata = ""

system = f"{platform.system()} {platform.release()}"
python = platform.python_version()
machine = platform.machine()
user = getpass.getuser()
hostname = platform.node()
pid = os.getpid()
cores = psutil.cpu_count()

self_about = {"name": "FancyStats", "desc": "See system info and statistics.", "ver": "2.0", "hidden": False,
    "author" : "VincTBest",
    "upgrade_url": "https://raw.githubusercontent.com/VincTBest/BashOS/master/apps/stats.py",}
app = fl.FancyApp(self_about)
app.add_action("copy", ["c"])

ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def strip_ansi(text):
    return ANSI_ESCAPE.sub("", text)

def usage_color(percent):
    if percent < 50:
        return app.c.cols["GREEN"]
    elif percent < 80:
        return app.c.cols["YELLOW"]
    return app.c.cols["RED"]

def get_about():
    return app.about

def create_label(label, data):
    global copydata
    string = f"{label:<12}: {app.c.ACCENT}{data}"
    copydata = copydata + "\n" + string
    app.printc(string)

def create_progress_bar(label, current, maximum=None):
    length = 10
    if maximum is not None:
        percent = current / maximum
    else:
        percent = current / 100

    chars = round(percent * length)

    bar = "#" * chars + "." * (length - chars)
    #label = label + " " * (10-len(label))
    create_label(f"{label}",f"{usage_color(percent*100)}[{bar}]{app.c.ACCENT} {percent*100:.1f}%")

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    global copydata
    while True:
        copydata = ""
        app.printc("Stats:", app.c.ACCENT)

        create_label(f"{app.c.BRIGHT}BashOS", "")

        apps = str(len(MODULES))
        if SANDBOXED: apps = "Sandboxed; can't display."
        create_label(f"Apps", apps)

        commands = str(len(COMMANDS))
        if SANDBOXED: commands = "Sandboxed; can't display."
        create_label(f"Commands", commands)

        uptime = datetime.timedelta(seconds=time.time()-main.START_TIME)
        create_label(f"Uptime", str(uptime))

        create_label(f"\n{app.c.BRIGHT}System", "")

        create_label(f"OS", system)
        create_label(f"Python", python)
        create_label(f"Machine", machine)
        create_label(f"User", user)
        create_label(f"Hostname", hostname)
        create_label(f"CWD", os.getcwd())
        create_label(f"PID", pid)

        create_label(f"\n{app.c.BRIGHT}Performance", "")
        create_label(f"Cores", cores)
        create_progress_bar(f"CPU Usage", psutil.cpu_percent())
        create_progress_bar(f"Memory", psutil.virtual_memory().percent)

        disk = shutil.disk_usage("/")
        create_progress_bar("Disk", disk.used // 1024 ** 3, disk.total // 1024 ** 3)

        action = readchar.readkey()
        if app.get_action(action, "quit"):
            return None, app.DEF_APP, None, None
        elif app.get_action(action, "copy"):
            app.printc("If you are on Linux be sure to have xclip or xsel installed or else you will get an error. Continue? (y/n) ")
            key = fl.read_input()
            if key.lower() == "y":
                pyperclip.copy(strip_ansi(copydata))
                copydata = ""
        app.clr()
