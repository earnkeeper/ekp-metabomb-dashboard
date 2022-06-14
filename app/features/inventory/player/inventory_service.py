from ekp_sdk.services import CoingeckoService
from web3 import Web3

from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService

from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService

from datetime import datetime


class InventoryService:
    def __init__(
            self,
            mapper_service: MapperService,
            metabomb_api_service: MetabombApiService,
            metabomb_coingecko_service: MetabombCoingeckoService,
            metabomb_moralis_service=MetabombMoralisService,
    ):
        self.mapper_service = mapper_service
        self.metabomb_api_service = metabomb_api_service
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.metabomb_moralis_service = metabomb_moralis_service

    async def get_hero_documents(self, address, currency):

        hero_list = await self.metabomb_api_service.get_market_heroes(for_sale=2)
        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        hero_map = self.mapper_service.get_hero_map(hero_list)
        hero_price_map = self.mapper_service.get_hero_price_map(hero_list)
        hero_nfts = await self.metabomb_moralis_service.get_heroes_by_address(address)

        documents = []

        for hero_nft in hero_nfts:

            token_id = str(hero_nft["token_id"])

            stats = hero_map[token_id]

            if token_id not in hero_map:
                continue

            hero = hero_map[token_id]
            rarity = hero["rarity"]
            rarity_name = self.mapper_service.HERO_RARITY_TO_NAME[rarity]
            level = hero["level"]
            hero_class = hero["hero_class"]

            price = self.mapper_service.get_hero_price(
                rarity,
                level,
                hero_price_map
            )

            price_fiat = None

            if price:
                price_fiat = price * mtb_rate

            mtb_per_day = 0.145 * 0.5 * 1440 * stats['power']
            fiat_per_day = mtb_per_day * mtb_rate

            est_payback = None
            est_roi = None

            if price_fiat:
                est_payback = f"{int(price_fiat / fiat_per_day)} days"
                est_roi = int(fiat_per_day * 365 * 100 / price_fiat)

            document = {
                "id": token_id,
                "updated": datetime.now().timestamp(),
                "display_id": hero['display_id'],
                "name": self.mapper_service.map_hero_name(rarity_name, level),
                "rarity_name": rarity_name,
                "level": level + 1,
                "hero_class": self.mapper_service.HERO_CLASS_TO_NAME[hero_class].lower(),
                "hero_class_capital": self.mapper_service.HERO_CLASS_TO_NAME[hero_class].capitalize(),
                "fiat_symbol": currency["symbol"],
                "price": price,
                "price_fiat": price_fiat,
                "hero_power": stats['power'],
                "hero_health": stats['health'],
                "hero_speed": stats['speed'],
                "hero_stamina": stats['stamina'],
                "hero_bomb_num": stats['bomb_num'],
                "hero_bomb_range": stats['bomb_range'],
                "mtb_per_day": mtb_per_day,
                "fiat_per_day": fiat_per_day,
                "est_payback": est_payback,
                "est_roi": est_roi
            }

            documents.append(document)

        return documents

    async def get_bomb_documents(self, address, currency):
        bomb_list = await self.metabomb_api_service.get_market_bombs(for_sale=2)
        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        bomb_map = self.mapper_service.get_bomb_map(bomb_list)
        bomb_price_map = self.mapper_service.get_bomb_price_map(bomb_list)
        bomb_nfts = await self.metabomb_moralis_service.get_bombs_by_address(address)

        documents = []

        for bomb_nft in bomb_nfts:

            token_id = str(bomb_nft["token_id"])

            if token_id not in bomb_map:
                continue
            
            bomb = bomb_map[token_id]
            rarity = bomb["rarity"]
            rarity_name = self.mapper_service.BOMB_RARITY_TO_NAME[rarity]
            name = f"{rarity_name} Bomb"
            skills = tuple(bomb[f"skill_{skill_id}"] for skill_id in range(1, 7))

            price = self.mapper_service.get_bomb_price(
                str(rarity),
                skills,
                bomb_price_map
            )
            price_fiat = None

            if price:
                price_fiat = price * mtb_rate

            document = {
                "id": token_id,
                "updated": datetime.now().timestamp(),
                "display_id": bomb['display_id'],
                "name": name,
                "rarity_name": rarity_name,
                "element": self.mapper_service.BOMB_ELEMENT_TO_NAME[bomb["element"]].lower(),
                "fiat_symbol": currency["symbol"],
                "price": price,
                "price_fiat": price_fiat,
                "skill_1": {'skill': bomb['skill_1'],
                            'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_1']]},
                "skill_2": {'skill': bomb['skill_2'],
                            'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_2']]},
                "skill_3": {'skill': bomb['skill_3'],
                            'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_3']]},
                "skill_4": {'skill': bomb['skill_4'],
                            'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_4']]},
                "skill_5": {'skill': bomb['skill_5'],
                            'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_5']]},
                "skill_6": {'skill': bomb['skill_6'],
                            'tooltip': self.mapper_service.SKILLS_TO_TOOLTIP[bomb['skill_6']]},
            }

            documents.append(document)

        return documents

    async def get_box_documents(self, address, currency):
        box_list = await self.metabomb_api_service.get_market_boxes(for_sale=2)
        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        box_price_map = self.mapper_service.get_box_price_map(box_list)

        box_nfts = await self.metabomb_moralis_service.get_boxes_by_address(address)

        documents = []

        balance = await self.metabomb_moralis_service.get_mtb_balance(address=address)
        balance_mtb = Web3.fromWei(int(balance), 'ether')

        for box_nft in box_nfts:

            token_id = str(box_nft["token_id"])

            contract_address = box_nft["token_address"]

            name = self.mapper_service.get_box_name_by_contract_address(
                contract_address
            )

            price = box_price_map.get(name, None)

            price_fiat = None

            if price:
                price_fiat = price * mtb_rate

            document = {
                "id": token_id,
                "updated": datetime.now().timestamp(),
                "name": name,
                "fiat_symbol": currency["symbol"],
                "price": price,
                "price_fiat": price_fiat,
                "balance_mtb": float(balance_mtb),
                "balance_fiat": float(balance_mtb) * mtb_rate,
            }

            documents.append(document)

        return documents
