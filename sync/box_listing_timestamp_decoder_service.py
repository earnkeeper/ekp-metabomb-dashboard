from db.box_listing_timestamp_repo import BoxListingTimestampRepo
from ekp_sdk.db import ContractTransactionsRepo
from shared.metabomb_api_service import MetabombApiService
from ast import literal_eval

TOKEN_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


class BoxListingTimestampDecoderService:
    def __init__(
            self,
            box_listing_timestamp_repo: BoxListingTimestampRepo,
            contract_transactions_repo: ContractTransactionsRepo,
            metabomb_api_service: MetabombApiService,
    ):
        self.box_listing_timestamp_repo = box_listing_timestamp_repo
        self.contract_transactions_repo = contract_transactions_repo
        self.metabomb_api_service = metabomb_api_service
        self.page_size = 2000

    async def decode_box_listing_timestamp(self):
        latest_block_number = self.box_listing_timestamp_repo.find_latest_block_number()

        while True:
            next_trans = self.contract_transactions_repo.find_since_block_number(latest_block_number, self.page_size)

            models = []

            for next_tran in next_trans:
                input = next_tran["input"]
                block_number = next_tran["blockNumber"]

                if (len(input) < 10):
                    latest_block_number = block_number
                    continue

                if input.startswith("0x36f7992b"):
                    model = self.__decode_model(next_tran)

                    if model:
                        models.append(model)

                latest_block_number = block_number

            if len(models):
                self.box_listing_timestamp_repo.save(models)

            if len(next_trans) < self.page_size:
                break

        print("✅ Finished decoding box opens..")

    def __decode_model(self, tran):

        box_token_id = 0

        box_token_id = int(tran["input"][10:74], 16)

        model = {
            "tokenId": box_token_id,
            "lastListingTimestamp": tran["timeStamp"],
            "blockNumber": tran["blockNumber"],
        }

        return model
