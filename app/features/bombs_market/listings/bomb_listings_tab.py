from app.utils.game_constants import METABOMB_IMAGE_URL, MTB_ICON
from app.utils.image_cell import image_cell
from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, commify, format_age,
                        format_currency, format_percent,
                        format_template, is_busy, switch_case, navigate)
from ekp_sdk.util import collection, documents
from shared.constants import BOMB_CONTRACT_ADDRESS


def bomb_listings_tab(LISTINGS_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs(
                [
                    "Browse the live Metabomb Bomb Market for the best deals on bombs.",
                    "🤔 Bombs with skill 5 increase earning by 100%, look out for deals on these ones",
                ],
            ),
            Div([], "mb-3"),
            market_row(LISTINGS_COLLECTION_NAME),
        ]
    )


def market_row(LISTINGS_COLLECTION_NAME):
    return Datatable(
        data=documents(LISTINGS_COLLECTION_NAME),
        busy_when=is_busy(collection(LISTINGS_COLLECTION_NAME)),
        default_sort_asc=False,
        pagination_per_page=18,
        on_row_clicked=navigate(
            format_template("https://market.metabomb.io/bomb/{{ token_id }}", {
                "token_id": "$.tokenId"
            }),
            True,
            True
        ),
        disable_list_view=True,
        search_hint="Search by token id or token name...",
        filters=[
            {"columnId": "rarity_name", "icon": "cil-spa"},
            {"columnId": "skills", "icon": "cil-color-palette", "imageMap": __SKILL_IMAGE_MAP, "imageMapClassName": "image-cover"},
            {"columnId": "element_capital", "icon": "cil-leaf", "imageMap": __ELEMENT_IMAGE_MAP},
        ],
        columns=[
            Column(
                id="last_listing_timestamp",
                title="Listed",
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
                min_width="260px"
            ),
            Column(
                id="skills",
                title="Skills",
                cell=skills_cell(),
                min_width="200px"
            ),
            Column(
                id="priceFiat",
                title="Cost",
                sortable=True,
                searchable=True,
                cell=cost_cell(),
                right=True,
                min_width="100px"
            ),
            Column(
                id="avgPriceFiat",
                title="Vs 24h Avg",
                width="140px",
                sortable=True,
                right=True,
                cell=__avg_price_cell
            ),
            Column(
                id="rarity_name",
                omit=True,
                title="Rarity"
            ),
            Column(
                id="element_capital",
                title="Element",
                omit=True,
            ),
            Column(
                id="skills",
                omit=True,
                title="Skills"
            ),

            Column(
                id="spacer",
                title="",
                width="2px"
            )
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


def earn_cell():
    return Row(
        children=[
            Col(
                class_name="col-12",
                children=[
                    Span(
                        format_template(
                            "{{ est_payback }} days", {
                                "est_payback": "$.est_payback"
                            }
                        ),
                    )
                ]
            ),
            Col(
                class_name="col-12",
                children=[
                    Row([
                        Col(
                            "col-auto pr-0",
                            [
                                Image(
                                    src=MTB_ICON,
                                    style={
                                        "height": "10px",
                                        "marginRight": "3px",
                                        "marginTop": "-2px"
                                    }
                                )
                            ]
                        ),
                        Col(
                            "col-auto pl-0",
                            [
                                Span(
                                    format_template(
                                        "{{ mtb_per_day }} /day",
                                        {
                                            "mtb_per_day": commify("$.mtb_per_day")
                                        }
                                    ),
                                    "font-small-1 text-success"
                                )
                            ]
                        )
                    ])
                ]
            ),
        ]
    )


def cost_cell():
    return Row([
        Col(
            class_name="col-12",
            children=[
                Span(
                    format_currency("$.priceFiat", "$.fiatSymbol"),
                    "float-right"
                ),
            ]
        ),
        Col(
            class_name="col-12 font-small-1",
            children=[
                Row([
                    Col("", []),
                    Col(
                        class_name="col-auto pr-0 my-auto",
                        children=[
                            Image(
                                src=MTB_ICON,
                                style={
                                    "height": "10px",
                                    "marginRight": "3px",
                                    "marginTop": "-2px"
                                }
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


def name_cell():
    return Row(
        class_name="mt-1",
        children=[
            Col(
                class_name="my-auto col-auto px-0",
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
                "px-0",
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
                                                            METABOMB_IMAGE_URL +
                                                            "/icons/element-icon/{{ element }}.png",
                                                            {
                                                                "element": '$.element'
                                                            }),
                                                        style={
                                                            "height": "14px"}
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
                                    Span(content=format_template(
                                        "Token Id: {{ tokenId }}",
                                        {
                                            "tokenId": "$.tokenId"
                                        }
                                    ),
                                        class_name="font-small-1")
                                    # Link(
                                    #     class_name="font-small-1",
                                    #     href=format_template(
                                    #         "https://bscscan.com/token/{{ contractAddress }}?a={{ tokenId }}",
                                    #         {
                                    #             "contractAddress": BOMB_CONTRACT_ADDRESS,
                                    #             "tokenId": "$.tokenId"
                                    #         }
                                    #     ),
                                    #     external=True,
                                    #     content=format_template(
                                    #         "Token Id: {{ tokenId }}",
                                    #         {
                                    #             "tokenId": "$.tokenId"
                                    #         }
                                    #     ),
                                    # )
                                ]
                            )
                        ]
                    )

                ]
            )

        ]
    )


__avg_price_cell = Span(
    format_percent("$.pcAboveAvgFiat"),
    switch_case("$.deal", {"no": "float-right text-success",
                "yes": "float-right text-danger"})
),


def set_image(icon_name, attr_name):
    return image_cell(
        f"{METABOMB_IMAGE_URL}/icons/stats-icon/{icon_name}.svg",
        f"$.{attr_name}",
        image_size="16px"
    )


def image_text_cell(src, text):
    return Row([
        Col("col-auto my-auto", [
            Image(
                src=src,
                style={"width": "24px"}
            )
        ]),
        Col("pl-0 my-auto", [Span(text)])
    ])


def timestamp_cell():
    return Row([
        Col(
            class_name="my-auto col-auto pr-0",
            children=[
                Span(format_age("$.last_listing_timestamp"))
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