from typing import TypedDict, Optional


class BombMarketListingDto(TypedDict):
    '''
    :example
    {
          "id": "508",
          "rarity": 0,
          "skill_1": 2,
          "skill_2": 0,
          "skill_3": 0,
          "skill_4": 0,
          "skill_5": 0,
          "skill_6": 0,
          "display_id": "4",
          "element": 4,
          "for_sale": true,
          "price": 635,
          "__typename": "Artifact"
    }
    '''
    id: str
    rarity: int
    skill_1: int
    skill_2: int
    skill_3: int
    skill_4: int
    skill_5: int
    skill_6: int
    display_id: str
    element: int
    for_sale: bool
    price: float
    __typename: str
