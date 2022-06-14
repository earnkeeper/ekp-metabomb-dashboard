from datetime import datetime


class HeroesSummaryService:
    def get_documents(self, listing_documents, history_documents, currency):
        floor_prices = {
            "Common": None,
            "Epic": None,
            "Legend": None,
            "Rare": None,
        }

        avg_prices = {
            "Common": None,
            "Epic": None,
            "Legend": None,
            "Rare": None,
        }

        display_ids = {
            "Common": None,
            "Epic": None,
            "Legend": None,
            "Rare": None,
        }

        for listing in listing_documents:
            price_fiat = listing["priceFiat"]
            display_id = listing["display_id"]
            avg_price_fiat = listing["avgPriceFiat"]
            name = listing['rarity_name']
            if (not floor_prices[name]) or (price_fiat < floor_prices[name]):
                floor_prices[name] = price_fiat
                display_ids[name] = display_id
            if (not avg_prices[name]) and avg_price_fiat:
                avg_prices[name] = avg_price_fiat

        return [
            {
                "id": "0",
                "updated": datetime.now().timestamp(),
                "common": {
                    "name": "Common",
                    "display_id": display_ids["Common"],
                    "floorPrice": floor_prices["Common"],
                    "avgPrice": avg_prices["Common"],
                    "fiatSymbol": currency["symbol"]
                },
                "epic": {
                    "name": "Epic",
                    "display_id": display_ids["Epic"],
                    "floorPrice": floor_prices["Epic"],
                    "avgPrice": avg_prices["Epic"],
                    "fiatSymbol": currency["symbol"]
                },
                "legend": {
                    "name": "Legend",
                    "display_id": display_ids["Legend"],
                    "floorPrice": floor_prices["Legend"],
                    "avgPrice": avg_prices["Legend"],
                    "fiatSymbol": currency["symbol"]
                },
                "rare": {
                    "name": "Rare",
                    "display_id": display_ids["Rare"],
                    "floorPrice": floor_prices["Rare"],
                    "avgPrice": avg_prices["Rare"],
                    "fiatSymbol": currency["symbol"]
                },
            }
        ]