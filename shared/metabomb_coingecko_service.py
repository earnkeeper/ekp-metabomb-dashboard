from ekp_sdk.services import CoingeckoService, CacheService

class MetabombCoingeckoService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service

    async def get_mtb_price(self, currency_id):
        return await self.cache_service.wrap(
            f"coingecko_price_metabomb_{currency_id}",
            lambda: self.coingecko_service.get_latest_price('metabomb', currency_id),
            ex=300
        )
        
    async def get_usd_price(self, currency_id):
        return await self.cache_service.wrap(
            f"coingecko_price_usdcoin_{currency_id}",
            lambda: self.coingecko_service.get_latest_price('usd-coin', currency_id),
            ex=300
        )    