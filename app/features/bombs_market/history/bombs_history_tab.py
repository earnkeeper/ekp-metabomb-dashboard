from app.utils.game_constants import (MTB_ICON, METABOMB_IMAGE_URL)
from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, commify,
                        format_age, format_currency, format_mask_address,
                        format_template, is_busy)
from ekp_sdk.util import documents, collection

from shared.constants import BOMB_CONTRACT_ADDRESS


def history_tab(HISTORY_COLLECTION_NAME):
    return Container([
        Paragraphs(["Browse the last 1000 sales from the market place right here.",
                    "Check out our discord for real time notifications of new listings"]),
        Div([], class_name="mb-2"),
        table_row(HISTORY_COLLECTION_NAME)
    ])


def table_row(HISTORY_COLLECTION_NAME):
    return Datatable(
        data=documents(HISTORY_COLLECTION_NAME),
        busy_when=is_busy(collection(HISTORY_COLLECTION_NAME)),
        default_sort_field_id="timestamp",
        default_sort_asc=False,
        filters=[
            {"columnId": "rarity", "icon": "cil-spa"},
            {"columnId": "skills", "icon": "cil-color-palette", "imageMap": __SKILL_IMAGE_MAP,
             "imageMapClassName": "image-cover"},
            {"columnId": "element_name_capital", "icon": "cil-leaf", "imageMap": __ELEMENT_IMAGE_MAP},
        ],
        columns=[
            Column(
                id="timestamp",
                sortable=True,
                cell=timestamp_cell(),
                width="120px"
            ),
            Column(
                id="item",
                value="$.name",
                title="Item",
                sortable=True,
                searchable=True,
                cell=name_cell(),
                min_width="200px"
            ),
            Column(
                id="skills",
                title="Skills",
                cell=skills_cell(),
                min_width="200px"
            ),
            Column(
                id="price",
                sortable=True,
                right=True,
                cell=price_cell()
            ),
            Column(
                id="type",
                omit=True,
                format=format_currency("$.priceFiat", "$.fiatSymbol")
            ),
            Column(
                id="rarity",
                omit=True,
            ),
            Column(
                id="skills",
                omit=True,
                title="Skills"
            ),
            Column(
                id="element_name",
                omit=True,
            ),
            Column(
                id="element_name_capital",
                title="Element",
                omit=True,
            ),

            Column(
                id="spacer",
                title="",
                width="2px"
            ),
        ]
    )


def skills_cell():
    return Row(
        children=[
            skill_col(s_id) for s_id in range(1, 7)
        ]
    )


def skill_col(skill_id):
    return Col(
        class_name="my-auto col-auto pr-0",
        children=[
            Image(
                src=format_template(METABOMB_IMAGE_URL + "/icons/skill-icon/skill-{{ skill_id }}.png", {
                    "skill_id": f"$.skill_{skill_id}['skill']"
                }),
                style={"height": "20px", "border-radius": "50%"},
                when=f"$.skill_{skill_id}['skill']",
                tooltip=f"$.skill_{skill_id}['tooltip']",
            )
        ]
    )


def timestamp_cell():
    return Row([
        Col(
            class_name="col-12",
            children=[
                Span(format_age("$.timestamp"))
            ]
        ),
        Col(
            class_name="col-12",
            children=[
                Link(
                    class_name="font-small-1",
                    href=format_template(
                        "https://bscscan.com/tx/{{ hash }}", {"hash": "$.hash"}),
                    external=True,
                    content=format_mask_address("$.hash")
                )
            ]
        )
    ])


def name_cell():
    return Row(
        children=[
            Col(
                class_name="my-auto col-auto pr-0",
                children=[
                    Image(
                        src=format_template(METABOMB_IMAGE_URL + "/gifs/bomb-gif/{{ display_id }}.gif", {
                            "display_id": '$.display_id'
                        }),
                        style={"height": "50px"}
                    )
                ]
            ),
            Col(
                children=[
                    Row(
                        children=[
                            Col(
                                class_name="col-12 font-small-4",
                                children=[
                                    Row(
                                        children=[
                                            Col(
                                                class_name="col-auto my-auto pr-0",
                                                children=[
                                                    Span("$.name")
                                                ]
                                            ),
                                            Col(
                                                class_name="col-auto my-auto",
                                                children=[
                                                    Image(
                                                        src=format_template(
                                                            METABOMB_IMAGE_URL + "/icons/element-icon/{{ element }}.png",
                                                            {
                                                                "element": '$.element_name'
                                                            }),
                                                        style={"height": "14px"}
                                                    )
                                                ]
                                            )

                                        ]
                                    )
                                ]
                            ),
                            Col(
                                class_name="col-12",
                                children=[
                                    Link(
                                        class_name="font-small-1",
                                        href=format_template(
                                            "https://bscscan.com/token/{{ contractAddress }}?a={{ tokenId }}",
                                            {
                                                "contractAddress": BOMB_CONTRACT_ADDRESS,
                                                "tokenId": "$.tokenId"
                                            }
                                        ),
                                        external=True,
                                        content=format_template(
                                            "Token Id: {{ tokenId }}",
                                            {
                                                "tokenId": "$.tokenId"
                                            }
                                        ),
                                    )
                                ]
                            )
                        ]
                    )

                ]
            )

        ]
    )


def price_cell():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.priceFiat", "$.fiatSymbol"))
            ]
        ),
        Col(
            class_name="col-12 text-right font-small-1",
            children=[
                Row([
                    Col(),
                    Col(
                        class_name="col-auto p-0 my-auto",
                        children=[
                            Image(
                                src=MTB_ICON,
                                style={"height": "10px",
                                       "marginRight": "3px", "marginTop": "-2px"}
                            )
                        ]
                    ),
                    Col(
                        class_name="col-auto pl-0 my-auto text-success",
                        children=[
                            Span(commify("$.price"))
                        ]
                    )
                ])

            ]
        ),
    ])


__SKILL_IMAGE_MAP = {
    "1. Diam. Chest +2": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-1.png",
    "2. Meta Chest +5": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-2.png",
    "3. Dmg Thru Blocks": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-3.png",
    "4. Free Bomb +20%": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-4.png",
    "5. Mana/Min +0.5": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-5.png",
    "6. Walk Thru Blocks": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-6.png",
    "7. Walk Thru Bombs": f"{METABOMB_IMAGE_URL}/icons/skill-icon/skill-7.png",
}

__ELEMENT_IMAGE_MAP = {
    element.capitalize(): f"{METABOMB_IMAGE_URL}/icons/element-icon/{element}.png" for element in
    ["earth", "fire", "thunder", "water", "wood"]
}
