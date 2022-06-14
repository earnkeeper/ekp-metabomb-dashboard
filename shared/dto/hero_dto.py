from typing import Optional, TypedDict


class HeroDto(TypedDict):
    '''
    :example
    {
        "id": "29220",
        "user_id": "2856",
        "name": null,
        "display_id": "7",
        "rarity": 0,
        "level": 0,
        "hero_class": 1,
        "for_sale": false,
        "price": 0,
        "power": 2,
        "health": 2,
        "speed": 3,
        "stamina": 3,
        "bomb_num": 1,
        "bomb_range": 1,
        "user": {
            "id": "2856",
            "name": "",
            "user_name": "",
            "__typename": "User"
        },
        "__typename": "Hero"
    }
    '''
    id: str
    user_id: str
    name: Optional[str]
    display_id: str
    rarity: int
    level: int
    hero_class: int
    for_sale: bool
    price: int
    power: int
    health: int
    speed: int
    stamina: int
    bomb_num: int
    bomb_range: int
    __typename: str
