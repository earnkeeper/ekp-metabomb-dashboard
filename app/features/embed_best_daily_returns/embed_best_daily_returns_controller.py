from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency

from app.features.embed_best_daily_returns.embed_best_daily_returns_service import EmbedBestDailyReturnService
from app.features.heroes_market.listings.heroes_listings_service import HeroListingsService
from app.features.heroes_market.history.heroes_history_service import HeroesHistoryService
from app.features.embed_best_daily_returns.embed_best_daily_returns_tile import tile



class EmbedBestDailyReturnsController:
    def __init__(
            self,
            client_service: ClientService,
            embed_best_daily_return_service: EmbedBestDailyReturnService,
            heroes_history_service: HeroesHistoryService,
            heroes_listings_service: HeroListingsService,
    ):
        self.client_service = client_service
        self.embed_best_daily_return_service = embed_best_daily_return_service
        self.heroes_history_service = heroes_history_service
        self.heroes_listings_service = heroes_listings_service

    async def on_connect(self, sid):
        pass

    async def on_client_state_changed(self, sid, event):
        currency = client_currency(event)

        history_documents = await self.heroes_history_service.get_documents(currency)

        listing_documents = await self.heroes_listings_service.get_documents(currency, history_documents)
        embed_heroes_documents = self.embed_best_daily_return_service.get_documents(listing_documents, currency)

        documents = [{
            "id": 'metabomb-best-daily-returns-tile',
            "size": 'tile',
            "element": tile(),
            "data": embed_heroes_documents,
            "page": 'heroes',
        }]

        await self.client_service.emit_documents(
            sid,
            "embeds",
            documents,
            layer_id='metabomb-best-daily-returns-tile'
        )

