from db.bomb_listing_timestamp_repo import BombListingTimestampRepo
from ekp_sdk.db import ContractTransactionsRepo
from shared.metabomb_api_service import MetabombApiService
from ast import literal_eval


class BombListingTimestampDecoderService:
    def __init__(
            self,
            bomb_listing_timestamp_repo: BombListingTimestampRepo,
            contract_transactions_repo: ContractTransactionsRepo,
            metabomb_api_service: MetabombApiService,
    ):
        self.bomb_listing_timestamp_repo = bomb_listing_timestamp_repo
        self.contract_transactions_repo = contract_transactions_repo
        self.metabomb_api_service = metabomb_api_service
        self.page_size = 2000

    async def decode_bomb_listing_timestamp(self):
        latest_block_number = self.bomb_listing_timestamp_repo.find_latest_block_number()

        while True:
            next_trans = self.contract_transactions_repo.find_since_block_number(latest_block_number, self.page_size)

            models = []

            for next_tran in next_trans:
                input = next_tran["input"]
                block_number = next_tran["blockNumber"]

                if (len(input) < 10):
                    latest_block_number = block_number
                    continue

                if input.startswith("0x0eda2f54"):
                    model = self.__decode_model(next_tran)

                    if model:
                        models.append(model)

                latest_block_number = block_number

            if len(models):
                self.bomb_listing_timestamp_repo.save(models)

            if len(next_trans) < self.page_size:
                break

        print("✅ Finished decoding box opens..")

    def __decode_model(self, tran):

        bomb_token_id = 0

        bomb_token_id = int(tran["input"][10:74], 16)

        model = {
            "tokenId": bomb_token_id,
            "lastListingTimestamp": tran["timeStamp"],
            "blockNumber": tran["blockNumber"],
        }

        return model
