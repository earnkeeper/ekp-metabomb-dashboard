from shared.hero_floor_price_service import HeroFloorPriceService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class DashboardHeroProfitService:
    def __init__(
            self,
            metabomb_coingecko_service: MetabombCoingeckoService,
            hero_floor_price_service: HeroFloorPriceService,
    ):
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.hero_floor_price_service = hero_floor_price_service

    async def get_documents(self, currency):

        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        all_documents = []

        for rarity, powers in self.POWERS_OF_RARITIES.items():
            documents = []
            for power in powers:
                document = {}
                document['power'] = power
                mtb_per_day = 0.145 * 0.5 * 1440 * power
                fiat_per_day = mtb_per_day * mtb_rate
                est_payback = None
                floor_price = await self.hero_floor_price_service.get_floor_price_by_rarity_power(rarity, power)
                if floor_price:
                    floor_price = floor_price * mtb_rate
                    est_payback = int(floor_price / fiat_per_day)
                document['market_value'] = floor_price
                document['mtb_per_day'] = int(mtb_per_day)
                document['roi'] = est_payback
                document["fiat_symbol"] = currency["symbol"],
                documents.append(document)

            all_documents.append(documents)

        return all_documents

    POWERS_OF_RARITIES = {
        0: [1, 2, 3, 4],
        1: [4, 5, 6, 7],
        2: [7, 8, 9, 10],
        3: [10, 11, 12, 13]
    }