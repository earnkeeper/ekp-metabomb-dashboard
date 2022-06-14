from pprint import pprint

from app.features.dashboard.dash_bomb_sale_price_and_volume_service import BombSalePriceAndVolumeService
from app.features.dashboard.dash_hero_sale_price_and_volume_service import HeroSalePriceAndVolumeService
from app.features.dashboard.dashboard_fusion_service import DashboardFusionService
from app.features.dashboard.dashboard_hero_profit_service import DashboardHeroProfitService
from app.features.dashboard.dashboard_opens_service import DashboardOpensService
from app.features.dashboard.dashboard_page import page
from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path, form_values

from app.features.heroes_market.history.heroes_history_service import HeroesHistoryService
from app.features.heroes_market.listings.heroes_listings_service import HeroListingsService

OPENS_COLLECTION_NAME = "metabomb_dashboard_opens"
FUSION_COLLECTION_NAME = "metabomb_dashboard_fusion"
HERO_DASH_PROFIT_COLLECTION_NAME = "metabomb_dashboard_hero_profit_calc"
RARITIES_FORM_NAME = "rarities_form_name"
CHART_COLLECTION_NAME = "chart_collection_name"
BOMB_RARITIES_FORM_NAME = "bomb_rarities_form_name"
BOMB_CHART_COLLECTION_NAME = "bomb_chart_collection_name"


class DashboardController:
    def __init__(
            self,
            client_service: ClientService,
            dashboard_opens_service: DashboardOpensService,
            dashboard_fusion_service: DashboardFusionService,
            dashboard_hero_profit_service: DashboardHeroProfitService,
            dash_hero_sale_price_and_volume_service: HeroSalePriceAndVolumeService,
            dash_bomb_sale_price_and_volume_service: BombSalePriceAndVolumeService
    ):
        self.client_service = client_service
        self.dashboard_opens_service = dashboard_opens_service
        self.dashboard_fusion_service = dashboard_fusion_service
        self.dashboard_hero_profit_service = dashboard_hero_profit_service
        self.dash_hero_sale_price_and_volume_service = dash_hero_sale_price_and_volume_service
        self.dash_bomb_sale_price_and_volume_service = dash_bomb_sale_price_and_volume_service
        self.path = 'dashboard'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'activity',
            'Dashboard',
            self.path,
            order=100,
            id="metabomb_dashboard",
            short_link="mtb-dashboard"
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            page(OPENS_COLLECTION_NAME, FUSION_COLLECTION_NAME,
                 HERO_DASH_PROFIT_COLLECTION_NAME, CHART_COLLECTION_NAME, RARITIES_FORM_NAME,
                 BOMB_RARITIES_FORM_NAME, BOMB_CHART_COLLECTION_NAME),
        )

    async def on_client_state_changed(self, sid, event):
        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, OPENS_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, FUSION_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, HERO_DASH_PROFIT_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, CHART_COLLECTION_NAME)
        await self.client_service.emit_busy(sid, BOMB_CHART_COLLECTION_NAME)

        currency = client_currency(event)

        # ----------------------------------------------------------------------

        opens_documents = await self.dashboard_opens_service.get_documents()

        await self.client_service.emit_documents(
            sid,
            OPENS_COLLECTION_NAME,
            opens_documents
        )

        # ----------------------------------------------------------------------

        fusion_documents = await self.dashboard_fusion_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            FUSION_COLLECTION_NAME,
            fusion_documents
        )

        hero_profit_calc_documents = await self.dashboard_hero_profit_service.get_documents(currency)

        await self.client_service.emit_documents(
            sid,
            HERO_DASH_PROFIT_COLLECTION_NAME,
            hero_profit_calc_documents
        )

        hero_form_values = form_values(event, RARITIES_FORM_NAME)

        if hero_form_values and "rarity" in hero_form_values and "currency" in hero_form_values:
            hero_chart_documents = await self.dash_hero_sale_price_and_volume_service.get_documents(currency,
                                                                                                    hero_form_values[
                                                                                                        'rarity'] or [],
                                                                                                    hero_form_values[
                                                                                                        'currency'] or [])

            await self.client_service.emit_documents(
                sid,
                CHART_COLLECTION_NAME,
                hero_chart_documents
            )

        bomb_form_values = form_values(event, BOMB_RARITIES_FORM_NAME)

        if bomb_form_values and "rarity" in bomb_form_values and "currency" in bomb_form_values:
            bomb_chart_documents = await self.dash_bomb_sale_price_and_volume_service.get_documents(currency,
                                                                                                    bomb_form_values[
                                                                                                        'rarity'] or [],
                                                                                                    bomb_form_values[
                                                                                                        'currency'] or [])
            await self.client_service.emit_documents(
                sid,
                BOMB_CHART_COLLECTION_NAME,
                bomb_chart_documents
            )

        await self.client_service.emit_done(sid, OPENS_COLLECTION_NAME)
        await self.client_service.emit_done(sid, FUSION_COLLECTION_NAME)
        await self.client_service.emit_done(sid, HERO_DASH_PROFIT_COLLECTION_NAME)
        await self.client_service.emit_done(sid, CHART_COLLECTION_NAME)
        await self.client_service.emit_done(sid, BOMB_CHART_COLLECTION_NAME)
