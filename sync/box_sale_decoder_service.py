import logging
import sys
from ast import literal_eval
from datetime import datetime

from db.market_sale_model import MarketSaleModel
from db.market_sales_repo import MarketSalesRepo
from ekp_sdk.db import ContractTransactionsRepo
from ekp_sdk.services import CacheService, CoingeckoService
from shared.constants import COMMON_BOX_CONTRACT_ADDRESS, MTB_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, \
    ULTRA_BOX_CONTRACT_ADDRESS, BOMB_BOX_CONTRACT_ADDRESS
from shared.mapper_service import MapperService
from web3 import Web3

HERO_BOX_TRANSFER_TOPIC = "0xd61e22991e1ab43a17e1ba8ddb78b72a4ffc0d7f455c8536073a6b8a9ffc0c4e"
BOMB_BOX_TRANSFER_TOPIC = "0x980eeb99bdb8de3043fd81f10d249141f5388fce276dd92ee88400c28d4c3a5b"

class BoxSaleDecoderService:
    def __init__(
        self,
        cache_service: CacheService,
        coingecko_service: CoingeckoService,
        contract_transactions_repo: ContractTransactionsRepo,
        market_sales_repo: MarketSalesRepo,
        mapper_service: MapperService,
    ):
        self.cache_service = cache_service
        self.coingecko_service = coingecko_service
        self.contract_transactions_repo = contract_transactions_repo
        self.market_sales_repo = market_sales_repo
        self.mapper_service = mapper_service

        self.page_size = 2000

    async def decode_box_sales(self):
        print("✨ Decoding box sales..")

        latest_block = self.market_sales_repo.find_latest_block_number("box")

        while True:
            next_trans = self.contract_transactions_repo.find_since_block_number(
                latest_block,
                self.page_size,
                "0x38edf988",
            )

            if not len(next_trans):
                break

            sales = []

            for next_tran in next_trans:
                block_number = next_tran["blockNumber"]

                sale = await self.__decode_box_sale(next_tran)

                if sale:
                    sales.append(sale)

                latest_block = block_number

            if len(sales):
                self.market_sales_repo.save(sales)

            if len(next_trans) < self.page_size:
                break

        print("✅ Finished hero box sales..")

    async def __decode_box_sale(self, tran):
        hash = tran["hash"]
        
        if "logs" not in tran:
            logging.warn(f'⚠️ skipping box decode, no logs: {hash}')
            return None

        timestamp = tran["timeStamp"]
        block_number = tran["blockNumber"]
        date_str = datetime.utcfromtimestamp(timestamp).strftime("%d-%m-%Y")

        bnb_cache_key = f"bnb_price_{date_str}"
        bnb_usd_price = await self.cache_service.wrap(bnb_cache_key, lambda: self.coingecko_service.get_historic_price("binancecoin", date_str, "usd"))

        mtb_cache_key = f"mtb_price_{date_str}"
        mtb_usd_price = await self.cache_service.wrap(mtb_cache_key, lambda: self.coingecko_service.get_historic_price("metabomb", date_str, "usd"))

        distributions = []
        box_type = None
        price = 0
        seller = None
        token_id = 0

        logs = tran["logs"].values()

        for log in logs:
            address = log["address"]
            data = log["data"]
            topics = log["topics"]

            if address == MTB_CONTRACT_ADDRESS:
                dec = Web3.fromWei(literal_eval(data), 'ether')
                distributions.append(dec)
            if address == COMMON_BOX_CONTRACT_ADDRESS and topics[0] == HERO_BOX_TRANSFER_TOPIC:
                token_id = literal_eval(topics[1])
                box_type = 0
            if address == PREMIUM_BOX_CONTRACT_ADDRESS and topics[0] == HERO_BOX_TRANSFER_TOPIC:
                token_id = literal_eval(topics[1])
                box_type = 1
            if address == ULTRA_BOX_CONTRACT_ADDRESS and topics[0] == HERO_BOX_TRANSFER_TOPIC:
                token_id = literal_eval(topics[1])
                box_type = 2
            if address == BOMB_BOX_CONTRACT_ADDRESS and topics[0] == BOMB_BOX_TRANSFER_TOPIC:
                token_id = literal_eval(topics[1])
                box_type = 3

        if box_type is None:
            logging.warn(f'⚠️ could not find box type for sale: {hash}')

        if not len(distributions):
            logging.warn(f'⚠️ skipping box decode, no distribution logs: {hash}')
            return None
        
        distributions.sort()

        bnb_cost = Web3.fromWei(tran["gasUsed"] * tran["gasPrice"], 'ether')
        price = sum(distributions)
        fees = price - distributions[-1]

        box = self.mapper_service.map_box_type_to_domain(box_type)

        sale: MarketSaleModel = {
            "bnbCost": float(bnb_cost),
            "bnbCostUsd": float(bnb_cost) * bnb_usd_price,
            "blockNumber": block_number,
            "box": box,
            "buyer": tran["from"],
            "fees": float(fees),
            "feesUsd": float(fees) * mtb_usd_price,
            "hash": hash,
            "nftType": "box",
            "price": float(price),
            "priceUsd": float(price) * mtb_usd_price,
            "seller": seller,
            "timestamp": timestamp,
            "tokenId": token_id,
        }

        return sale
