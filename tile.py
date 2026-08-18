class Tile:
    def __init__(self, kind):
        self.kind = kind
        self.revealed = False

        # Предмет, который можно найти
        self.loot = None

        # Груз, оставшийся после уничтожения корабля
        self.dropped_loot = []

    @property
    def movement_cost(self):
        if self.kind == "asteroid":
            return 2

        return 1