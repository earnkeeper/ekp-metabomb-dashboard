import asyncio
from ekp_sdk.services import MoralisApiService, CacheService
from shared.utils.lists import flatten

from shared.constants import BOX_CONTRACT_ADDRESSES, HERO_CONTRACT_ADDRESS, BOMB_CONTRACT_ADDRESS, MTB_CONTRACT_ADDRESS


class MetabombMoralisService:
    def __init__(
            self,
            moralis_api_service: MoralisApiService,
            cache_service: CacheService,
    ):
        self.moralis_api_service = moralis_api_service
        self.cache_service = cache_service
        self.cache_expiry = 300

    async def get_heroes_by_address(self, address):
        async def get_from_api(address):
            return await self.moralis_api_service.get_nfts_by_owner_and_token_address(
                address,
                HERO_CONTRACT_ADDRESS,
                'bsc',
            )

        return await self.cache_service.wrap(
            f"metabomb_heroes_{address}",
            lambda: get_from_api(address),
            ex=self.cache_expiry
        )

    async def get_bombs_by_address(self, address):
        async def get_from_api(address):
            return await self.moralis_api_service.get_nfts_by_owner_and_token_address(
                address,
                BOMB_CONTRACT_ADDRESS,
                'bsc',
            )

        return await self.cache_service.wrap(
            f"metabomb_bombs_{address}",
            lambda: get_from_api(address),
            ex=self.cache_expiry
        )

    async def get_boxes_by_address(self, address):
        async def get_from_api(address):
            futures = []

            for contract_address in BOX_CONTRACT_ADDRESSES:
                futures.append(
                    self.moralis_api_service.get_nfts_by_owner_and_token_address(
                        address,
                        contract_address,
                        'bsc',
                    )
                )

            gathered = await asyncio.gather(*futures)

            return flatten(gathered)

        return await self.cache_service.wrap(
            f"metabomb_boxes_{address}",
            lambda: get_from_api(address),
            ex=self.cache_expiry
        )

    async def get_mtb_balance(self, address):

        async def get_from_api(address):
            return await self.moralis_api_service.get_address_token_price(
                chain='bsc',
                token_address=MTB_CONTRACT_ADDRESS,
                address=address,
            )


        return await self.cache_service.wrap(
            f"metabomb_balance_{address}",
            lambda: get_from_api(address),
            ex=self.cache_expiry
        )