
import asyncio

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from db.bomb_listing_timestamp_repo import BombListingTimestampRepo
from db.bombs_sales_repo import BombsSalesRepo
from db.box_listing_timestamp_repo import BoxListingTimestampRepo
from db.box_opens_repo import BoxOpensRepo
from db.hero_listing_timestamp_repo import HeroListingTimestampRepo
from db.market_sales_repo import MarketSalesRepo
from db.state_repo import StateRepo
from shared.constants import HERO_CONTRACT_ADDRESS, MTB_CONTRACT_ADDRESS, BOMB_CONTRACT_ADDRESS
from shared.mapper_service import MapperService
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService
from sync.bomb_listing_timestamp_decoder_service import BombListingTimestampDecoderService
from sync.bomb_sale_decoder_service import BombsSaleDecoderService
from sync.box_listing_timestamp_decoder_service import BoxListingTimestampDecoderService
from sync.box_open_decoder_service import COMMON_BOX_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, ULTRA_BOX_CONTRACT_ADDRESS, BOMB_BOX_CONTRACT_ADDRESS, BoxOpenDecoderService
from sync.box_sale_decoder_service import BoxSaleDecoderService
from sync.hero_sale_decoder_service import HeroSaleDecoderService
from sync.hero_listing_timestamp_decoder_service import HeroListingTimestampDecoderService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        # DB
        
        self.market_transactions_repo = MarketSalesRepo(
            mg_client=self.mg_client,
        )

        self.box_opens_repo = BoxOpensRepo(
            mg_client=self.mg_client,
        )

        self.state_repo = StateRepo(
            mg_client=self.mg_client,
        )

        self.hero_listing_timestamp_repo = HeroListingTimestampRepo(
            mg_client=self.mg_client
        )
        self.box_listing_timestamp_repo = BoxListingTimestampRepo(
            mg_client=self.mg_client
        )

        self.bomb_listing_timestamp_repo = BombListingTimestampRepo(
            mg_client=self.mg_client
        )

        self.bombs_sales_repo = BombsSalesRepo(
            mg_client=self.mg_client
        )

        # Services
        
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

        self.box_open_decoder_service = BoxOpenDecoderService(
            box_opens_repo=self.box_opens_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            metabomb_api_service=self.metabomb_api_service
        )

        self.box_sale_decoder_service = BoxSaleDecoderService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            contract_transactions_repo=self.contract_transactions_repo,
            market_sales_repo=self.market_transactions_repo,
            mapper_service=self.mapper_service,
        )

        self.hero_sale_decoder_service = HeroSaleDecoderService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            contract_transactions_repo=self.contract_transactions_repo,
            market_sales_repo=self.market_transactions_repo,
            mapper_service=self.mapper_service,
            metabomb_api_service=self.metabomb_api_service
        )

        self.hero_listing_timestamp_decoder_service = HeroListingTimestampDecoderService(
            hero_listing_timestamp_repo=self.hero_listing_timestamp_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            metabomb_api_service=self.metabomb_api_service
        )

        self.box_listing_timestamp_decoder_service = BoxListingTimestampDecoderService(
            box_listing_timestamp_repo=self.box_listing_timestamp_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            metabomb_api_service=self.metabomb_api_service
        )

        self.bomb_listing_timestamp_decoder_service = BombListingTimestampDecoderService(
            bomb_listing_timestamp_repo=self.bomb_listing_timestamp_repo,
            contract_transactions_repo=self.contract_transactions_repo,
            metabomb_api_service=self.metabomb_api_service
        )

        self.bomb_sale_decoder_service = BombsSaleDecoderService(
            cache_service=self.cache_service,
            coingecko_service=self.coingecko_service,
            contract_transactions_repo=self.contract_transactions_repo,
            bombs_sales_repo=self.bombs_sales_repo,
            mapper_service=self.mapper_service,
            metabomb_api_service=self.metabomb_api_service
        )

if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    loop = asyncio.get_event_loop()

    contract_addresses = [
        HERO_CONTRACT_ADDRESS,
        BOMB_CONTRACT_ADDRESS,
        COMMON_BOX_CONTRACT_ADDRESS,
        PREMIUM_BOX_CONTRACT_ADDRESS,
        ULTRA_BOX_CONTRACT_ADDRESS,
        BOMB_BOX_CONTRACT_ADDRESS,
    ]

    log_addresses = [
        HERO_CONTRACT_ADDRESS,
        BOMB_CONTRACT_ADDRESS,
        COMMON_BOX_CONTRACT_ADDRESS,
        PREMIUM_BOX_CONTRACT_ADDRESS,
        ULTRA_BOX_CONTRACT_ADDRESS,
        BOMB_BOX_CONTRACT_ADDRESS,
        MTB_CONTRACT_ADDRESS
    ]

    futures = []

    for contract_address in contract_addresses:
        futures.append(
            container.transaction_sync_service.sync_transactions(contract_address, 17394713)
        )
    
    for log_address in log_addresses:
        futures.append(
            container.transaction_sync_service.sync_logs(log_address, 17394713)
        )
    
    loop.run_until_complete(
        asyncio.gather(*futures)
    )
    
    loop.run_until_complete(
        container.box_sale_decoder_service.decode_box_sales()
    )
    
    loop.run_until_complete(
        container.hero_sale_decoder_service.decode_hero_sales()
    )
    
    loop.run_until_complete(
        container.box_open_decoder_service.decode_box_openings()
    )
    
    loop.run_until_complete(
        container.hero_listing_timestamp_decoder_service.decode_hero_listing_timestamp()
    )
    
    loop.run_until_complete(
        container.box_listing_timestamp_decoder_service.decode_box_listing_timestamp()
    )

    loop.run_until_complete(
        container.bomb_sale_decoder_service.decode_bomb_sales()
    )

    loop.run_until_complete(
        container.bomb_listing_timestamp_decoder_service.decode_bomb_listing_timestamp()
    )
