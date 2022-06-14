from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency
from app.features.heroes_market.listings.heroes_listings_service import HeroListingsService
from app.features.heroes_market.history.heroes_history_service import HeroesHistoryService
from app.features.embed_hero_floor.embed_hero_floor_service import EmbedHeroesService
from app.features.embed_hero_floor.embed_hero_floor_tile import tile



class EmbedHeroesFloorController:
    def __init__(
            self,
            client_service: ClientService,
            embed_heroes_service: EmbedHeroesService,
            heroes_history_service: HeroesHistoryService,
            heroes_listings_service: HeroListingsService,
    ):
        self.client_service = client_service
        self.embed_heroes_service = embed_heroes_service
        self.heroes_history_service = heroes_history_service
        self.heroes_listings_service = heroes_listings_service

    async def on_connect(self, sid):
        pass

    async def on_client_state_changed(self, sid, event):
        currency = client_currency(event)

        history_documents = await self.heroes_history_service.get_documents(currency)

        listing_documents = await self.heroes_listings_service.get_documents(currency, history_documents)
        embed_heroes_documents = self.embed_heroes_service.get_documents(listing_documents, history_documents, currency)

        documents = [{
            "id": 'metabomb-hero-tile',
            "size": 'tile',
            "element": tile(),
            "data": embed_heroes_documents,
            "page": 'heroes',
        }]

        await self.client_service.emit_documents(
            sid,
            "embeds",
            documents,
            layer_id='metabomb-hero-tile'
        )

