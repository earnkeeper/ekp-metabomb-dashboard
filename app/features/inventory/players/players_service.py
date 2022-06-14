from pprint import pprint

from shared.constants import MTB_CONTRACT_ADDRESS
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService

from datetime import datetime

from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from web3 import Web3

class InventoryPlayersService:
    def __init__(
            self,
            mapper_service: MapperService,
            metabomb_api_service: MetabombApiService,
            metabomb_coingecko_service: MetabombCoingeckoService,
            metabomb_moralis_service: MetabombMoralisService,
    ):
        self.mapper_service = mapper_service
        self.metabomb_api_service = metabomb_api_service
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.metabomb_moralis_service = metabomb_moralis_service

    async def get_documents(self, currency, form_values):
        documents = []

        hero_list = await self.metabomb_api_service.get_market_heroes(for_sale=2)
        box_list = await self.metabomb_api_service.get_market_boxes(for_sale=2)
        bomb_list = await self.metabomb_api_service.get_market_bombs(for_sale=2)

        mtb_rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        hero_map = self.mapper_service.get_hero_map(hero_list)
        bomb_map = self.mapper_service.get_bomb_map(bomb_list)

        hero_price_map = self.mapper_service.get_hero_price_map(hero_list)
        bomb_price_map = self.mapper_service.get_bomb_price_map(bomb_list)
        box_price_map = self.mapper_service.get_box_price_map(box_list)

        for form_value in form_values:
            address = form_value["address"]

            balance = await self.metabomb_moralis_service.get_mtb_balance(address=address)
            balance_mtb = Web3.fromWei(int(balance), 'ether')
            document = await self.__get_document(
                address,
                currency,
                balance_mtb,
                hero_map,
                hero_price_map,
                bomb_map,
                bomb_price_map,
                box_price_map,
                mtb_rate
            )

            documents.append(document)

        return documents

    async def __get_document(
            self,
            address,
            currency,
            balance_mtb,
            hero_map,
            hero_price_map,
            bomb_map,
            bomb_price_map,
            box_price_map,
            mtb_rate
    ):

        box_nfts = await self.metabomb_moralis_service.get_boxes_by_address(address)
        hero_nfts = await self.metabomb_moralis_service.get_heroes_by_address(address)
        bomb_nfts = await self.metabomb_moralis_service.get_bombs_by_address(address)

        total_price = 0

        total_mtb_per_day = 0

        for bomb_nft in bomb_nfts:
            token_id = bomb_nft["token_id"]

            if token_id not in bomb_map:
                continue

            bomb = bomb_map[token_id]

            rarity = str(bomb["rarity"])

            skills = tuple(bomb[f"skill_{skill_id}"] for skill_id in range(1, 7))

            price = self.mapper_service.get_bomb_price(
                rarity,
                skills,
                bomb_price_map
            )

            if price:
                total_price += price

        for hero_nft in hero_nfts:
            token_id = str(hero_nft["token_id"])

            stats = hero_map[token_id]

            mtb_per_day = 0.145 * 0.5 * 1440 * stats['power']

            total_mtb_per_day += mtb_per_day

            if token_id not in hero_map:
                continue

            hero = hero_map[token_id]

            rarity = str(hero["rarity"])

            level = str(hero["level"])

            price = self.mapper_service.get_hero_price(
                rarity,
                level,
                hero_price_map
            )

            if price:
                total_price += price

        for box_nft in box_nfts:
            contract_address = box_nft["token_address"]

            box_name = self.mapper_service.get_box_name_by_contract_address(
                contract_address
            )

            price = box_price_map.get(box_name, None)

            if price:
                total_price += price

        document = {
            "id": address,
            "updated": datetime.now().timestamp(),
            "fiat_symbol": currency["symbol"],
            "boxes": len(box_nfts),
            "heroes": len(hero_nfts),
            "bombs": len(bomb_nfts),
            "balance_mtb": float(balance_mtb),
            "balance_fiat": float(balance_mtb) * mtb_rate,
            "market_value_fiat": total_price * mtb_rate,
            "est_mtb_per_day": total_mtb_per_day
        }

        return document
