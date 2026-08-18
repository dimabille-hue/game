import math
import pygame

from config import BOARD_SIZE
from ui.theme import BOARD_X, BOARD_Y, HEX_RADIUS, HEX_ROW_OFFSET, HEX_X_STEP, HEX_Y_STEP


def hex_points(cx, cy, radius=HEX_RADIUS):
    return [
        (
            cx + int(math.cos(math.radians(60 * index + 30)) * radius),
            cy + int(math.sin(math.radians(60 * index + 30)) * radius),
        )
        for index in range(6)
    ]


def tile_center(x, y):
    return (
        BOARD_X + HEX_RADIUS + x * HEX_X_STEP + (y % 2) * HEX_ROW_OFFSET,
        BOARD_Y + HEX_RADIUS + y * HEX_Y_STEP,
    )


def tile_rect(x, y):
    cx, cy = tile_center(x, y)
    return pygame.Rect(cx - HEX_RADIUS, cy - HEX_RADIUS, HEX_RADIUS * 2, HEX_RADIUS * 2)


def point_in_polygon(point, polygon):
    px, py = point
    inside = False
    previous_x, previous_y = polygon[-1]

    for current_x, current_y in polygon:
        crosses_y = (current_y > py) != (previous_y > py)
        if crosses_y:
            slope_x = (previous_x - current_x) * (py - current_y) / (previous_y - current_y) + current_x
            if px < slope_x:
                inside = not inside
        previous_x, previous_y = current_x, current_y

    return inside


def mouse_to_tile(position):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if point_in_polygon(position, hex_points(*tile_center(x, y))):
                return x, y

    return None
