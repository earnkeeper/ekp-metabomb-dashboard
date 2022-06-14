from ekp_sdk.db import MgClient
from pymongo import UpdateOne

class BoxOpensRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['box_opens']
        self.collection.create_index("hash", unique=True)
        self.collection.create_index("block_number")
        self.collection.create_index("timestamp")
        self.collection.create_index("address")
        self.collection.create_index("box_type")
        self.collection.create_index("hero_rarity")

    def find_latest_block_number(self):
        results = list(
            self.collection
            .find()
            .sort("block_number", -1)
            .limit(1)
        )
        
        if not len(results):
            return 0
        
        return results[0]["block_number"]
    
    def find_since_block_number(self, block_number, limit):
        results = list(
            self.collection
            .find({"block_number": {"$gte": block_number}})
            .sort("block_number")
            .limit(limit)
        )
        
        return results

    def save(self, models):
        
        self.collection.bulk_write(
            list(map(lambda model: UpdateOne(
                {"hash": model["hash"]}, {"$set": model}, True), models))
        )
        

