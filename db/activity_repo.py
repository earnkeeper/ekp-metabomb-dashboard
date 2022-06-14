from ekp_sdk.db import MgClient


class ActivityRepo:
    def __init__(
        self,
        mg_client: MgClient
    ):
        self.mg_client = mg_client
        self.db = self.mg_client.client['activity']
        self.collection = self.db['activity']

    def find_all(self):
        return list(self.collection.find({ "game_slug": "metabomb" }))
