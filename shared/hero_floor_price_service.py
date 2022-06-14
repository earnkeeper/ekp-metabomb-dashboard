from pprint import pprint
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService


class HeroFloorPriceService:
    def __init__(
            self,
            metabomb_api_service: MetabombApiService,
            mapper_service: MapperService
    ):
        self.metabomb_api_service = metabomb_api_service
        self.mapper_service = mapper_service

    async def get_floor_prices(self):
        listings = await self.metabomb_api_service.get_market_heroes()

        floor_prices = {
            "Common": None,
            "Rare": None,
            "Epic": None,
            "Legend": None,
            "Mythic": None,
            "Meta": None,
        }

        for listing in listings:
            price = listing["price"]

            if not listing["for_sale"]:
                continue

            rarity_name = self.mapper_service.HERO_RARITY_TO_NAME[listing['rarity']]

            if (not floor_prices[rarity_name]) or (price < floor_prices[rarity_name]):
                floor_prices[rarity_name] = price

        return floor_prices

    async def get_floor_price_by_rarity_power(self, rarity, power):
        listings = await self.metabomb_api_service.get_market_heroes()

        for listing in listings:
            if listing["hero_class"] == 0:
                listing["power"] += 1

        floor_price = None

        spec_listings = list(
            filter(lambda x: x['power'] == power and x['rarity'] == rarity and x['for_sale'], listings))

        if spec_listings:
            floor_price = min(spec_listing["price"] for spec_listing in spec_listings)

        return floor_price
