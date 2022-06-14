from app.features.dashboard.documents.fusion_cost_document import FusionCostDocument
from shared.hero_floor_price_service import HeroFloorPriceService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class DashboardFusionService:
    def __init__(
        self,
        hero_floor_price_service: HeroFloorPriceService,
        metabomb_coingecko_service: MetabombCoingeckoService
    ):
        self.hero_floor_price_service = hero_floor_price_service
        self.metabomb_coingecko_service = metabomb_coingecko_service

    async def get_documents(self, currency):
        hero_floor_prices = await self.hero_floor_price_service.get_floor_prices()

        rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        documents = []

        last_total_cost = None

        for target_name in self.TARGETS.keys():

            target = self.TARGETS[target_name]

            inputs_count = target["count_level_1"]

            inputs_required_level = target["required_level"]

            fusion_fees = target["fusion_fees"]

            input_hero_rarity = target["input_hero_rarity"]

            input_cost = hero_floor_prices[input_hero_rarity]

            if not input_cost or (last_total_cost and input_cost > last_total_cost):
                input_cost = last_total_cost

            inputs_cost = input_cost * inputs_count

            market_value = hero_floor_prices[target_name]
            market_value_fiat = None
            if market_value:
                market_value_fiat = market_value * rate

            total_cost = inputs_cost + fusion_fees
            last_total_cost = total_cost
            total_cost_fiat = total_cost * rate

            color = target["color"]

            document: FusionCostDocument = {
                "color": color,
                "total_cost_color": "normal" if not market_value_fiat else "success" if total_cost_fiat < market_value_fiat else "danger",
                "market_value_color": "normal" if not market_value_fiat else "success" if total_cost_fiat > market_value_fiat else "danger",
                "fiat_symbol": currency["symbol"],
                "fusion_fees_fiat": fusion_fees * rate,
                "fusion_fees_mtb": fusion_fees,
                "input_floor_price_fiat": input_cost * rate,
                "input_floor_price_mtb": input_cost,
                "inputs_cost_fiat": inputs_cost * rate,
                "inputs_cost_mtb": inputs_cost,
                "inputs_count": inputs_count,
                "inputs_required_level": inputs_required_level,
                "market_value_fiat": market_value_fiat,
                "market_value_mtb": market_value,
                "target_name": target_name,
                "total_cost_fiat": total_cost_fiat,
                "input_hero_rarity": input_hero_rarity,
                "total_cost_mtb": total_cost
            }

            documents.append(document)

        return documents

    TARGETS = {
        "Rare": {
            "color": "",
            "count_level_1": 4,
            "required_level": 2,
            "input_hero_rarity": "Common",
            "fusion_fees": 600
        },
        "Epic": {
            "color": "",
            "count_level_1": 6,
            "required_level": 3,
            "input_hero_rarity": "Rare",
            "fusion_fees": 3000
        },
        "Legend": {
            "color": "",
            "count_level_1": 8,
            "required_level": 4,
            "input_hero_rarity": "Epic",
            "fusion_fees": 14000
        },
        "Mythic": {
            "color": "",
            "count_level_1": 10,
            "required_level": 5,
            "input_hero_rarity": "Legend",
            "fusion_fees": 54000
        },
        "Meta": {
            "color": "",
            "count_level_1": 12,
            "required_level": 6,
            "input_hero_rarity": "Mythic",
            "fusion_fees": 220000
        },
    }


