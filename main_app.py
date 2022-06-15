from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.dashboard.dash_bomb_sale_price_and_volume_service import BombSalePriceAndVolumeService
from app.features.dashboard.dash_hero_sale_price_and_volume_service import HeroSalePriceAndVolumeService
from app.features.dashboard.dashboard_controller import DashboardController
from app.features.dashboard.dashboard_fusion_service import DashboardFusionService
from app.features.dashboard.dashboard_hero_profit_service import DashboardHeroProfitService
from app.features.dashboard.dashboard_opens_service import \
    DashboardOpensService

from db.bombs_sales_repo import BombsSalesRepo
from db.box_opens_repo import BoxOpensRepo
from db.market_sales_repo import MarketSalesRepo
from shared.hero_floor_price_service import HeroFloorPriceService
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        self.metabomb_coingecko_service = MetabombCoingeckoService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service
        )
        #
        self.metabomb_api_service = MetabombApiService(
            cache_service=self.cache_service
        )

        self.mapper_service = MapperService(
            cache_service=self.cache_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
        )
        #
        self.hero_floor_price_service = HeroFloorPriceService(
            metabomb_api_service=self.metabomb_api_service,
            mapper_service=self.mapper_service
        )

        self.box_opens_repo = BoxOpensRepo(
            mg_client=self.mg_client,
        )

        self.market_sales_repo = MarketSalesRepo(
            mg_client=self.mg_client,
        )

        self.bombs_sales_repo = BombsSalesRepo(
            mg_client=self.mg_client
        )

        # FEATURES - DASHBOARD

        self.dashboard_opens_service = DashboardOpensService(
            box_opens_repo=self.box_opens_repo
        )

        self.dashboard_fusion_service = DashboardFusionService(
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            hero_floor_price_service=self.hero_floor_price_service
        )

        self.dashboard_hero_profit_service = DashboardHeroProfitService(
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            hero_floor_price_service=self.hero_floor_price_service
        )

        self.dash_hero_sale_price_and_volume_service = HeroSalePriceAndVolumeService(
            market_sales_repo=self.market_sales_repo,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            mapper_service=self.mapper_service
        )

        self.dash_bomb_sale_price_and_volume_service = BombSalePriceAndVolumeService(
            bombs_sales_repo=self.bombs_sales_repo,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            mapper_service=self.mapper_service
        )

        self.dashboard_controller = DashboardController(
            client_service=self.client_service,
            dashboard_opens_service=self.dashboard_opens_service,
            dashboard_fusion_service=self.dashboard_fusion_service,
            dashboard_hero_profit_service=self.dashboard_hero_profit_service,
            dash_hero_sale_price_and_volume_service=self.dash_hero_sale_price_and_volume_service,
            dash_bomb_sale_price_and_volume_service=self.dash_bomb_sale_price_and_volume_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.dashboard_controller)

    # container.client_service.add_controller(container.embed_box_floor_controller)
    # container.client_service.add_controller(container.embed_heroes_floor_controller)
    # container.client_service.add_controller(container.embed_best_daily_returns_controller)

    container.client_service.listen()
