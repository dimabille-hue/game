import time

from config import GAME_TIME

from board import Board
from ship import Ship
from bot import Bot

from events import resolve_tile

from combat import (
    attack,
    steal,
)

from loot import cargo_value


class Game:

    def __init__(self):
        self.new_game()

    def new_game(self):

        self.board = Board()

        self.player = Ship(
            0,
            0,
            "Игрок"
        )

        self.bot = Ship(
            6,
            6,
            "Бот"
        )

        # Раскрываем стартовые области
        self.board.reveal(
            0,
            0,
            1
        )

        self.board.reveal(
            6,
            6,
            1
        )

        self.bot_ai = Bot(self)

        self.started_at = time.time()

        self.turn = 1

        self.game_over = False

        self.center_found = False

        # Полный журнал партии.
        # Храним максимум 100 последних сообщений.
        self.messages = []

        # 0 означает, что мы находимся внизу журнала.
        # Чем больше число — тем дальше смотрим в историю.
        self.log_scroll = 0

        self.log(
            "Новая партия. Найди добычу и доставь её домой."
        )

    # =========================================================
    # ВРЕМЯ
    # =========================================================

    def time_left(self):

        return max(
            0,
            GAME_TIME
            -
            int(
                time.time()
                -
                self.started_at
            )
        )

    # =========================================================
    # ЖУРНАЛ
    # =========================================================

    def log(
        self,
        message,
        kind="info"
    ):

        self.messages.append(
            (
                message,
                kind
            )
        )

        # Не позволяем журналу бесконечно расти.
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]

        # Новое событие автоматически
        # прокручивает журнал вниз.
        self.log_scroll = 0

    def scroll_log(self, amount):

        # Сколько строк одновременно помещается
        # в области журнала.
        visible_lines = 8

        max_scroll = max(
            0,
            len(self.messages) - visible_lines
        )

        self.log_scroll += amount

        self.log_scroll = max(
            0,
            min(
                self.log_scroll,
                max_scroll
            )
        )

    def log_to_top(self):

        visible_lines = 8

        self.log_scroll = max(
            0,
            len(self.messages) - visible_lines
        )

    def log_to_bottom(self):

        self.log_scroll = 0

    # =========================================================
    # ДВИЖЕНИЕ ИГРОКА
    # =========================================================

    def move_player(
        self,
        dx,
        dy
    ):

        if self.game_over:
            return

        if self.player.moves <= 0:

            self.log(
                "Очки движения закончились.",
                "warning"
            )

            return

        nx = self.player.x + dx
        ny = self.player.y + dy

        tile = self.board.get(
            nx,
            ny
        )

        if tile is None:

            self.log(
                "Нельзя выйти за карту.",
                "warning"
            )

            return

        cost = tile.movement_cost

        if not self.player.move_available(
            cost
        ):

            self.log(
                "Недостаточно топлива или движения.",
                "warning"
            )

            return

        self.player.moves -= cost

        self.player.fuel -= 1

        self.player.x = nx
        self.player.y = ny

        self.board.reveal(
            nx,
            ny,
            1
        )

        resolve_tile(
            self,
            self.player
        )

        self.check_destroyed(
            self.player
        )

        self.check_collision()

        self.check_delivery()

    # =========================================================
    # БОЙ
    # =========================================================

    def player_attack(self):

        attack(
            self,
            self.player,
            self.bot
        )

    def player_steal(self):

        steal(
            self,
            self.player,
            self.bot
        )

    # =========================================================
    # ДОСТАВКА ГРУЗА
    # =========================================================

    def check_delivery(self):

        if (
            self.player.x == 0
            and
            self.player.y == 0
            and
            self.player.cargo
        ):

            value = cargo_value(
                self.player.cargo
            )

            self.player.score += value

            self.player.cargo.clear()

            self.log(
                f"Груз доставлен! +{value}",
                "good"
            )

    # =========================================================
    # СКАНЕР
    # =========================================================

    def scan(self):

        if not self.player.scan_available:

            self.log(
                "Сканер уже использован.",
                "warning"
            )

            return

        self.player.scan_available = False

        self.board.reveal(
            self.player.x,
            self.player.y,
            2
        )

        self.log(
            "Сканер раскрыл область."
        )

    # =========================================================
    # РЕМОНТ
    # =========================================================

    def repair(self):

        tile = self.board.get(
            self.player.x,
            self.player.y
        )

        at_base = (
            self.player.x == 0
            and
            self.player.y == 0
        )

        at_station = (
            tile is not None
            and
            tile.kind == "station"
        )

        if at_base or at_station:

            self.player.repair()

            self.log(
                "Корабль отремонтирован.",
                "good"
            )

        else:

            self.log(
                "Ремонт возможен только "
                "на базе или станции.",
                "warning"
            )

    # =========================================================
    # ЗАВЕРШЕНИЕ ХОДА
    # =========================================================

    def end_turn(self):

        if self.game_over:
            return

        self.bot_ai.take_turn()

        self.turn += 1

        self.player.reset_turn()

        self.check_time()

    # =========================================================
    # СТОЛКНОВЕНИЕ
    # =========================================================

    def check_collision(self):

        if (
            self.player.x == self.bot.x
            and
            self.player.y == self.bot.y
        ):

            self.player.hp -= 1

            self.bot.hp -= 1

            self.log(
                "Столкновение! Оба корабля "
                "получили 1 урон.",
                "danger"
            )

            self.check_destroyed(
                self.player
            )

            self.check_destroyed(
                self.bot
            )

    # =========================================================
    # УНИЧТОЖЕНИЕ КОРАБЛЯ
    # =========================================================

    def check_destroyed(
        self,
        ship
    ):

        if ship.hp > 0:
            return

        tile = self.board.get(
            ship.x,
            ship.y
        )

        if tile is not None:

            tile.dropped_loot.extend(
                ship.cargo
            )

        ship.cargo.clear()

        if ship.name == "Игрок":

            ship.x = 0
            ship.y = 0

        else:

            ship.x = 6
            ship.y = 6

        ship.hp = 3

        ship.shield = 1

        ship.fuel = 10

        ship.moves = 0

        self.log(
            f"{ship.name} уничтожен. "
            f"Груз потерян.",
            "danger"
        )

    # =========================================================
    # ТАЙМЕР
    # =========================================================

    def check_time(self):

        if self.time_left() <= 0:

            self.game_over = True

            self.log(
                "Время вышло!",
                "danger"
            )

    # =========================================================
    # ФИНАЛЬНЫЙ СЧЁТ
    # =========================================================

    def final_scores(self):

        player_score = self.player.score

        bot_score = self.bot.score

        if (
            self.player.x == 0
            and
            self.player.y == 0
        ):

            player_score += cargo_value(
                self.player.cargo
            )

        if (
            self.bot.x == 6
            and
            self.bot.y == 6
        ):

            bot_score += cargo_value(
                self.bot.cargo
            )

        return (
            player_score,
            bot_score
        )