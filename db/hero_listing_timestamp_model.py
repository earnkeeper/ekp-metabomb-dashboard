from typing import TypedDict

from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from typing_extensions import NotRequired


class HeroListingTimestampModel(TypedDict):
    tokenId: str
    lastListingTimestamp: int
    blockNumber: int