import math

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE
from ui.geometry import tile_center, tile_rect
from ui.primitives import DrawPrimitives
from ui.theme import (
    BOARD_X,
    BOARD_Y,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    DUST,
    NEBULAE,
    PALETTE,
    STARS,
    TILE_COLORS,
)


class SpaceRenderer:
    """Renders the game as a layered animated sci-fi cockpit UI."""

    def __init__(self, screen, fonts):
        self.screen = screen
        self.ui = DrawPrimitives(screen, fonts)

    def render(self, game, now, selected_tile=None, action_menu=None):
        self.draw_background(now)
        self.draw_header(game, now)
        self.draw_board(game, now, selected_tile)
        self.draw_sidebar(game)
        self.draw_log(game)
        self.draw_action_menu(action_menu)
        self.draw_game_over(game)

    def draw_background(self, now):
        self.screen.fill(PALETTE["bg"])
        for center, radius, color in NEBULAE:
            nebula = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            for i in range(9, 0, -1):
                pygame.draw.circle(
                    nebula,
                    (color[0], color[1], color[2], color[3] // i),
                    (radius, radius),
                    radius * i // 9,
                )
            self.screen.blit(
                nebula,
                (center[0] - radius, center[1] - radius),
                special_flags=pygame.BLEND_ADD,
            )

        for x, y, size, phase in STARS:
            twinkle = 0.45 + 0.55 * math.sin(now * 1.8 + phase * 6.28)
            shade = int(110 + 110 * twinkle)
            pygame.draw.circle(self.screen, (shade, shade + 10, 255), (x, y), size)

        for i in range(0, SCREEN_WIDTH, 90):
            pygame.draw.line(self.screen, (12, 24, 47), (i, 0), (i + 130, SCREEN_HEIGHT), 1)

    def draw_planet(self, cx, cy, now):
        self.ui.glow((cx, cy), (43, 205, 190), 43, 58)
        pygame.draw.circle(self.screen, (55, 185, 170), (cx, cy), 20)
        pygame.draw.circle(self.screen, (27, 105, 118), (cx - 7, cy - 6), 8)
        pygame.draw.circle(self.screen, (93, 220, 196), (cx + 8, cy + 6), 5)
        pygame.draw.arc(self.screen, (202, 252, 242), (cx - 32, cy - 10, 64, 22), 0.15 + now % 0.4, 3.0, 3)

    def draw_station(self, cx, cy, now):
        self.ui.glow((cx, cy), PALETTE["cyan"], 35, 50)
        pygame.draw.circle(self.screen, (92, 115, 178), (cx, cy), 17, 3)
        pygame.draw.rect(self.screen, (146, 171, 233), (cx - 14, cy - 14, 28, 28), 2, border_radius=5)
        pygame.draw.line(self.screen, PALETTE["white"], (cx - 29, cy), (cx + 29, cy), 3)
        pygame.draw.line(self.screen, PALETTE["white"], (cx, cy - 29), (cx, cy + 29), 3)
        pygame.draw.circle(self.screen, PALETTE["cyan"], (cx, cy), 5 + int(math.sin(now * 5) > 0))

    def draw_asteroid(self, cx, cy):
        points = [(cx - 22, cy - 5), (cx - 12, cy - 21), (cx + 8, cy - 18), (cx + 22, cy), (cx + 9, cy + 20), (cx - 16, cy + 15)]
        pygame.draw.polygon(self.screen, (153, 122, 88), points)
        pygame.draw.polygon(self.screen, (91, 74, 63), points, 2)
        pygame.draw.circle(self.screen, (94, 76, 62), (cx - 5, cy - 4), 4)
        pygame.draw.circle(self.screen, (185, 150, 105), (cx + 7, cy + 6), 3)

    def draw_anomaly(self, cx, cy, now):
        pulse = 3 * math.sin(now * 4)
        self.ui.glow((cx, cy), PALETTE["purple"], 46, 62)
        for radius in (14, 23, 31):
            pygame.draw.circle(self.screen, PALETTE["purple"], (cx, cy), int(radius + pulse), 2)
        pygame.draw.circle(self.screen, (235, 165, 255), (cx, cy), 7)

    def draw_pirates(self, cx, cy, now):
        self.ui.glow((cx, cy), PALETTE["red"], 37, 46)
        pygame.draw.circle(self.screen, PALETTE["red"], (cx, cy), 20, 3)
        angle = now * 2
        for offset in (0, math.pi / 2):
            dx = int(math.cos(angle + offset) * 16)
            dy = int(math.sin(angle + offset) * 16)
            pygame.draw.line(self.screen, PALETTE["red"], (cx - dx, cy - dy), (cx + dx, cy + dy), 4)

    def draw_center(self, cx, cy, now):
        self.ui.glow((cx, cy), PALETTE["gold"], 50, 70)
        pygame.draw.circle(self.screen, PALETTE["gold"], (cx, cy), 22, 2)
        for i in range(8):
            angle = now * 1.4 + i * math.tau / 8
            start = (cx + int(math.cos(angle) * 12), cy + int(math.sin(angle) * 12))
            end = (cx + int(math.cos(angle) * 31), cy + int(math.sin(angle) * 31))
            pygame.draw.line(self.screen, PALETTE["gold"], start, end, 2)
        pygame.draw.circle(self.screen, (255, 233, 145), (cx, cy), 7)

    def draw_base(self, cx, cy, color):
        self.ui.glow((cx, cy), color, 37, 45)
        pygame.draw.rect(self.screen, color, (cx - 22, cy - 15, 44, 30), 2, border_radius=6)
        pygame.draw.line(self.screen, color, (cx, cy - 25), (cx, cy + 25), 3)
        pygame.draw.line(self.screen, color, (cx - 16, cy), (cx + 16, cy), 2)
        pygame.draw.circle(self.screen, PALETTE["white"], (cx, cy), 4)

    def draw_tile(self, tile, x, y, now, selected_tile):
        rect = tile_rect(x, y)
        base = (13, 22, 42) if not tile.revealed else TILE_COLORS.get(tile.kind, TILE_COLORS["empty"])
        pygame.draw.rect(self.screen, base, rect, border_radius=12)
        pygame.draw.rect(self.screen, PALETTE["grid"], rect, 1, border_radius=12)

        if selected_tile == (x, y):
            self.ui.glow(rect.center, PALETTE["cyan"], 45, 45)
            pygame.draw.rect(self.screen, PALETTE["cyan"], rect, 3, border_radius=12)

        if not tile.revealed:
            self.ui.centered_text("?", rect.center, "big", PALETTE["muted"])
            return

        cx, cy = tile_center(x, y)
        painters = {
            "planet": lambda: self.draw_planet(cx, cy, now),
            "station": lambda: self.draw_station(cx, cy, now),
            "asteroid": lambda: self.draw_asteroid(cx, cy),
            "anomaly": lambda: self.draw_anomaly(cx, cy, now),
            "pirate": lambda: self.draw_pirates(cx, cy, now),
            "center": lambda: self.draw_center(cx, cy, now),
            "player_base": lambda: self.draw_base(cx, cy, PALETTE["cyan"]),
            "bot_base": lambda: self.draw_base(cx, cy, PALETTE["red"]),
        }
        if tile.kind == "empty":
            pygame.draw.circle(self.screen, (83, 111, 150), (cx, cy), 3)
        else:
            painters.get(tile.kind, lambda: None)()

    def draw_route_hint(self, game):
        px, py = game.player.x, game.player.y
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            tile = game.board.get(px + dx, py + dy)
            if tile is None:
                continue
            rect = tile_rect(px + dx, py + dy)
            color = PALETTE["green"] if game.player.move_available(tile.movement_cost) else PALETTE["red"]
            pygame.draw.rect(self.screen, color, rect.inflate(-14, -14), 1, border_radius=8)

    def draw_ship(self, cx, cy, color, enemy=False, now=0):
        direction = -1 if enemy else 1
        self.ui.glow((cx, cy), color, 32, 70)
        flame = 8 + int(4 * math.sin(now * 12))
        hull = [(cx + direction * 24, cy), (cx - direction * 15, cy - 15), (cx - direction * 7, cy), (cx - direction * 15, cy + 15)]
        wing_top = [(cx - direction * 3, cy - 3), (cx - direction * 19, cy - 23), (cx - direction * 10, cy - 4)]
        wing_bottom = [(cx - direction * 3, cy + 3), (cx - direction * 19, cy + 23), (cx - direction * 10, cy + 4)]
        pygame.draw.polygon(self.screen, (20, 31, 54), wing_top)
        pygame.draw.polygon(self.screen, (20, 31, 54), wing_bottom)
        pygame.draw.polygon(self.screen, color, hull)
        pygame.draw.polygon(self.screen, PALETTE["white"], [(cx + direction * 7, cy - 5), (cx + direction * 14, cy), (cx + direction * 7, cy + 5)])
        pygame.draw.line(self.screen, PALETTE["gold"], (cx - direction * 16, cy), (cx - direction * (16 + flame), cy), 4)

    def draw_board(self, game, now, selected_tile):
        pygame.draw.rect(self.screen, (8, 15, 31), (BOARD_X - 8, BOARD_Y - 8, BOARD_WIDTH + 10, BOARD_HEIGHT + 10), border_radius=18)
        for x, y, phase in DUST:
            alpha = int(40 + 50 * math.sin(now * 2 + phase * 6.28))
            pygame.draw.circle(self.screen, (80, 190, 210, alpha), (x, y), 1)
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                self.draw_tile(game.board.get(x, y), x, y, now, selected_tile)
        self.draw_route_hint(game)
        self.draw_ship(*tile_center(game.player.x, game.player.y), PALETTE["cyan"], now=now)
        self.draw_ship(*tile_center(game.bot.x, game.bot.y), PALETTE["red"], enemy=True, now=now)

    def stat_chip(self, text, x, color):
        rect = pygame.Rect(x, 20, 112, 34)
        pygame.draw.rect(self.screen, (12, 22, 42), rect, border_radius=17)
        pygame.draw.rect(self.screen, color, rect, 1, border_radius=17)
        self.ui.centered_text(text, rect.center, "small", PALETTE["text"])

    def draw_header(self, game, now):
        self.ui.text("ПОСЛЕДНИЙ СЕКТОР", 30, 18, "title", PALETTE["white"])
        pygame.draw.line(self.screen, (37, 215, 255), (30, 58), (295 + int(math.sin(now) * 15), 58), 2)
        seconds = game.time_left()
        self.stat_chip(f"⏱ {seconds // 60:02d}:{seconds % 60:02d}", 322, PALETTE["gold"])
        self.stat_chip(f"HP {game.player.hp}/3", 444, PALETTE["red"])
        self.stat_chip(f"🛡 {game.player.shield}", 566, PALETTE["cyan"])
        self.stat_chip(f"Fuel {game.player.fuel}/10", 688, PALETTE["green"])
        self.stat_chip(f"Score {game.player.score}", 810, PALETTE["purple"])

    def draw_sidebar(self, game):
        panel_rect = pygame.Rect(600, 82, 350, 548)
        self.ui.panel(panel_rect)
        self.ui.text("ГРУЗ", 622, 104, "big")
        if game.player.cargo:
            for i, item in enumerate(game.player.cargo):
                self.ui.text(f"◆ {item.name}: {item.value}", 625, 150 + i * 28, "small", PALETTE["gold"])
        else:
            self.ui.text("Трюм пуст", 625, 150, "small", PALETTE["muted"])
        self.ui.text(f"Слоты: {game.player.cargo_slots()}/3", 625, 254)
        self.ui.text(f"Движение: {game.player.moves}", 625, 286)
        self.ui.text("УПРАВЛЕНИЕ", 622, 342, "big")
        controls = ["ЛКМ — движение", "ПКМ — действия", "WASD / ЦФЫВ", "SPACE — конец хода", "E / У — сканер", "R / К — ремонт", "F / А — атака", "G / П — ограбление", "N / Т — новая игра"]
        for i, text in enumerate(controls):
            self.ui.text(text, 625, 390 + i * 24, "small", PALETTE["muted"])

    def draw_log(self, game):
        log_rect = pygame.Rect(30, 645, 560, 105)
        self.ui.panel(log_rect, 12)
        self.ui.text("ЖУРНАЛ", 43, 653, "big")
        total, visible_lines = len(game.messages), 4
        if total > visible_lines:
            status = "▼ последние" if game.log_scroll == 0 else f"↑ история: {game.log_scroll}"
            self.ui.text(status, 178, 663, "small", PALETTE["muted"])
        end_index = total - game.log_scroll
        for i, (message, kind) in enumerate(game.messages[max(0, end_index - visible_lines):end_index]):
            color = {"danger": PALETTE["red"], "warning": PALETTE["gold"], "good": PALETTE["green"]}.get(kind, (195, 207, 232))
            self.ui.text(message if len(message) <= 65 else message[:62] + "...", 43, 690 + i * 18, "small", color)

    def draw_action_menu(self, action_menu):
        if action_menu is None:
            return
        rect = pygame.Rect(action_menu["x"], action_menu["y"], action_menu["width"], action_menu["height"])
        self.ui.panel(rect, 10, PALETTE["cyan"])
        mouse_pos = pygame.mouse.get_pos()
        for i, (title, _callback) in enumerate(action_menu["actions"]):
            button = pygame.Rect(rect.x + 6, rect.y + 6 + i * 42, rect.width - 12, 36)
            color = (45, 78, 112) if button.collidepoint(mouse_pos) else (22, 37, 61)
            pygame.draw.rect(self.screen, color, button, border_radius=7)
            self.ui.text(title, button.x + 12, button.y + 9, "small", PALETTE["white"])

    def draw_game_over(self, game):
        if not game.game_over:
            return
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))
        player_score, bot_score = game.final_scores()
        if player_score > bot_score:
            result, color = "ПОБЕДА!", PALETTE["green"]
        elif player_score < bot_score:
            result, color = "ПОРАЖЕНИЕ", PALETTE["red"]
        else:
            result, color = "НИЧЬЯ", PALETTE["gold"]
        rect = pygame.Rect((SCREEN_WIDTH - 420) // 2, (SCREEN_HEIGHT - 240) // 2, 420, 240)
        self.ui.panel(rect, 16, color)
        self.ui.centered_text(result, (SCREEN_WIDTH // 2, rect.y + 55), "big", color)
        self.ui.centered_text(f"{player_score} : {bot_score}", (SCREEN_WIDTH // 2, rect.y + 105), "big", PALETTE["white"])
        self.ui.text("Ваш результат", rect.x + 55, rect.y + 145, "small", PALETTE["muted"])
        self.ui.text(str(player_score), rect.x + 55, rect.y + 170, "normal", PALETTE["cyan"])
        self.ui.text("Противник", rect.x + 270, rect.y + 145, "small", PALETTE["muted"])
        self.ui.text(str(bot_score), rect.x + 270, rect.y + 170, "normal", PALETTE["red"])
        self.ui.centered_text("N / Т — новая игра", (SCREEN_WIDTH // 2, rect.y + 211), "small", PALETTE["muted"])
