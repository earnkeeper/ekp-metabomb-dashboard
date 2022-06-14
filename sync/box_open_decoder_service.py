from db.box_opens_repo import BoxOpensRepo
from ekp_sdk.db import ContractTransactionsRepo
from shared.metabomb_api_service import MetabombApiService
from ast import literal_eval
from shared.constants import COMMON_BOX_CONTRACT_ADDRESS, HERO_CONTRACT_ADDRESS, PREMIUM_BOX_CONTRACT_ADDRESS, ULTRA_BOX_CONTRACT_ADDRESS, BOMB_BOX_CONTRACT_ADDRESS

TOKEN_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


class BoxOpenDecoderService:
    def __init__(
        self,
        box_opens_repo: BoxOpensRepo,
        contract_transactions_repo: ContractTransactionsRepo,
        metabomb_api_service: MetabombApiService,
    ):
        self.box_opens_repo = box_opens_repo
        self.contract_transactions_repo = contract_transactions_repo
        self.metabomb_api_service = metabomb_api_service
        self.page_size = 2000
        
        
    async def decode_box_openings(self):
        heroes = await self.metabomb_api_service.get_market_heroes(for_sale=2)
        
        heroes_map = {}
        
        for hero in heroes:
            heroes_map[str(hero["id"])] = hero
        
        latest_block_number = self.box_opens_repo.find_latest_block_number()
        while True:
            next_trans = self.contract_transactions_repo.find_since_block_number(latest_block_number, self.page_size)
            
            models = []
            
            for next_tran in next_trans:
                input = next_tran["input"]
                block_number = next_tran["blockNumber"]

                if (len(input) < 10):
                    latest_block_number = block_number
                    continue

                if input.startswith("0xf35dea5a"):
                    if "logs" not in next_tran:
                        print(f"⚠️ no logs found for tran: {next_tran['hash']}")
                        continue;
                    
                    model = self.__decode_model(next_tran, heroes_map)
                    
                    if model:
                        models.append(model)

                latest_block_number = block_number

            if len(models):
                self.box_opens_repo.save(models)

            if len(next_trans) < self.page_size:
                break

        print("✅ Finished decoding box opens..")

    def __decode_model(self, tran, heroes_map):
        
        logs = tran["logs"].values()

        box_type = None
        box_token_id = 0
        hero_token_id = 0
        
        for log in logs:
            address = log["address"]
            topics = log["topics"]

            if (address == COMMON_BOX_CONTRACT_ADDRESS) and (topics[0] == TOKEN_TRANSFER_TOPIC):
                box_token_id = literal_eval(topics[3])
                box_type = "Common Box"
            if (address == PREMIUM_BOX_CONTRACT_ADDRESS) and (topics[0] == TOKEN_TRANSFER_TOPIC):
                box_token_id = literal_eval(topics[3])
                box_type = "Premium Box"
            if (address == ULTRA_BOX_CONTRACT_ADDRESS) and (topics[0] == TOKEN_TRANSFER_TOPIC):
                box_token_id = literal_eval(topics[3])
                box_type = "Ultra Box"
            if (address == BOMB_BOX_CONTRACT_ADDRESS) and (topics[0] == TOKEN_TRANSFER_TOPIC):
                box_token_id = literal_eval(topics[3])
                box_type = "Bomb Box"
            if (address == HERO_CONTRACT_ADDRESS) and (topics[0] == TOKEN_TRANSFER_TOPIC):
                hero_token_id = literal_eval(topics[3])

        if (not box_token_id) or (not hero_token_id):
            return None

        if str(hero_token_id) not in heroes_map:
            return None
        
        hero = heroes_map[str(hero_token_id)]
        
        
        model = {
            "address": tran["from"],
            "block_number": tran["blockNumber"],
            "box_token_id": box_token_id,
            "box_type": box_type,
            "hash": tran["hash"],
            "hero_rarity": hero['rarity'],
            "hero_token_id": hero_token_id,
            "timestamp": tran["timeStamp"],
        }
        
        return model