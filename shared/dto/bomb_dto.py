from typing import TypedDict


class BombDto(TypedDict):
    '''
    :example
    {
        id
        user_id
        rarity
        skill_1
        skill_2
        skill_3
        skill_4
        skill_5
        skill_6
        display_id
        element
        for_sale
        price
        __typename
    }
    '''
    id: str
    user_id: str
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
