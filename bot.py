from loot import cargo_value
from combat import (
    attack,
    steal,
)


class Bot:

    def __init__(self, game):

        self.game = game

    def take_turn(self):

        bot = self.game.bot

        bot.reset_turn()

        while (
            bot.moves > 0
            and
            not self.game.game_over
        ):

            if self.try_combat():
                continue

            target = self.choose_target()

            if target is None:
                break

            if not self.move_towards(
                target
            ):
                break

    def try_combat(self):

        bot = self.game.bot
        player = self.game.player

        distance = (
            abs(bot.x - player.x)
            +
            abs(bot.y - player.y)
        )

        if distance != 1:
            return False

        if (
            player.cargo_value() >= 3000
            and
            bot.moves > 0
        ):

            return steal(
                self.game,
                bot,
                player
            )

        return attack(
            self.game,
            bot,
            player
        )

    def choose_target(self):

        bot = self.game.bot
        player = self.game.player

        if bot.hp <= 1:

            return (
                6,
                6
            )

        if cargo_value(
            bot.cargo
        ) >= 3500:

            return (
                6,
                6
            )

        distance = (
            abs(player.x - bot.x)
            +
            abs(player.y - bot.y)
        )

        if (
            distance <= 3
            and
            cargo_value(
                player.cargo
            ) >= 1500
        ):

            return (
                player.x,
                player.y
            )

        best = None
        best_score = -999999

        for y in range(7):

            for x in range(7):

                tile = (
                    self.game.board.get(
                        x,
                        y
                    )
                )

                if not tile.revealed:
                    continue

                if tile.kind != "planet":
                    continue

                if tile.loot is None:
                    continue

                distance = (
                    abs(x - bot.x)
                    +
                    abs(y - bot.y)
                )

                score = (
                    tile.loot.value
                    -
                    distance * 300
                )

                if score > best_score:

                    best_score = score
                    best = (
                        x,
                        y
                    )

        if best:
            return best

        return (
            3,
            3
        )

    def move_towards(
        self,
        target
    ):

        bot = self.game.bot

        tx, ty = target

        dx = 0
        dy = 0

        if bot.x < tx:
            dx = 1

        elif bot.x > tx:
            dx = -1

        elif bot.y < ty:
            dy = 1

        elif bot.y > ty:
            dy = -1

        if dx == 0 and dy == 0:
            return False

        nx = bot.x + dx
        ny = bot.y + dy

        tile = self.game.board.get(
            nx,
            ny
        )

        if tile is None:
            return False

        cost = tile.movement_cost

        if not bot.move_available(
            cost
        ):
            return False

        bot.moves -= cost
        bot.fuel -= 1

        bot.x = nx
        bot.y = ny

        self.game.board.reveal(
            bot.x,
            bot.y
        )

        from events import resolve_tile

        resolve_tile(
            self.game,
            bot
        )

        self.game.check_destroyed(
            bot
        )

        if (
            bot.x == 6
            and
            bot.y == 6
            and
            bot.cargo
        ):

            value = cargo_value(
                bot.cargo
            )

            bot.score += value
            bot.cargo.clear()

            self.game.log(
                f"Бот доставил груз: "
                f"+{value}"
            )

        self.game.check_collision()

        return True