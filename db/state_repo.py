import time

from ekp_sdk.db import MgClient
from pymongo import UpdateOne


class StateRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['state']
        self.collection.create_index("id", unique=True)

    def find(self, id):
        return self.collection.find_one({"id": id})

    def save(self, models):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda model: UpdateOne(
                {"id": model["id"]}, {"$set": model}, True), models))
        )

        print(
            f"⏱  [StateRepo.save({len(models)})] {time.perf_counter() - start:0.3f}s")
