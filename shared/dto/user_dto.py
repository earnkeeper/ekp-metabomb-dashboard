from typing import TypedDict


class UserDto(TypedDict, total=False):
    '''
    :example
    {
        "wallet_address": "0x6cc36cdc0a12f54c7afe99cb8d635135f9c3974f",
        "__typename": "User"
    }
    :example
    {
        "id": "2856",
        "name": "",
        "user_name": "",
        "__typename": "User"
    }
    '''

    id: str
    name: str
    user_name: str
    wallet_address: str
    __typename: str
