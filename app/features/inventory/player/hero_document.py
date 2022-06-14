from typing import TypedDict


class HeroInventoryDocument(TypedDict):
    id: str
    updated: int
    name: str
    display_id: str
    price: float
    price_fiat: float
    fiat_symbol: str
    rarity_name: str
    level: int
    hero_class: str
    