from datetime import datetime

from db.bomb_listing_timestamp_repo import BombListingTimestampRepo
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class BombListingsService:
    def __init__(
            self,
            metabomb_coingecko_service: MetabombCoingeckoService,
            metabomb_api_service: MetabombApiService,
            mapper_service: MapperService,
            bomb_listing_timestamp_repo: BombListingTimestampRepo
    ):
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.metabomb_api_service = metabomb_api_service
        self.mapper_service = mapper_service
        self.bomb_listing_timestamp_repo = bomb_listing_timestamp_repo

    async def get_documents(self, currency, history_documents):

        now = datetime.now().timestamp()

        name_totals = self.get_name_totals(history_documents, now)

        listings = await self.metabomb_api_service.get_market_bombs()

        bomb_listing_timestamps = list(self.bomb_listing_timestamp_repo.collection.find())

        documents = []

        rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        for listing in listings:
            if not listing['for_sale']:
                continue

            document = self.map_document(
                listing, 
                bomb_listing_timestamps,
                currency, 
                rate, 
                now, 
                name_totals
            )
            
            documents.append(document)

        return documents

    def map_document(self, listing, bomb_listing_timestamps, currency, rate, now, name_totals):
        price = listing["price"]

        rarity_name = self.mapper_service.BOMB_RARITY_TO_NAME[listing["rarity"]]
        token_id = int(listing["id"])

        timestamp = list(filter(lambda x: x['tokenId'] == token_id, bomb_listing_timestamps))
        name = f"{rarity_name} Bomb"
        # element = listing['element']


        name_total = None
        if name in name_totals:
            name_total = name_totals[name]

        avg_price_24h = None
        avg_price_fiat_24h = None
        pc_above_avg_price = None
        pc_above_avg_price_fiat = None

        deal = "?"

        if name_total is not None:
            avg_price_24h = name_total["price_total"] / name_total["count"]
            avg_price_fiat_24h = name_total["price_fiat_total"] / \
                                 name_total["count"]
            pc_above_avg_price = (price - avg_price_24h) * 100 / avg_price_24h
            pc_above_avg_price_fiat = (
                                              price * rate - avg_price_fiat_24h) * 100 / avg_price_fiat_24h
            if pc_above_avg_price_fiat < 0:
                deal = "yes"
            if pc_above_avg_price_fiat > 1:
                deal = "no"

        price_fiat = price * rate

        skills = self.get_skills_list(listing)

        return {
            "fiatSymbol": currency["symbol"],
            "id": int(listing["id"]),
            "name": name,
            "avgPrice": avg_price_24h,
            "avgPriceFiat": avg_price_fiat_24h,
            "display_id": listing['display_id'],
            "pcAboveAvg": pc_above_avg_price,
            "pcAboveAvgFiat": pc_above_avg_price_fiat,
            "deal": deal,
            "price": price,
            "priceFiat": price_fiat,
            "tokenId": int(listing["id"]),
            "type": listing["__typename"],
            "updated": now,
            "rarity_name": rarity_name,
            "element_capital": self.mapper_service.BOMB_ELEMENT_TO_NAME[listing["element"]].capitalize(),
            "element": self.mapper_service.BOMB_ELEMENT_TO_NAME[listing["element"]].lower(),
            "last_listing_timestamp": timestamp[0]['lastListingTimestamp'] if timestamp else None,
            "skills": skills,
            "skill_1": {'skill': listing['skill_1'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[listing['skill_1']]},
            "skill_2": {'skill': listing['skill_2'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[listing['skill_2']]},
            "skill_3": {'skill': listing['skill_3'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[listing['skill_3']]},
            "skill_4": {'skill': listing['skill_4'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[listing['skill_4']]},
            "skill_5": {'skill': listing['skill_5'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[listing['skill_5']]},
            "skill_6": {'skill': listing['skill_6'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[listing['skill_6']]},
        }
        
    def get_skills_list(self, listing):
        skills = []
        
        for i in range(1, 7):
            if listing[f'skill_{i}']:
                skills.append(self.__SKILL_NUMBER_TO_NAME[listing[f'skill_{i}']])
            
        return skills
            


    def get_name_totals(self, history_documents, now):
        name_totals = {}

        for document in history_documents:
            timestamp = document["timestamp"]

            if (now - timestamp) > 86400:
                continue

            name = document["name"]

            if name not in name_totals:
                name_totals[name] = {
                    "price_total": 0,
                    "price_fiat_total": 0,
                    "count": 0
                }

            name_totals[name]["price_total"] += document["price"]
            name_totals[name]["price_fiat_total"] += document["priceFiat"]
            name_totals[name]["count"] += 1

        return name_totals

    __SKILL_NUMBER_TO_NAME = {
        1: "1. Diam. Chest +2",
        2: "2. Meta Chest +5",
        3: "3. Dmg Thru Blocks",
        4: "4. Free Bomb +20%",
        5: "5. Mana/Min +0.5",
        6: "6. Walk Thru Blocks",
        7: "7. Walk Thru Bombs",
    }