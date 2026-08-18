import random

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE

BOARD_X = 34
BOARD_Y = 92
HEX_RADIUS = 38
HEX_X_STEP = 66
HEX_Y_STEP = 58
HEX_ROW_OFFSET = HEX_X_STEP // 2
BOARD_WIDTH = HEX_RADIUS * 2 + HEX_X_STEP * (BOARD_SIZE - 1) + HEX_ROW_OFFSET
BOARD_HEIGHT = HEX_RADIUS * 2 + HEX_Y_STEP * (BOARD_SIZE - 1)

PALETTE = {
    "bg": (4, 7, 18),
    "panel": (10, 16, 31),
    "panel_light": (18, 29, 52),
    "grid": (42, 64, 98),
    "text": (226, 237, 255),
    "muted": (133, 151, 184),
    "cyan": (71, 217, 255),
    "red": (255, 80, 105),
    "green": (83, 230, 155),
    "gold": (255, 203, 80),
    "purple": (183, 113, 255),
    "white": (248, 252, 255),
}

TILE_COLORS = {
    "empty": (18, 30, 52),
    "planet": (20, 70, 78),
    "station": (44, 52, 96),
    "asteroid": (65, 55, 46),
    "anomaly": (58, 35, 88),
    "pirate": (82, 35, 48),
    "center": (90, 67, 25),
    "player_base": (23, 58, 102),
    "bot_base": (73, 37, 58),
}

random.seed(9)
STARS = [
    (
        random.randrange(0, SCREEN_WIDTH),
        random.randrange(0, SCREEN_HEIGHT),
        random.choice((1, 1, 1, 2)),
        random.random(),
    )
    for _ in range(130)
]
NEBULAE = [
    ((190, 165), 210, (40, 80, 170, 28)),
    ((790, 180), 240, (120, 60, 180, 24)),
    ((465, 615), 260, (40, 170, 165, 18)),
]
DUST = [
    (
        random.randrange(BOARD_X, BOARD_X + BOARD_WIDTH),
        random.randrange(BOARD_Y, BOARD_Y + BOARD_HEIGHT),
        random.random(),
    )
    for _ in range(70)
]
