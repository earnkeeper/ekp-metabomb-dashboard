from typing import TypedDict


class BoxListingTimestampModel(TypedDict):
    tokenId: str
    lastListingTimestamp: int
    blockNumber: int