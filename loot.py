from dataclasses import dataclass

MAX_CARGO_SLOTS = 3


@dataclass(frozen=True)
class Loot:
    name: str
    value: int
    slots: int


LOOT_TABLE = {
    "scrap": Loot("Металлолом", 500, 1),
    "mineral": Loot("Минерал", 1500, 1),
    "technology": Loot("Технология", 3000, 1),
    "artifact": Loot("Артефакт", 7000, 2),
    "ancient": Loot("Древний артефакт", 12000, 3),
}


def cargo_slots(cargo):
    return sum(item.slots for item in cargo)


def cargo_value(cargo):
    return sum(item.value for item in cargo)


def can_take(cargo, item):
    return cargo_slots(cargo) + item.slots <= MAX_CARGO_SLOTS