# BashOS

### A basic CLI with easy App and Command creation.

## Features:
- Apps, Commands and Monitors.
- Built-in app-maker library.

## Made with:
- Python
    - Package 'readchar'
    - Package 'requests'
    - Package 'urllib'
    - ANSI colors from https://github.com/rene-d

## How to run:
Simply run ```run.bash``` (```bash run.bash```).

###### Or

Open a console on the root directory and run ```source .venv/bin/activate``` to active venv (you should see a .venv behind your username), run ```python main.py``` to run the main file.

### Quick Guide:

After running it you will see a bunch of info messages and you will be thrown into FancyAppSelector. Use A; D/J; L/4; 6/Left; Right to navigate it. You can press S/K/5/Down to run the selected app, or W/I/8/Up to run it sandboxed (The app can't read or write the global store, won't know what other apps and commands exist, and won't be able to set what app to quit to, as it will always be the default app, which by default is FancyAppSelector.) and you can also press Q/U/7/PageUp to quit. If you forget any of these, just press any other button and the control scheme will be printed.

## How to make an app:
Making an app is very straight-forwards and easy. First, make a new python file in the ```apps``` folder. You can name it anything you want.
This is an example app.
```python
import const

def get_about():
    return {"name": "Example", "desc": "An Example App.", "ver": "1.0.0", "hidden": False,
    "author" : "Your Name",
    "upgrade_url": "https://github.com/VincTBest/BashOS/apps/ex.py",} # The URL to your app. (for upgrades, set it to None if you don't have one.)

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    print("Hello!") # Print a message
    return None, const.DEFAULT_APP, None, None
    # Open the default app (return stop_running: Bool; new_module_name: String (Always const.DEFAULT_APP when sandboxed); new_store: Dict; run_sandboxed: Bool)
```
You can modify this to make your first app.
If you want another example, check out system.py.

### The FancyLib library:
This is the same program, but made with FancyLib. Most of FancyLib isn't used, because this is a very simple app.
```python
import apps.fancylib as fl

self_about = {
    "name": "Fancy Example", "desc": "An Example App, but with FancyLib.", "ver": "1.0.0", "hidden": False,
    "author" : "Your Name",
    "upgrade_url": "https://github.com/VincTBest/BashOS/apps/fancy_ex.py",
}
app = fl.FancyApp(self_about)

def get_about():
    return app.about

def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    app.printc("Hello!", app.c.ACCENT) # Print a message with the accent color.
    return None, app.DEF_APP, None, None
    # Open the default app (return stop_running: Bool; new_module_name: String (Always const.DEFAULT_APP when sandboxed); new_store: Dict; run_sandboxed: Bool)
```
If you want another example for a FancyLib app, you can check out FancyAppSelector or any app with the 'Fancy' prefix.

### Const.py
Const.py has a few utilities that can come in handy when making an app.
- const.DEFAULT_APP: The default app.
- const.Const(): A class used for storing variables that throw an error when modified.
- const.Colors(): ANSI Color Codes.

#### How to use colors:
```python
import const

c = const.Colors()

print(c.cols["RED"]+"This is red!"+c.cols["RESET"])
print(c.cols["GREEN"]+"This is green!"+c.cols["RESET"])
print(c.cols["BLUE"]+"This is blue!"+c.cols["RESET"])
print(c.cols["RESET"]+"This is white!"+c.cols["RESET"])
print(c.cols["CROSSED"]+"This is crossed out!"+c.cols["RESET"])
```

## Configuring BashOS
Basic configuration settings can be found in config.json such as:
- default_app: The default app
- FancyColors: FancyLib's default colors.
