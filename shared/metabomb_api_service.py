import time
from typing import List

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from shared.dto.bomb_dto import BombDto
from shared.dto.box_market_listing_dto import BoxMarketListingDto
from shared.dto.hero_dto import HeroDto
from shared.dto.hero_market_listing_dto import HeroMarketListingDto
from shared.dto.bomb_market_listing_dto import BombMarketListingDto

from ekp_sdk.services import CacheService


class MetabombApiService:
    def __init__(
            self,
            cache_service: CacheService
    ):
        self.base_url = "https://api.metabomb.io/graphql/"
        self.cache_service = cache_service

    async def get_hero(self, token_id) -> HeroDto:
        return await self.__gql_get(
            self.__HERO_QUERY,
            {"id": str(token_id)},
            lambda x: x["hero"]
        )

    async def get_bomb(self, token_id) -> BombDto:
        return await self.__gql_get(
            self.__BOMB_QUERY,
            {"id": str(token_id)},
            lambda x: x["bomb"]
        )
    async def get_market_boxes(self, for_sale=1) -> List[BoxMarketListingDto]:
        return await self.cache_service.wrap(
            f"metabomb_box_listings_{for_sale}",
            lambda: self.__gql_get(
                self.__MARKET_BOX_QUERY,
                self.__market_box_params(1, 10000, for_sale),
                lambda x: x["box_market"]["boxes"]
            ),
            ex=60
        )
        
    async def get_market_heroes(self, for_sale=1) -> List[HeroMarketListingDto]:
        return await self.cache_service.wrap(
            f"metabomb_hero_listings_{for_sale}",
            lambda: self.__gql_get(
                self.__MARKET_HERO_QUERY,
                self.__market_hero_params(1, 10000, for_sale),
                lambda x: x["hero_market"]["heroes"]
            ),
            ex=60
        )

    async def get_market_bombs(self, for_sale=1) -> List[BombMarketListingDto]:
        return await self.cache_service.wrap(
            f"metabomb_bomb_listings_{for_sale}",
            lambda: self.__gql_get(
                self.__MARKET_BOMBS_QUERY,
                self.__market_bombs_params(1, 10000, for_sale),
                lambda x: x["bomb_market"]["bombs"]
            ),
            ex=60
        )

    async def __gql_get(self, query, variables, fn=lambda x: x):
        url = self.base_url

        print(f"🐛 {url}")

        start = time.perf_counter()

        transport = AIOHTTPTransport(url=url)

        async with Client(transport=transport) as client:
            gql_result = await client.execute(
                query,
                variable_values=variables
            )

            print(f"⏱  [{url}] {time.perf_counter() - start:0.3f}s")

            return fn(gql_result)

    __MARKET_BOX_QUERY = gql("""
        query box_market($input: BoxMarketInput!) {
        box_market(input: $input) {
            error
            count
            boxes {
            id
            token_id
            box_type
            price
            for_sale
            chain_process
            __typename
            }
            __typename
        }
        }
        """)

    __MARKET_HERO_QUERY = gql("""
            query hero_market($input: HeroMarketInput!) {
                hero_market(input: $input) {
                    error
                    count
                    heroes {
                        id
                        name
                        display_id
                        rarity
                        level
                        hero_class
                        for_sale
                        price
                        power
                        health
                        speed
                        stamina
                        bomb_num
                        bomb_range
                        __typename
                    }
                    __typename
                }
            }
        """)

    __MARKET_BOMBS_QUERY = gql("""
                query bomb_market($input: BombMarketInput!) {
                  bomb_market(input: $input) {
                    error
                    count
                    bombs {
                      id
                      rarity
                      skill_1
                      skill_2
                      skill_3
                      skill_4
                      skill_5
                      skill_6
                      display_id
                      element
                      for_sale
                      price
                      __typename
                    }
                    __typename
                  }
                }
            """)

    __HERO_QUERY = gql("""
        query hero($id: ID!) {
            hero(id: $id) {
                id
                user_id
                name
                display_id
                rarity
                level
                hero_class
                for_sale
                price
                power
                health
                speed
                stamina
                bomb_num
                bomb_range
                user {
                id
                name
                user_name
                __typename
                }
                __typename
            }
        }
        """)

    __BOMB_QUERY = gql("""
            query bomb($id: ID!) {
              bomb(id: $id) {
                id
                user_id
                rarity
                skill_1
                skill_2
                skill_3
                skill_4
                skill_5
                skill_6
                display_id
                element
                for_sale
                price
                user {
                  id
                  name
                  user_name
                  __typename
                }
                __typename
              }
            }
            """)

    def __market_box_params(self, page, count, for_sale = 1):
        return {
            "input": {
                "f5": 0,
                "token_id": -1,
                "page": page,
                "count": count,
                "sort": 0,
                "sort_type": 3,
                "box_type": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5
                ],
                "forSale": for_sale

            }
        }

    def __market_hero_params(self, page, count, for_sale=1):
        return {
            "input": {
                "f5": 0,
                "rarity": [0, 1, 2, 3, 4, 5],
                "class_hero": [0, 1, 2, 3, 4],
                "power": [1, 18],
                "speed": [1, 18],
                "health": [1, 18],
                "stamina": [1, 18],
                "bomb_num": [1, 4],
                "bomb_range": [1, 4],
                "level": [0, 6],
                "page": page,
                "count": count,
                "sort": 0,
                "sort_type": 1,
                "forSale": for_sale
            }

        }

    def __market_bombs_params(self, page, count, for_sale=1):
        return {
            "input":
                {
                    "f5": 0,
                    "rarity": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5
                    ],
                    "element": [
                        0,
                        1,
                        2,
                        3,
                        4
                    ],
                    "skill": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                    ],
                    "page": page,
                    "count": count,
                    "sort": 0,
                    "sort_type": 3,
                    "forSale": for_sale
                }
        }
