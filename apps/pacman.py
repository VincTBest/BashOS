import const

SELF_STORE = {
    "pacman": {
        "x": 0, # grid x
        "y": 0, # grid y
        "lives": 3,
        "eat": {
            "duration": 12, # seconds, constant
            "time_left": 0,
        }
    },
    "map": {
        "w": 13, # grid width
        "h": 14, # grid heigh
        "walls": [ # 0-air-(small-point) 1-wall 2-ghost-spawn 3-player-spawn 4-cherry-spawn 5-inf-scroll 6-big-point
            1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,6,1,0,0,1,1,1,0,0,1,6,1,
            1,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,1,1,0,1,1,1,1,0,1,
            1,0,0,0,1,2,2,2,1,0,0,0,1,
            1,1,1,0,1,1,1,1,1,0,1,1,1,
            5,0,0,0,0,0,3,0,0,0,0,0,5,
            1,1,0,1,0,0,0,0,0,1,0,1,1,
            1,0,0,0,0,0,1,0,0,0,0,0,1,
            1,0,1,0,1,1,1,1,1,0,1,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,1,0,6,0,1,0,6,0,1,0,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,
        ]
    }
}


TILES = {
    0: ".",
    1: "#",
    2: "G",
    3: " ",
    4: "C",
    5: " ",
    6: "o",
}

DIRS = {
    "u": (0, -1),
    "d": (0, 1),
    "l": (-1, 0),
    "r": (1, 0),
}

def get_about():
    return {"name": "pacman", "desc": "Play the classic game: Pacman!", "ver": "0.0.0", "hidden": False}

def draw():
    w = SELF_STORE["map"]["w"]
    h = SELF_STORE["map"]["h"]
    walls = list(SELF_STORE["map"]["walls"])

    px = SELF_STORE["pacman"]["x"]
    py = SELF_STORE["pacman"]["y"]

    print()

    for y in range(h):
        row = ""
        for x in range(w):
            if x == px and y == py:
                row += "P"
            else:
                row += TILES[walls[y * w + x]]
        print(row)

    print()


def run(MODULES: dict, STORE: dict, SANDBOXED: bool, COMMANDS: dict):
    global SELF_STORE
    return None, const.DEFAULT_APP, None, None
    draw()

    direction = input("Move (u/d/l/r, exit): ")

    if direction == "exit":
        return None, const.DEFAULT_APP, None, None

    if direction in DIRS:
        dx, dy = DIRS[direction]

        x = SELF_STORE["pacman"]["x"]
        y = SELF_STORE["pacman"]["y"]

        nx = x + dx
        ny = y + dy

        w = SELF_STORE["map"]["w"]
        h = SELF_STORE["map"]["h"]

        # Tunnel
        if nx < 0:
            nx = w - 1
        elif nx >= w:
            nx = 0

        if ny < 0:
            ny = h - 1
        elif ny >= h:
            ny = 0

        walls = list(SELF_STORE["map"]["walls"])
        idx = ny * w + nx
        tile = walls[idx]

        # Can't walk into walls or ghost house
        if tile not in (1, 2):
            SELF_STORE["pacman"]["x"] = nx
            SELF_STORE["pacman"]["y"] = ny

            # Eat small dot
            if tile == 0:
                walls[idx] = 3

            # Eat power pellet
            elif tile == 6:
                walls[idx] = 3
                SELF_STORE["pacman"]["eat"]["time_left"] = \
                    SELF_STORE["pacman"]["eat"]["duration"]

            SELF_STORE["map"]["walls"] = tuple(walls)

    return None, None, None, None