import asyncio
import json
import logging
from ast import literal_eval
from datetime import datetime
from typing import List

from ekp_sdk.domain import Log
from ekp_sdk.dto import Web3LogDto
from ekp_sdk.services import CacheService, CoingeckoService, Web3Service
from shared.constants import COMMON_BOX_CONTRACT_ADDRESS, HERO_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, ULTRA_BOX_CONTRACT_ADDRESS, BOMB_BOX_CONTRACT_ADDRESS
from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from shared.domain.market_listing import MarketListing
from shared.dto.hero_dto import HeroDto
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from web3 import Web3

from listener.notification_service import NotificationService


class ListenerService:
    def __init__(
        self,
        cache_service: CacheService,
        notification_service: NotificationService,
        mapper_service: MapperService,
        metabomb_api_service: MetabombApiService,
        web3_service: Web3Service,
    ):
        self.cache_service = cache_service
        self.mapper_service = mapper_service
        self.metabomb_api_service = metabomb_api_service
        self.notification_service = notification_service
        self.web3_service = web3_service

    def listen(self):
        common_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(COMMON_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })

        premium_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(PREMIUM_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })

        ultra_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(ULTRA_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })
        bomb_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(BOMB_BOX_CONTRACT_ADDRESS),
            "topics": ["0xe04eefd2590e9186abb360fc0848592add67dcef57f68a4110a6922c4793f7e0"]
        })

        hero_filter = self.web3_service.get_filter({
            "address": Web3.toChecksumAddress(HERO_CONTRACT_ADDRESS),
            "topics": ["0x27bae1fb91b142a2956e7482d5370a469a66deae9cc45d8b0ec35067a54a18ad"]
        })

        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            asyncio.gather(
                self.filter_loop(common_filter, 2),
                self.filter_loop(premium_filter, 2),
                self.filter_loop(ultra_filter, 2),
                self.filter_loop(bomb_filter, 2),
                self.filter_loop(hero_filter, 2),
            )
        )

    async def filter_loop(self, filter, poll_interval):
        while True:
            try:
                for new_event in filter.get_new_entries():
                    listing = await self.decode_market_listing(json.loads(Web3.toJSON(new_event)))
                    await self.process_market_listing(listing)

                await asyncio.sleep(poll_interval)
            except Exception:
                logging.exception("🚨 error while listening for events")
                quit()

    async def decode_market_listing(self, log_dto: Web3LogDto) -> MarketListing:
        log: Log = self.mapper_service.map_web3_log_dto_to_domain(log_dto)

        hash = log["transaction_hash"]

        logging.info(f"🐛 Decoding log: {hash}")

        data = log["data"]

        if len(data) < 66:
            logging.warn(f"⚠️ Skipping tran due to missing data field: {hash}")
            return

        address = log["address"].lower()
        topics = log["topics"]
        hero: Hero = None
        box_type = None
        token_id = literal_eval(topics[1])

        if address == COMMON_BOX_CONTRACT_ADDRESS:
            box_type = 0
        if address == PREMIUM_BOX_CONTRACT_ADDRESS:
            box_type = 1
        if address == ULTRA_BOX_CONTRACT_ADDRESS:
            box_type = 2
        if address == BOMB_BOX_CONTRACT_ADDRESS:
            box_type = 3
        if address == HERO_CONTRACT_ADDRESS:
            hero_dto: HeroDto = await self.metabomb_api_service.get_hero(token_id)
            hero = self.mapper_service.map_hero_dto_to_domain(hero_dto)

        box: HeroBox = None
        if box_type is not None:
            box = {
                "type": box_type,
                "name": self.mapper_service.HERO_BOX_TYPE_TO_NAME[box_type]
            }

        block_number = log["block_number"]
        block = await self.web3_service.get_block(block_number)

        mtb_rate = await self.mapper_service.get_mtb_rate()
        price = Web3.fromWei(literal_eval(data[0:66]), 'ether')
        timestamp = block["timestamp"]
        tran = await self.web3_service.get_transaction(hash)

        listing: MarketListing = {
            "box": box,
            "for_sale": True,
            "hash": hash,
            "hero": hero,
            "id": token_id,
            "listed": timestamp,
            "price_mtb": float(price),
            "price_usdc": float(price) * mtb_rate,
            "seller": tran['from'],
            "token_id": token_id,
            "updated": datetime.now().timestamp(),
        }

        return listing

    async def process_market_listing(self, new_listing: MarketListing):
        logging.info(f"🐛 Processing listing: {new_listing['hash']}")

        floor_listing = None

        if new_listing["box"] is not None:

            dtos = await self.metabomb_api_service.get_market_boxes(for_sale = 2)

            current_listings: List[MarketListing] = await self.mapper_service.map_market_box_dtos_to_domain(dtos)

            filtered_listings = filter(
                lambda current_listing: current_listing['box']['type'] == new_listing['box']['type'],
                current_listings
            )

            floor_listing = self.__get_floor_listing(filtered_listings)

            if (new_listing["price_mtb"] > floor_listing["price_mtb"]):
                logging.warn(
                    f'⚠️ not notifying listing, price ({int(new_listing["price_mtb"])}) is not lower than floor price ({floor_listing["price_mtb"]})'
                )
                return

        if new_listing["hero"] is not None:
            dtos = await self.metabomb_api_service.get_market_heroes(for_sale=2)

            current_listings: List[MarketListing] = await self.mapper_service.map_market_hero_dtos_to_domain(dtos)

            filtered_listings = list(
                filter(
                    lambda current_listing: (current_listing['hero']['rarity'] == new_listing['hero']['rarity']) and (
                        current_listing['hero']['level'] == new_listing['hero']['level']) and (current_listing["for_sale"]),
                    current_listings
                )
            )

            floor_listing = self.__get_floor_listing(filtered_listings)

            if (new_listing["price_mtb"] > floor_listing["price_mtb"]):
                logging.warn(
                    f'⚠️ not notifying listing, price ({int(new_listing["price_mtb"])}) is not lower than floor price ({floor_listing["price_mtb"]})'
                )
                return

        await self.notification_service.send_notification(new_listing, floor_listing)

        logging.info(f"📣 Listing sent to discord: {new_listing['hash']}")

    def __get_floor_listing(self, listings: List[MarketListing]):

        sorted_listings = sorted(
            listings,
            key=lambda filtered_listing: filtered_listing["price_mtb"]
        )

        return sorted_listings[0]
