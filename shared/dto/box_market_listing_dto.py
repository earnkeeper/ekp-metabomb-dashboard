from typing import TypedDict

from shared.dto.user_dto import UserDto


class BoxMarketListingDto(TypedDict):
    '''
    :example
    {
        "id": "2315",
        "token_id": "1792",
        "box_type": 0,
        "price": 6490,
        "for_sale": 1,
        "chain_process": 0,
        "__typename": "Box"
    }
    '''

    id: str
    token_id: str
    user: UserDto
    box_type: int
    price: int
    for_sale: int
    chain_process: int
    __typename: str



