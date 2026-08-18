import random

from tile import Tile
from loot import LOOT_TABLE


class Board:

    SIZE = 7

    def __init__(self):

        self.tiles = [
            [
                Tile("empty")
                for _ in range(self.SIZE)
            ]
            for _ in range(self.SIZE)
        ]

        self.generate()

    def generate(self):

        # Базы
        self.tiles[0][0] = Tile(
            "player_base"
        )

        self.tiles[6][6] = Tile(
            "bot_base"
        )

        # Центральный сектор
        self.tiles[3][3] = Tile(
            "center"
        )

        positions = []

        for y in range(self.SIZE):

            for x in range(self.SIZE):

                if (x, y) in {
                    (0, 0),
                    (6, 6),
                    (3, 3),
                }:
                    continue

                positions.append(
                    (x, y)
                )

        random.shuffle(positions)

        types = (
            ["planet"] * 10
            + ["station"] * 4
            + ["asteroid"] * 6
            + ["anomaly"] * 5
            + ["pirate"] * 4
            + ["empty"] * 13
        )

        random.shuffle(types)

        for position, tile_type in zip(
            positions,
            types
        ):

            x, y = position

            tile = Tile(tile_type)

            if tile_type == "planet":
                tile.loot = self.random_loot()

            self.tiles[y][x] = tile

    def random_loot(self):

        r = random.random()

        if r < 0.01:
            return LOOT_TABLE["ancient"]

        if r < 0.10:
            return LOOT_TABLE["artifact"]

        if r < 0.30:
            return LOOT_TABLE["technology"]

        if r < 0.65:
            return LOOT_TABLE["mineral"]

        return LOOT_TABLE["scrap"]

    def get(self, x, y):

        if not self.inside(x, y):
            return None

        return self.tiles[y][x]

    def inside(self, x, y):

        return (
            0 <= x < self.SIZE
            and
            0 <= y < self.SIZE
        )

    def reveal(
        self,
        x,
        y,
        radius=1
    ):

        for yy in range(
            y - radius,
            y + radius + 1
        ):

            for xx in range(
                x - radius,
                x + radius + 1
            ):

                tile = self.get(
                    xx,
                    yy
                )

                if tile:
                    tile.revealed = True