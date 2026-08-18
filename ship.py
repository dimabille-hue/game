from config import (
    MAX_HP,
    MAX_FUEL,
    MOVE_POINTS,
)

from loot import (
    cargo_slots,
    cargo_value,
)


class Ship:

    def __init__(self, x, y, name):

        self.x = x
        self.y = y

        self.name = name

        # Здоровье
        self.hp = MAX_HP
        self.max_hp = MAX_HP

        # Щит
        self.shield = 1

        # Топливо
        self.fuel = MAX_FUEL

        # Очки движения за ход
        self.moves = MOVE_POINTS

        # Сила атаки
        self.attack = 1

        # Груз
        self.cargo = []

        # Очки
        self.score = 0

        # Сканер можно использовать один раз
        self.scan_available = True

    def reset_turn(self):
        self.moves = MOVE_POINTS

    def cargo_slots(self):
        return cargo_slots(self.cargo)

    def cargo_value(self):
        return cargo_value(self.cargo)

    def move_available(self, cost):

        return (
            self.moves >= cost
            and self.fuel > 0
        )

    def repair(self):

        self.hp = self.max_hp
        self.shield = 1
        self.fuel = MAX_FUEL