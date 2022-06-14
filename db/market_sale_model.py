from typing import TypedDict

from shared.domain.bomb import Bomb
from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from typing_extensions import NotRequired


class MarketSaleModel(TypedDict):
    bnbCost: float
    bnbCostUsd: float
    blockNumber: int
    buyer: str
    fees: float
    feesUsd: float
    hash: hash
    hero: NotRequired[Hero]
    box: NotRequired[HeroBox]
    bomb: NotRequired[Bomb]
    nftType: str
    price: float
    priceUsd: float
    seller: str
    timestamp: int
    tokenId: str
