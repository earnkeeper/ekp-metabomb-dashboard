import asyncio
from pprint import pprint

from decouple import AutoConfig
from ekp_sdk import BaseContainer

from shared.metabomb_api_service import MetabombApiService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig(".env")

        super().__init__(config)

        self.metabomb_api_service = MetabombApiService(
            cache_service=self.cache_service
        )


async def main(container: AppContainer):
    heroes = await container.metabomb_api_service.get_market_heroes()
    pprint(heroes)

if __name__ == '__main__':
    container = AppContainer()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        main(container)
    )
