from ekp_sdk.services import ClientService
from ekp_sdk.util import client_currency, client_path, form_values

from app.features.inventory.players.players_service import InventoryPlayersService
from app.features.inventory.players.players_page import players_page

INVENTORY_PLAYERS_COLLECTION_NAME = "metabomb_inventory_players"
INVENTORY_PLAYERS_FORM_NAME = "metabomb_inventory_players"


class InventoryPlayersController:
    def __init__(
        self,
        client_service: ClientService,
        inventory_players_service: InventoryPlayersService,
    ):
        self.client_service = client_service
        self.inventory_players_service = inventory_players_service
        self.path = 'players'

    async def on_connect(self, sid):
        await self.client_service.emit_menu(
            sid,
            'clipboard',
            'Inventory',
            self.path,
            order=500,
            id="metabomb_inventory",
            short_link="mtb-inventory"
        )
        await self.client_service.emit_page(
            sid,
            self.path,
            players_page(INVENTORY_PLAYERS_COLLECTION_NAME, INVENTORY_PLAYERS_FORM_NAME),
        )

    async def on_client_state_changed(self, sid, event):

        path = client_path(event)

        if (path != self.path):
            return

        await self.client_service.emit_busy(sid, INVENTORY_PLAYERS_COLLECTION_NAME)

        currency = client_currency(event)

        address_form_values = form_values(event, INVENTORY_PLAYERS_FORM_NAME)
        
        inventory_documents = await self.inventory_players_service.get_documents(currency, address_form_values or [])

        await self.client_service.emit_documents(
            sid,
            INVENTORY_PLAYERS_COLLECTION_NAME,
            inventory_documents
        )

        await self.client_service.emit_done(sid, INVENTORY_PLAYERS_COLLECTION_NAME)
