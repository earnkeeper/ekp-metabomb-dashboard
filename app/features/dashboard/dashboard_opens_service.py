from datetime import datetime

from app.utils.game_constants import rarity_names
from db.box_opens_repo import BoxOpensRepo


class DashboardOpensService:
    def __init__(
        self,
        box_opens_repo: BoxOpensRepo,
    ):
        self.box_opens_repo = box_opens_repo

    def get_document(self, box_type, opens, now, rarities):
        root_index = len(rarities)

        nodes = []
        links = []

        names = rarity_names()

        i = 0

        for rarity in rarities:
            nodes.append({"name": names[rarity], "value": 0})
            links.append({"source": root_index, "target": i, "value": 0})
            i += 1

        nodes.append({"name": f"Opened", "value": 0, "color": "yellow"}),

        for open in opens:
            if open["box_type"] != box_type:
                continue

            nodes[root_index]["value"] += 1
            i = rarities.index(open["hero_rarity"])
            nodes[i]["value"] += 1
            links[i]["value"] += 1

        for i in range(root_index):
            total = nodes[i]["value"]
            pc = round(
                nodes[i]["value"] * 100 / nodes[root_index]["value"], 2
            )
            nodes[i]["value"] = pc
            nodes[i]["name"] = f'{format(total, ",d")} x {nodes[i]["name"]} ({pc}%)'

        total = nodes[root_index]["value"]
        nodes[root_index]["name"] = f'{format(total, ",d")} {nodes[root_index]["name"]}'

        doc = {
            "id": box_type,
            "updated": now,
            "nodes": nodes,
            "links": links
        }

        return doc

    async def get_documents(self):
        opens = self.box_opens_repo.find_since_block_number(0, 10000)
        now = datetime.now().timestamp()
        return [
            self.get_document("Common Box", opens, now, [0, 1, 2]),
            self.get_document("Premium Box", opens, now, [0, 1, 2, 3]),
            self.get_document("Ultra Box", opens, now, [1, 2, 3, 4]),
        ]
