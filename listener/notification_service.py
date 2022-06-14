from ekp_sdk.services import RestClient
from shared.domain.hero import Hero
from shared.domain.hero_box import HeroBox
from shared.domain.market_listing import MarketListing
from shared.mapper_service import MapperService


class NotificationService:
    def __init__(
        self,
        rest_client: RestClient,
        mapper_service: MapperService,
        discord_base_url,
        discord_channel_id
    ):
        self.rest_client = rest_client
        self.discord_base_url = discord_base_url
        self.discord_channel_id = discord_channel_id
        self.mapper_service = mapper_service

    async def send_notification(
        self,
        new_listing: MarketListing,
        floor_listing: MarketListing
    ):

        fields = [
            {
                "name": "Token Id",
                "value": str(new_listing["token_id"]),
                "inline": True
            },
            {
                "name": "MTB",
                "value": format(int(new_listing["price_mtb"]), ",d"),
                "inline": True
            },
            {
                "name": "USD",
                "value": f'$ {format(round(new_listing["price_usdc"],2))}',
                "inline": True
            },
        ]

        name = "Unknown NFT"
        image_url = None
        title_url = ""

        if new_listing["hero"] is not None:
            hero: Hero = new_listing["hero"]
            name = f"{hero['rarity_name']} Lv {hero['level'] + 1} Hero"
            image_url = self.mapper_service.get_hero_image_url(hero["display_id"])
            title_url = f"https://market.metabomb.io/hero/{hero['id']}"

            fields.append({
                "name": "Power",
                "value": str(hero["power"]),
                "inline": True
            })
            fields.append({
                "name": "Health",
                "value": str(hero["health"]),
                "inline": True
            })
            fields.append({
                "name": "Speed",
                "value": str(hero["speed"]),
                "inline": True
            })
            fields.append({
                "name": "Stamina",
                "value": str(hero["stamina"]),
                "inline": True
            })
            fields.append({
                "name": "Bomb num",
                "value": str(hero["bomb_num"]),
                "inline": True
            })
            fields.append({
                "name": "Bomb range",
                "value": str(hero["bomb_range"]),
                "inline": True
            })

            fields.append({
                "name": "Class",
                "value": hero["hero_class_name"],
                "inline": True
            })
            
        if new_listing["box"] is not None:
            box: HeroBox = new_listing["box"]
            name = box["name"]
            image_url = self.mapper_service.get_hero_box_url(box["type"])
            title_url = "https://market.metabomb.io/trade/boxes"
            
            fields.append({
                "name": "Type",
                "value": box["name"],
                "inline": True
            })

        if floor_listing is not None:
            fields.append({
                "name": "Floor MTB",
                "value": f'{format(int(floor_listing["price_mtb"]), ",")}',
                "inline": True
            })
            fields.append({
                "name": "Floor USD",
                "value": f'$ {format(round(floor_listing["price_usdc"],2), ",")}',
                "inline": True
            })

        seller = new_listing["seller"]
        
        masked_seller = f"{seller[0:5]}...{seller[-3:]}"

        embed = {
            "type": "rich",
            "title": "Metabomb Floor Alert!",
            "description": f'**{masked_seller}** has listed a **{name}** at lower than floor price!\n\n{title_url}\n\n👀\n\n',
            "url": "https://earnkeeper.io/game/metabomb/marketplace",
            "color": 16215296,
            "image": {"url": image_url},
            "fields": fields,
            "footer": {
                "text": 'Brought to you by EarnKeeper.io, the leading P2E Analytics platform',
                "icon_url": "https://earnkeeper.io/logos/earnkeeper_logo.png"
            }
        }

        await self.rest_client.post(
            f"{self.discord_base_url}/message/{self.discord_channel_id}",
            {"embeds": [embed]}
        )
