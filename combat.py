import random

from loot import can_take


def adjacent(
    ship_a,
    ship_b
):

    distance = (
        abs(ship_a.x - ship_b.x)
        +
        abs(ship_a.y - ship_b.y)
    )

    return distance == 1


def attack(
    game,
    attacker,
    defender
):

    if game.game_over:
        return False

    if not adjacent(
        attacker,
        defender
    ):

        if attacker.name == "Игрок":

            game.log(
                "Цель должна "
                "находиться рядом.",
                "warning"
            )

        return False

    if attacker.moves <= 0:

        game.log(
            "Нет очков действия.",
            "warning"
        )

        return False

    attacker.moves -= 1

    damage = attacker.attack

    if defender.shield > 0:

        defender.shield = max(
            0,
            defender.shield - damage
        )

        game.log(
            f"{attacker.name} "
            f"пробил щит "
            f"{defender.name}."
        )

    else:

        defender.hp -= damage

        game.log(
            f"{attacker.name} "
            f"атаковал "
            f"{defender.name}: "
            f"-{damage} HP.",
            "danger"
        )

    game.check_destroyed(
        defender
    )

    return True


def steal(
    game,
    attacker,
    defender
):

    if game.game_over:
        return False

    if not adjacent(
        attacker,
        defender
    ):

        game.log(
            "Нужно находиться "
            "рядом с кораблём.",
            "warning"
        )

        return False

    if attacker.moves <= 0:
        return False

    if not defender.cargo:

        game.log(
            f"У {defender.name} "
            f"нет груза."
        )

        return False

    item = random.choice(
        defender.cargo
    )

    if not can_take(
        attacker.cargo,
        item
    ):

        game.log(
            "В твоём трюме "
            "нет места.",
            "warning"
        )

        return False

    attacker.moves -= 1

    defender.cargo.remove(
        item
    )

    attacker.cargo.append(
        item
    )

    game.log(
        f"{attacker.name} "
        f"украл {item.name} "
        f"у {defender.name}!",
        "good"
    )

    return True