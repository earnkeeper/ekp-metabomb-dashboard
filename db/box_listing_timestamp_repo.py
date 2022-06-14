from ekp_sdk.db import MgClient
from pymongo import UpdateOne
import time


class BoxListingTimestampRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['box_listing_timestamp']
        self.collection.create_index("tokenId", unique=True)
        self.collection.create_index("lastListingTimestamp")
        self.collection.create_index("blockNumber")

    def find_all(self, nftType, limit):
        start = time.perf_counter()

        results = list(
            self.collection
                .find({"nftType": nftType})
                .sort("timestamp")
                .limit(limit)
        )

        print(f"⏱  [MarketSalesRepo.find_all({len(results)})] {time.perf_counter() - start:0.3f}s")

        return results

    def find_latest_block_number(self):
        results = list(
            self.collection
                .find()
                .sort("blockNumber", -1)
                .limit(1)
        )

        if not len(results):
            return 0

        return results[0]["blockNumber"]

    def save(self, models):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda model: UpdateOne({"tokenId": model["tokenId"]}, {"$set": model}, True), models))
        )

        print(f"⏱  [MarketSalesRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s")

