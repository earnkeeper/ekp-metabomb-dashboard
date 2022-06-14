from datetime import datetime
from pprint import pprint


class BoxesSummaryService:
    def get_documents(self, listing_documents, history_documents, currency):
        # pprint(listing_documents)
        floor_prices = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
            "Bomb Box": None
        }

        avg_prices = {
            "Common Box": None,
            "Premium Box": None,
            "Ultra Box": None,
            "Bomb Box": None
        }
        
        for listing in listing_documents:
            price_fiat = listing["priceFiat"]
            avg_price_fiat = listing["avgPriceFiat"]
            name = listing['name']
            if (not floor_prices[name]) or (price_fiat < floor_prices[name]):
                floor_prices[name] = price_fiat
            if (not avg_prices[name]) and avg_price_fiat:
                avg_prices[name] = avg_price_fiat
            
        
        return [
            {
                "id": "0",
                "updated": datetime.now().timestamp(),
                "common": {
                    "name": "Common Box",
                    "floorPrice": floor_prices["Common Box"],
                    "avgPrice": avg_prices["Common Box"],
                    "fiatSymbol": currency["symbol"]
                },
                "premium": {
                    "name": "Premium Box",
                    "floorPrice": floor_prices["Premium Box"],
                    "avgPrice": avg_prices["Premium Box"],
                    "fiatSymbol": currency["symbol"]
                },
                "ultra": {
                    "name": "Ultra Box",
                    "floorPrice": floor_prices["Ultra Box"],
                    "avgPrice": avg_prices["Ultra Box"],
                    "fiatSymbol": currency["symbol"]
                },
                "bomb": {
                    "name": "Bomb Box",
                    "floorPrice": floor_prices["Bomb Box"],
                    "avgPrice": avg_prices["Bomb Box"],
                    "fiatSymbol": currency["symbol"]
                }
            }
        ]
