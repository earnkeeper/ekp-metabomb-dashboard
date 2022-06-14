from db.market_sales_repo import MarketSalesRepo
from shared.metabomb_coingecko_service import MetabombCoingeckoService


class BoxesHistoryService:
    def __init__(
        self,
        market_sales_repo: MarketSalesRepo,
        metabomb_coingecko_service: MetabombCoingeckoService
    ):
        self.market_sales_repo = market_sales_repo
        self.metabomb_coingecko_service = metabomb_coingecko_service

    async def get_documents(self, currency):
        rate = await self.metabomb_coingecko_service.get_usd_price(currency["id"])

        models = self.market_sales_repo.find_all('box', 1000)

        documents = []

        for model in models:
            document = self.map_document(model, currency, rate)
            documents.append(document)

        return documents

    def map_document(self, model, currency, rate):

        return {
            "bnbCost": model["bnbCost"],
            "bnbCostFiat": model["bnbCostUsd"] * rate,
            "buyer": model["buyer"],
            "fiatSymbol": currency["symbol"],
            "hash": model["hash"],
            "name": model["box"]["name"],
            "type": model["nftType"],
            "price": model["price"],
            "priceFiat": model["priceUsd"] * rate,
            "seller": model["seller"],
            "updated": model["timestamp"],
            "timestamp": model["timestamp"],
            "tokenId": model["tokenId"],
        }
