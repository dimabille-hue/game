from config import MAX_FUEL

import random

from loot import (
    LOOT_TABLE,
    can_take,
)


def resolve_tile(game, ship):

    tile = game.board.get(
        ship.x,
        ship.y
    )

    if tile is None:
        return

    if tile.kind == "planet":

        planet(
            game,
            ship,
            tile
        )

    elif tile.kind == "station":

        station(
            game,
            ship
        )

    elif tile.kind == "anomaly":

        anomaly(
            game,
            ship
        )

    elif tile.kind == "pirate":

        pirates(
            game,
            ship
        )

    elif tile.kind == "center":

        center(
            game,
            ship
        )

    # Подбираем груз,
    # оставшийся после уничтожения корабля.
    if tile.dropped_loot:

        remaining = []

        for item in tile.dropped_loot:

            if can_take(
                ship.cargo,
                item
            ):

                ship.cargo.append(
                    item
                )

                game.log(
                    f"{ship.name} забрал: "
                    f"{item.name} "
                    f"({item.value})"
                )

            else:

                remaining.append(
                    item
                )

        tile.dropped_loot = remaining


def planet(game, ship, tile):

    if tile.loot is None:
        return

    if not can_take(
        ship.cargo,
        tile.loot
    ):

        if ship.name == "Игрок":

            game.log(
                "Трюм заполнен.",
                "warning"
            )

        return

    item = tile.loot

    ship.cargo.append(
        item
    )

    tile.loot = None

    game.log(
        f"{ship.name} нашёл "
        f"{item.name} — "
        f"{item.value}"
    )


def station(game, ship):

    ship.repair()

    game.log(
        f"{ship.name}: "
        f"станция восстановила корабль."
    )


def anomaly(game, ship):

    event = random.randint(
        1,
        4
    )

    if event == 1:

        ship.fuel = min(
            MAX_FUEL,
            ship.fuel + 3
        )

        game.log(
            f"{ship.name}: +3 топлива."
        )

    elif event == 2:

        ship.hp -= 1

        game.log(
            f"{ship.name}: "
            f"аномалия нанесла 1 урон.",
            "danger"
        )

    elif event == 3:

        game.board.reveal(
            ship.x,
            ship.y,
            2
        )

        game.log(
            f"{ship.name}: "
            f"сектор просканирован."
        )

    else:

        dx, dy = random.choice(
            [
                (2, 0),
                (-2, 0),
                (0, 2),
                (0, -2),
            ]
        )

        ship.x = max(
            0,
            min(6, ship.x + dx)
        )

        ship.y = max(
            0,
            min(6, ship.y + dy)
        )

        game.board.reveal(
            ship.x,
            ship.y
        )

        game.log(
            f"{ship.name}: "
            f"пространственный скачок."
        )


def pirates(game, ship):

    if random.random() < 0.6:

        reward = random.randint(
            1000,
            3000
        )

        ship.score += reward

        game.log(
            f"{ship.name}: "
            f"победа над пиратами "
            f"+{reward}"
        )

    else:

        ship.hp -= 1

        game.log(
            f"{ship.name}: "
            f"пираты нанесли 1 урон.",
            "danger"
        )


def center(game, ship):

    r = random.random()

    if r < 0.35:

        item = LOOT_TABLE[
            "ancient"
        ]

        if can_take(
            ship.cargo,
            item
        ):

            ship.cargo.append(
                item
            )

            game.log(
                f"{ship.name}: "
                f"ДРЕВНИЙ АРТЕФАКТ!"
            )

    elif r < 0.65:

        ship.fuel = min(
            10,
            ship.fuel + 5
        )

        game.log(
            f"{ship.name}: +5 топлива."
        )

    elif r < 0.85:

        game.board.reveal(
            ship.x,
            ship.y,
            3
        )

        game.log(
            "Центральный сектор "
            "раскрыл карту."
        )

    else:

        ship.hp = 0

        game.log(
            "Центральный сектор "
            "уничтожил корабль!",
            "danger"
        )

    game.center_found = True