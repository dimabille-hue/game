import pygame

from config import TILE_SIZE, BOARD_SIZE
from ui.theme import BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT


def tile_rect(x, y):
    return pygame.Rect(
        BOARD_X + x * TILE_SIZE + 3,
        BOARD_Y + y * TILE_SIZE + 3,
        TILE_SIZE - 7,
        TILE_SIZE - 7,
    )


def tile_center(x, y):
    return (
        BOARD_X + x * TILE_SIZE + TILE_SIZE // 2,
        BOARD_Y + y * TILE_SIZE + TILE_SIZE // 2,
    )


def mouse_to_tile(position):
    mx, my = position
    if not (BOARD_X <= mx < BOARD_X + BOARD_WIDTH and BOARD_Y <= my < BOARD_Y + BOARD_HEIGHT):
        return None

    x = (mx - BOARD_X) // TILE_SIZE
    y = (my - BOARD_Y) // TILE_SIZE
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        return x, y

    return None
