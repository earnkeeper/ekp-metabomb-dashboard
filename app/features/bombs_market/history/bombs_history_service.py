from db.bombs_sales_repo import BombsSalesRepo

from shared.mapper_service import MapperService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class BombsHistoryService:
    def __init__(
        self,
        bombs_sales_repo: BombsSalesRepo,
        metabomb_coingecko_service: MetabombCoingeckoService,
        mapper_service: MapperService
    ):
        self.bombs_sales_repo = bombs_sales_repo
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.mapper_service = mapper_service

    async def get_documents(self, currency):
        rate = await self.metabomb_coingecko_service.get_usd_price(currency["id"])

        models = self.bombs_sales_repo.find_all('bomb', 1000)

        documents = []

        for model in models:
            document = self.map_document(model, currency, rate)
            documents.append(document)

        return documents

    def map_document(self, model, currency, rate):
        bomb = model['bomb']['bomb']
        rarity_name = bomb['rarity_name']
        element_name = bomb['element_name'].lower()
        name = f"{rarity_name} Bomb"
        skills = self.get_skills_list(bomb)
        
        return {
            "bnbCost": model["bnbCost"],
            "bnbCostFiat": model["bnbCostUsd"] * rate,
            "buyer": model["buyer"],
            "display_id": bomb['display_id'],
            "fiatSymbol": currency["symbol"],
            "hash": model["hash"],
            "name": name,
            "rarity": rarity_name,
            "element_name": element_name,
            "element_name_capital": element_name.capitalize(),
            "skills": skills,
            "skill_1": {'skill': bomb['skill_1'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_1']]},
            "skill_2": {'skill': bomb['skill_2'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_2']]},
            "skill_3": {'skill': bomb['skill_3'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_3']]},
            "skill_4": {'skill': bomb['skill_4'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_4']]},
            "skill_5": {'skill': bomb['skill_5'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_5']]},
            "skill_6": {'skill': bomb['skill_6'], 'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_6']]},
            "type": model["nftType"],
            "price": model["price"],
            "priceFiat": model["priceUsd"] * rate,
            "seller": model["seller"],
            "updated": model["timestamp"],
            "timestamp": model["timestamp"],
            "tokenId": model["tokenId"],
        }

    def get_skills_list(self, listing):
        skills = []

        for i in range(1, 7):
            if listing[f'skill_{i}']:
                skills.append(self.__SKILL_NUMBER_TO_NAME[listing[f'skill_{i}']])

        return skills

    __SKILL_NUMBER_TO_NAME = {
        1: "1. Diam. Chest +2",
        2: "2. Meta Chest +5",
        3: "3. Dmg Thru Blocks",
        4: "4. Free Bomb +20%",
        5: "5. Mana/Min +0.5",
        6: "6. Walk Thru Blocks",
        7: "7. Walk Thru Bombs",
    }