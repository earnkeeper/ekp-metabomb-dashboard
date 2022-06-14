import time
from datetime import datetime

from ekp_sdk.services import CoingeckoService
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from db.box_listing_timestamp_repo import BoxListingTimestampRepo
from shared.metabomb_api_service import MetabombApiService
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class BoxesListingsService:
    def __init__(
        self,
        metabomb_coingecko_service: MetabombCoingeckoService,
        metabomb_api_service: MetabombApiService,
        box_listing_timestamp_repo: BoxListingTimestampRepo
    ):
        self.metabomb_coingecko_service = metabomb_coingecko_service
        self.metabomb_api_service = metabomb_api_service
        self.box_listing_timestamp_repo = box_listing_timestamp_repo

    async def get_documents(self, currency, history_documents):

        box_listing_timestamps = list(self.box_listing_timestamp_repo.collection.find())

        now = datetime.now().timestamp()

        name_totals = self.get_name_totals(history_documents, now)

        listings = await self.metabomb_api_service.get_market_boxes()

        documents = []

        rate = await self.metabomb_coingecko_service.get_mtb_price(currency["id"])

        for listing in listings:
            document = self.map_document(
                listing,
                box_listing_timestamps,
                currency, 
                rate, 
                now, 
                name_totals
            )
            
            if document:
                documents.append(document)

        return documents


    def map_document(self, listing, box_listing_timestamps, currency, rate, now, name_totals):
        price = listing["price"]
        
        box_type = listing["box_type"]

        token_id = int(listing["token_id"])
        
        if box_type not in self.__BOX_TYPES:
            return None

        timestamp = list(filter(lambda x: x['tokenId'] == token_id, box_listing_timestamps))
        name = self.__BOX_TYPES[box_type]

        name_total = None
        if name in name_totals:
            name_total = name_totals[name]

        avg_price_24h = None
        avg_price_fiat_24h = None
        pc_above_avg_price = None
        pc_above_avg_price_fiat = None

        deal = "?"

        if name_total is not None:
            avg_price_24h = name_total["price_total"] / name_total["count"]
            avg_price_fiat_24h = name_total["price_fiat_total"] / \
                name_total["count"]
            pc_above_avg_price = (price - avg_price_24h) * 100 / avg_price_24h
            pc_above_avg_price_fiat = (
                price * rate - avg_price_fiat_24h) * 100 / avg_price_fiat_24h
            if pc_above_avg_price_fiat < 0:
                deal = "yes"
            if pc_above_avg_price_fiat > 1:
                deal = "no"

        return {
            "fiatSymbol": currency["symbol"],
            "id": int(listing["id"]),
            "name": name,
            "avgPrice": avg_price_24h,
            "avgPriceFiat": avg_price_fiat_24h,
            "pcAboveAvg": pc_above_avg_price,
            "pcAboveAvgFiat": pc_above_avg_price_fiat,
            "deal": deal,
            "price": price,
            "priceFiat": price * rate,
            "tokenId": int(listing["token_id"]),
            "type": listing["__typename"],
            "updated": now,
            "last_listing_timestamp": timestamp[0]['lastListingTimestamp'] if timestamp else None,
        }

    def get_name_totals(self, history_documents, now):
        name_totals = {}

        for document in history_documents:
            timestamp = document["timestamp"]

            if (now - timestamp) > 86400:
                continue

            name = document["name"]

            if name not in name_totals:
                name_totals[name] = {
                    "price_total": 0,
                    "price_fiat_total": 0,
                    "count": 0
                }

            name_totals[name]["price_total"] += document["price"]
            name_totals[name]["price_fiat_total"] += document["priceFiat"]
            name_totals[name]["count"] += 1

        return name_totals
    
    __BOX_TYPES = {
        0: "Common Box",
        1: "Premium Box",
        2: "Ultra Box",
        3: "Bomb Box"
    }
