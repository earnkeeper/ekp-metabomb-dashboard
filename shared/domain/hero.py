from typing import TypedDict


class Hero(TypedDict):
    id: int
    name: str
    display_id: int
    rarity: int
    rarity_name: str
    level: int
    hero_class: int
    hero_class_name: str
    power: int
    health: int
    speed: int
    stamina: int
    bomb_num: int
    bomb_range: int
