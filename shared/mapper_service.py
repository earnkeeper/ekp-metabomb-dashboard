import asyncio
from datetime import datetime
from typing import List

from ekp_sdk.services import BaseMapperService, CacheService
from shared.constants import COMMON_BOX_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, ULTRA_BOX_CONTRACT_ADDRESS, \
    BOMB_BOX_CONTRACT_ADDRESS
from shared.domain.bomb import Bomb

from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from shared.domain.market_listing import MarketListing
from shared.dto.bomb_market_listing_dto import BombMarketListingDto
from shared.dto.box_market_listing_dto import BoxMarketListingDto
from shared.dto.hero_dto import HeroDto
from shared.dto.hero_market_listing_dto import HeroMarketListingDto
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class MapperService(BaseMapperService):
    def __init__(
            self,
            cache_service: CacheService,
            metabomb_coingecko_service: MetabombCoingeckoService,
    ):
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.cache_service = cache_service

    async def get_mtb_rate(self):
        rate = await self.metabomb_coingecko_service.get_mtb_price("usd")
        return rate

    def map_hero_dto_to_domain(self, dto: HeroDto) -> Hero:
        hero: Hero = {
            'bomb_num': dto['bomb_num'],
            'bomb_range': dto['bomb_range'],
            'display_id': dto['display_id'],
            'health': dto['health'],
            'hero_class': dto['hero_class'],
            'hero_class_name': self.HERO_CLASS_TO_NAME[dto['hero_class']],
            'id': dto['id'],
            'level': dto['level'],
            'name': dto['name'],
            'power': dto['power'],
            'rarity': dto['rarity'],
            'rarity_name': self.HERO_RARITY_TO_NAME[dto['rarity']],
            'speed': dto['speed'],
            'stamina': dto['stamina'],
        }

        return hero

    def get_hero_image_url(self, display_id):
        return f"https://market.metabomb.io/gifs/char-gif/{display_id}.gif"

    def get_hero_box_url(self, box_type):
        return self.HERO_BOX_TYPE_TO_IMAGE_URL[box_type]

    def map_hero_name(self, rarity_name, level):
        return f'{rarity_name} Lv {int(level) + 1} Hero'

    async def map_market_box_dtos_to_domain(self, dtos: List[BoxMarketListingDto]) -> List[MarketListing]:
        mtb_rate = await self.get_mtb_rate()

        futures = []

        for dto in dtos:
            futures.append(self.map_market_box_dto_to_domain(dto, mtb_rate))

        listings = await asyncio.gather(*futures)

        return listings

    def map_box_type_to_domain(self, box_type: int) -> HeroBox:
        box: HeroBox = {
            'type': box_type,
            'name': self.HERO_BOX_TYPE_TO_NAME[box_type]
        }

        return box

    async def map_market_box_dto_to_domain(self, dto: BoxMarketListingDto, mtb_rate: int = None) -> MarketListing:
        box = self.map_box_type_to_domain(dto["box_type"])

        if mtb_rate is None:
            mtb_rate = await self.get_mtb_rate()

        market_listing: MarketListing = {
            'box': box,
            'for_sale': dto['for_sale'] == 1,
            'id': dto['id'],
            'price_mtb': dto['price'],
            'price_usdc': dto['price'] * mtb_rate,
            'token_id': dto['token_id'],
            'updated': datetime.now().timestamp(),
        }

        return market_listing

    async def map_market_hero_dtos_to_domain(self, dtos: List[HeroMarketListingDto]) -> List[MarketListing]:
        mtb_rate = await self.get_mtb_rate()

        futures = []

        for dto in dtos:
            futures.append(self.map_market_hero_dto_to_domain(dto, mtb_rate))

        listings = await asyncio.gather(*futures)

        return listings

    async def map_market_bombs_dtos_to_domain(self, dtos: List[BombMarketListingDto]) -> List[MarketListing]:
        mtb_rate = await self.get_mtb_rate()

        futures = []

        for dto in dtos:
            futures.append(self.map_market_bombs_dto_to_domain(dto, mtb_rate))

        listings = await asyncio.gather(*futures)

        return listings

    def get_hero_map(self, hero_list):
        hero_map = {}

        for hero in hero_list:
            token_id = str(hero["id"])
            hero_map[token_id] = hero

        return hero_map

    def get_bomb_map(self, bomb_list):
        bomb_map = {}

        for bomb in bomb_list:
            token_id = str(bomb["id"])
            bomb_map[token_id] = bomb

        return bomb_map

    def get_hero_price_map(self, hero_list):
        hero_price_map = {}

        for hero in hero_list:
            if not hero["for_sale"]:
                continue

            rarity = str(hero["rarity"])
            level = str(hero["level"])
            price = int(hero["price"])

            if rarity not in hero_price_map:
                hero_price_map[rarity] = {}

            if (level not in hero_price_map[rarity]) or (hero_price_map[rarity][level] > price):
                hero_price_map[rarity][level] = price

        return hero_price_map

    def get_bomb_price_map(self, bomb_list):
        bomb_price_map = {}

        for bomb in bomb_list:
            if not bomb["for_sale"]:
                continue

            rarity = str(bomb["rarity"])
            skills_list = tuple(bomb[f"skill_{skill_id}"] for skill_id in range(1, 7))
            price = int(bomb["price"])

            if rarity not in bomb_price_map:
                bomb_price_map[rarity] = {}

            if (skills_list not in bomb_price_map[rarity]) or (bomb_price_map[rarity][skills_list] > price):
                bomb_price_map[rarity][skills_list] = price

        return bomb_price_map

    def get_box_price_map(self, box_list: List[BoxMarketListingDto]):
        box_price_map = {}

        for box in box_list:
            if ("for_sale" not in box) or (not box["for_sale"]):
                continue

            box_type = box["box_type"]
            box_name = self.get_box_name_by_box_type(box_type)
            price = box["price"]

            if (box_name not in box_price_map) or (box_price_map[box_name] > price):
                box_price_map[box_name] = price

        return box_price_map

    def get_hero_price(self, rarity, level, hero_price_map):
        if str(rarity) not in hero_price_map:
            return None

        if str(level) not in hero_price_map[str(rarity)]:
            return None

        return hero_price_map[str(rarity)][str(level)]

    def get_bomb_price(self, rarity, skills, bomb_price_map):
        if str(rarity) not in bomb_price_map:
            return None

        if skills not in bomb_price_map[str(rarity)]:
            return None

        return bomb_price_map[str(rarity)][skills]

    async def map_market_hero_dto_to_domain(self, dto: HeroMarketListingDto, mtb_rate: int = None) -> MarketListing:
        hero: Hero = {
            'id': dto['id'],
            'display_id': dto['display_id'],
            'hero_class': dto['hero_class'],
            'hero_class_name': self.HERO_CLASS_TO_NAME[dto['hero_class']],
            'level': dto['level'],
            'rarity': dto['rarity'],
            'rarity_name': self.HERO_RARITY_TO_NAME[dto['rarity']],
        }

        if mtb_rate is None:
            mtb_rate = await self.get_mtb_rate()

        market_listing: MarketListing = {
            'hero': hero,
            'for_sale': dto['for_sale'] == 1,
            'id': dto['id'],
            'price_mtb': dto['price'],
            'price_usdc': dto['price'] * mtb_rate,
            'token_id': dto['id'],
            'updated': datetime.now().timestamp(),
        }

        return market_listing

    async def map_market_bombs_dto_to_domain(self, dto: BombMarketListingDto, mtb_rate: int = None) -> MarketListing:
        bomb: Bomb = {
            'id': dto['id'],
            'display_id': dto['display_id'],
            'element': dto['element'],
            'element_name': self.BOMB_ELEMENT_TO_NAME[dto['element']],
            'rarity': dto['rarity'],
            'rarity_name': self.BOMB_RARITY_TO_NAME[dto['rarity']],
            'skill_1': dto['skill_1'],
            'skill_2': dto['skill_2'],
            'skill_3': dto['skill_3'],
            'skill_4': dto['skill_4'],
            'skill_5': dto['skill_5'],
            'skill_6': dto['skill_6'],
        }

        if mtb_rate is None:
            mtb_rate = await self.get_mtb_rate()

        bomb_market_listing: MarketListing = {
            'bomb': bomb,
            'for_sale': dto['for_sale'],
            'id': dto['id'],
            'price_mtb': dto['price'],
            'price_usdc': dto.get('price', 0) * mtb_rate,
            'token_id': dto['id'],
            'updated': datetime.now().timestamp(),
        }

        return bomb_market_listing

    HERO_BOX_TYPE_TO_NAME = {
        0: "Common Box",
        1: "Premium Box",
        2: "Ultra Box",
        3: "Bomb Box"
    }

    def get_box_name_by_contract_address(self, contract_address):
        return self.HERO_BOX_CONTRACT_ADDRESS_TO_NAME.get(contract_address, None)

    def get_box_name_by_box_type(self, box_type):
        return self.HERO_BOX_TYPE_TO_NAME.get(box_type, None)

    HERO_BOX_CONTRACT_ADDRESS_TO_NAME = {
        COMMON_BOX_CONTRACT_ADDRESS: "Common Box",
        PREMIUM_BOX_CONTRACT_ADDRESS: "Premium Box",
        ULTRA_BOX_CONTRACT_ADDRESS: "Ultra Box",
        BOMB_BOX_CONTRACT_ADDRESS: "Bomb Box"
    }

    HERO_CLASS_TO_NAME = {
        0: "Warrior",
        1: "Assassin",
        2: "Mage",
        3: "Support",
        4: "Ranger",
    }

    HERO_RARITY_TO_NAME = {
        0: "Common",
        1: "Rare",
        2: "Epic",
        3: "Legend",
        4: "Mythic",
        5: "Meta",
    }

    BOMB_ELEMENT_TO_NAME = {
        0: "Fire",
        1: "Wood",
        2: "Thunder",
        3: "Earth",
        4: "Water"
    }

    BOMB_RARITY_TO_NAME = {
        0: "Common",
        1: "Rare",
        2: "Epic",
        3: "Legend",
        4: "Mythic",
        5: "Meta",
    }

    SKILLS_TO_TOOLTIP = {
        0: "",
        1: "+2 Damage on diamond chest",
        2: "+5 Damage on meta chest",
        3: "Explosion caused damage through blocks",
        4: "+20% Change of not losing mana when placing bombs",
        5: "+0.5 Mana/Min when resting",
        6: "Go through blocks",
        7: "Go through bombs",
    }

    HERO_BOX_TYPE_TO_IMAGE_URL = {
        0: "https://market.metabomb.io/gifs/herobox-gif/normal-box.gif",
        1: "https://market.metabomb.io/gifs/herobox-gif/premium-box.gif",
        2: "https://market.metabomb.io/gifs/herobox-gif/ultra-box.gif",
        3: "https://market.metabomb.io/gifs/herobox-gif/bomb-box.gif"
    }
