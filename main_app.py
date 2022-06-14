from decouple import AutoConfig
from ekp_sdk import BaseContainer

from app.features.bombs_market.bombs_market_controller import BombsMarketController
from app.features.bombs_market.bombs_summary_service import BombsSummaryService
from app.features.bombs_market.history.bombs_history_service import BombsHistoryService
from app.features.bombs_market.listings.bomb_listings_service import BombListingsService
from app.features.boxes_market.boxes_summary_service import BoxesSummaryService
from app.features.boxes_market.history.boxes_history_service import \
    BoxesHistoryService
from app.features.boxes_market.listings.boxes_listings_service import \
    BoxesListingsService
from app.features.boxes_market.boxes_market_controller import BoxesMarketController
from app.features.dashboard.dash_bomb_sale_price_and_volume_service import BombSalePriceAndVolumeService
from app.features.dashboard.dash_hero_sale_price_and_volume_service import HeroSalePriceAndVolumeService
from app.features.dashboard.dashboard_controller import DashboardController
from app.features.dashboard.dashboard_fusion_service import DashboardFusionService
from app.features.dashboard.dashboard_hero_profit_service import DashboardHeroProfitService
from app.features.dashboard.dashboard_opens_service import \
    DashboardOpensService
from app.features.embed_best_daily_returns.embed_best_daily_returns_controller import EmbedBestDailyReturnsController
from app.features.embed_best_daily_returns.embed_best_daily_returns_service import EmbedBestDailyReturnService
from app.features.embed_box_floor.embed_box_floor_controller import EmbedBoxFloorController
from app.features.heroes_market.heroes_market_controller import HeroesMarketController
from app.features.heroes_market.history.heroes_history_service import HeroesHistoryService
from app.features.heroes_market.listings.heroes_listings_service import HeroListingsService
from app.features.inventory.player.inventory_controller import InventoryController
from app.features.inventory.player.inventory_service import InventoryService
from app.features.inventory.players.players_controller import InventoryPlayersController
from app.features.inventory.players.players_service import InventoryPlayersService
from app.features.heroes_market.heroes_summary_service import HeroesSummaryService
from db.activity_repo import ActivityRepo
from db.bomb_listing_timestamp_repo import BombListingTimestampRepo
from db.bombs_sales_repo import BombsSalesRepo
from db.box_listing_timestamp_repo import BoxListingTimestampRepo
from db.box_opens_repo import BoxOpensRepo
from db.market_sales_repo import MarketSalesRepo
from db.hero_listing_timestamp_repo import HeroListingTimestampRepo
from shared.hero_floor_price_service import HeroFloorPriceService
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from shared.metabomb_moralis_service import MetabombMoralisService
from app.features.embed_box_floor.embed_box_floor_service import EmbedBoxesService
from app.features.embed_hero_floor.embed_hero_floor_service import EmbedHeroesService
from app.features.embed_hero_floor.embed_hero_floor_controller import EmbedHeroesFloorController

