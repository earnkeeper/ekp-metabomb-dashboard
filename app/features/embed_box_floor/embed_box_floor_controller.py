from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency
from app.features.boxes_market.listings.boxes_listings_service import BoxesListingsService
from app.features.boxes_market.history.boxes_history_service import BoxesHistoryService
from app.features.embed_box_floor.embed_box_floor_service import EmbedBoxesService
from app.features.embed_box_floor.embed_box_floor_tile import tile

OPENS_COLLECTION_NAME = "metabomb_dashboard_opens"
ACTIVITY_COLLECTION_NAME = "metabomb_dashboard_activity"

class EmbedBoxFloorController:
    def __init__(
        self,
        client_service: ClientService,
        embed_boxes_service: EmbedBoxesService,
        boxes_history_service: BoxesHistoryService,
        boxes_listings_service: BoxesListingsService
    ):
        self.client_service = client_service
        self.embed_boxes_service = embed_boxes_service
        self.boxes_history_service = boxes_history_service
        self.boxes_listings_service = boxes_listings_service

    async def on_connect(self, sid):
        pass


    async def on_client_state_changed(self, sid, event):

        currency = client_currency(event)

        history_documents = await self.boxes_history_service.get_documents(currency)

        listing_documents = await self.boxes_listings_service.get_documents(currency, history_documents)
        embed_boxes_documents = self.embed_boxes_service.get_documents(listing_documents, history_documents, currency)


        documents = [{
            "id": 'metabomb-box-tile',
            "size": 'tile',
            "element": tile(),
            "data": embed_boxes_documents,
            "page": 'boxes',
        }]
        
        await self.client_service.emit_documents(
            sid,
            "embeds",
            documents,
            layer_id='metabomb-box-tile'            
        )
        
