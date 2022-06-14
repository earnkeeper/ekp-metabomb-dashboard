from typing import TypedDict


class BombListingTimestampModel(TypedDict):
    tokenId: str
    lastListingTimestamp: int
    blockNumber: int
