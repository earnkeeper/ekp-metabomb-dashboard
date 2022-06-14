from typing import Optional, TypedDict


class HeroMarketListingDto(TypedDict):
    '''
    :example
    {
        "id": "30",
        "name": null,
        "display_id": "5",
        "rarity": 0,
        "level": 0,
        "hero_class": 1,
        "for_sale": false,
        "price": 0,
        "__typename": "Hero"
    }
    '''

    id: str
    name: Optional[str]
    display_id: str
    rarity: int
    level: int
    hero_class: int
    for_sale: int
    price: int
    __typename: str
