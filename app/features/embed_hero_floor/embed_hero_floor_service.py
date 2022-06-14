from datetime import datetime


class EmbedHeroesService:
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

        count_heroes = {
            "Common": 0,
            "Epic": 0,
            "Legend": 0,
            "Rare": 0,
        }

        perc_difference = {
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

        colors = {
            "Common": "normal",
            "Epic": "normal",
            "Legend": "normal",
            "Rare": "normal",
        }

        for listing in listing_documents:
            price_fiat = listing["priceFiat"]
            display_id = listing["display_id"]
            avg_price_fiat = listing["avgPriceFiat"]
            name = listing['rarity_name']
            count_heroes[name] += 1
            if (not floor_prices[name]) or (price_fiat < floor_prices[name]):
                floor_prices[name] = price_fiat
                display_ids[name] = display_id
            if (not avg_prices[name]) and avg_price_fiat:
                avg_prices[name] = avg_price_fiat

            perc_difference[name] = None
            if floor_prices[name] and avg_prices[name]:
                perc_difference[name] = (floor_prices[name] - avg_prices[name]) / avg_prices[name] * 100

        def set_color(hero_type):
            if perc_difference[hero_type] and (perc_difference[hero_type] < 0):
                colors[hero_type] = "danger"
            if perc_difference[hero_type] and (perc_difference[hero_type] > 0):
                colors[hero_type] = "success"

        set_color("Common")
        set_color("Epic")
        set_color("Legend")
        set_color("Rare")

        document = {
            "id": "0",
            "updated": datetime.now().timestamp(),
        }

        def set_document_hero(hero_id, hero_type):
            document[hero_id] = {
                "name": hero_type,
                "countBoxes": count_heroes[hero_type],
                "display_id": display_ids[hero_type],
                "percDiff": perc_difference[hero_type],
                "floorPrice": floor_prices[hero_type],
                "avgPrice": avg_prices[hero_type],
                "fiatSymbol": currency["symbol"],
                "color": colors[hero_type],
            }

        set_document_hero("common", "Common")
        set_document_hero("epic", "Epic")
        set_document_hero("legend", "Legend")
        set_document_hero("rare", "Rare")

        return [document]
