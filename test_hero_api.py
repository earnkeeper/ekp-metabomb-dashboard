
import asyncio

from decouple import AutoConfig
from ekp_sdk import BaseContainer
from shared.metabomb_api_service import MetabombApiService


class AppContainer(BaseContainer):
    def __init__(self):
        config = AutoConfig('.env')

        super().__init__(config)

        self.metabomb_api_service = MetabombApiService(
            coingecko_service=self.coingecko_service
        )


if __name__ == '__main__':
    container = AppContainer()

    print("🚀 Application Start")

    async def test():
        listings = await container.metabomb_api_service.get_market_heroes()
        print(len(listings))

    asyncio.run(test())