class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        self.metabomb_coingecko_service = MetabombCoingeckoService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service
        )
        
        self.metabomb_api_service = MetabombApiService(
            cache_service=self.cache_service
        )

        self.mapper_service = MapperService(
            cache_service=self.cache_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
        )

        self.hero_floor_price_service = HeroFloorPriceService(
            metabomb_api_service=self.metabomb_api_service,
            mapper_service=self.mapper_service            
        )
        
        self.metabomb_moralis_service = MetabombMoralisService(
            cache_service=self.cache_service,
            moralis_api_service=self.moralis_api_service
        )

        # DB

        self.activity_repo = ActivityRepo(
            mg_client=self.mg_client,
        )

        self.box_opens_repo = BoxOpensRepo(
            mg_client=self.mg_client,
        )

        self.market_sales_repo = MarketSalesRepo(
            mg_client=self.mg_client,
        )

        self.hero_listing_timestamp_repo = HeroListingTimestampRepo(
            mg_client=self.mg_client
        )

        self.bomb_listing_timestamp_repo = BombListingTimestampRepo(
            mg_client=self.mg_client
        )

        self.bombs_sales_repo = BombsSalesRepo(
            mg_client=self.mg_client
        )

        # FEATURES - BOXES MARKET

        self.box_listing_timestamp_repo = BoxListingTimestampRepo(
            mg_client=self.mg_client
        )

        self.boxes_listings_service = BoxesListingsService(
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_api_service=self.metabomb_api_service,
            box_listing_timestamp_repo=self.box_listing_timestamp_repo
        )

        self.boxes_history_service = BoxesHistoryService(
            market_sales_repo=self.market_sales_repo,
            metabomb_coingecko_service=self.metabomb_coingecko_service
        )

        self.market_summary_service = BoxesSummaryService()

        self.boxes_market_controller = BoxesMarketController(
            client_service=self.client_service,
            boxes_listings_service=self.boxes_listings_service,
            boxes_history_service=self.boxes_history_service,
            boxes_summary_service=self.market_summary_service
        )

        # FEATURES - HEROES MARKET

        self.heroes_listings_service = HeroListingsService(
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_api_service=self.metabomb_api_service,
            mapper_service=self.mapper_service,
            hero_listing_timestamp_repo=self.hero_listing_timestamp_repo
        )

        self.heroes_history_service = HeroesHistoryService(
            market_sales_repo=self.market_sales_repo,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            mapper_service=self.mapper_service
        )

        self.heroes_summary_service = HeroesSummaryService()

        self.heroes_market_controller = HeroesMarketController(
            client_service=self.client_service,
            heroes_history_service=self.heroes_history_service,
            heroes_listings_service=self.heroes_listings_service,
            heroes_summary_service=self.heroes_summary_service
        )

        # FEATURES - BOMBS MARKET

        self.bombs_listings_service = BombListingsService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            mapper_service=self.mapper_service,
            bomb_listing_timestamp_repo=self.bomb_listing_timestamp_repo
        )

        self.bombs_history_service = BombsHistoryService(
            bombs_sales_repo=self.bombs_sales_repo,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            mapper_service=self.mapper_service
        )

        self.bombs_summary_service = BombsSummaryService()

        # self.heroes_summary_service = HeroesSummaryService()

        self.bombs_market_controller = BombsMarketController(
            client_service=self.client_service,
            bombs_history_service=self.bombs_history_service,
            bombs_listings_service=self.bombs_listings_service,
            bombs_summary_service=self.bombs_summary_service
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

        # FEATURES - INVENTORY - PLAYERS

        self.inventory_players_service = InventoryPlayersService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_moralis_service=self.metabomb_moralis_service,
            mapper_service=self.mapper_service
        )

        self.inventory_players_controller = InventoryPlayersController(
            client_service=self.client_service,
            inventory_players_service=self.inventory_players_service
        )

        # FEATURES - INVENTORY

        self.inventory_service = InventoryService(
            metabomb_api_service=self.metabomb_api_service,
            metabomb_coingecko_service=self.metabomb_coingecko_service,
            metabomb_moralis_service=self.metabomb_moralis_service,
            mapper_service=self.mapper_service
        )

        self.inventory_controller = InventoryController(
            client_service=self.client_service,
            inventory_service=self.inventory_service
        )
        
        # FEATURES - BOX FLOOR EMBED

        self.embed_boxes_service = EmbedBoxesService()
        
        self.embed_box_floor_controller = EmbedBoxFloorController(
            client_service=self.client_service,
            boxes_history_service=self.boxes_history_service,
            boxes_listings_service=self.boxes_listings_service,
            embed_boxes_service=self.embed_boxes_service
        )

        self.embed_heroes_service = EmbedHeroesService()

        self.embed_heroes_floor_controller = EmbedHeroesFloorController(
            client_service=self.client_service,
            embed_heroes_service=self.embed_heroes_service,
            heroes_history_service=self.heroes_history_service,
            heroes_listings_service=self.heroes_listings_service
        )

        self.embed_best_daily_returns_service = EmbedBestDailyReturnService()

        self.embed_best_daily_returns_controller = EmbedBestDailyReturnsController(
            client_service=self.client_service,
            embed_best_daily_return_service=self.embed_best_daily_returns_service,
            heroes_history_service=self.heroes_history_service,
            heroes_listings_service=self.heroes_listings_service
        )


if __name__ == '__main__':
    container = AppContainer()

    container.client_service.add_controller(container.boxes_market_controller)
    container.client_service.add_controller(container.dashboard_controller)
    container.client_service.add_controller(container.heroes_market_controller)
    container.client_service.add_controller(container.bombs_market_controller)
    container.client_service.add_controller(
        container.inventory_players_controller
    )
    container.client_service.add_controller(
        container.inventory_controller
    )
    
    container.client_service.add_controller(container.embed_box_floor_controller)
    container.client_service.add_controller(container.embed_heroes_floor_controller)
    container.client_service.add_controller(container.embed_best_daily_returns_controller)

    container.client_service.listen()
