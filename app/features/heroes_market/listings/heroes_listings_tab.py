from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, commify,
                        format_currency, format_percent,
                        format_template, is_busy, switch_case, format_age, navigate)
from ekp_sdk.util import collection, documents

from app.utils.game_constants import METABOMB_IMAGE_URL, MTB_ICON
from app.utils.image_cell import image_cell
from shared.constants import HERO_CONTRACT_ADDRESS


def heroes_listings_tab(LISTINGS_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs(
                [
                    "Browse the live Metabomb Marketplace for the best deals.",
                    "The heroes with the best Return on Investment are shown at the top.",
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
        default_sort_field_id="est_roi",
        default_sort_asc=False,
        on_row_clicked=navigate(
            format_template("https://market.metabomb.io/hero/{{ token_id }}", {
                "token_id": "$.tokenId"
            }),
            True,
            True
        ),
        pagination_per_page=18,
        disable_list_view=True,
        search_hint="Search by token id or token name...",
        filters=[
            {"columnId": "rarity_name", "icon": "cil-spa"},
            {"columnId": "hero_power", "icon": "cil-fire"},
            {"columnId": "hero_stamina", "icon": "cil-bolt"},
            {"columnId": "hero_class_capital", "icon": "cil-shield-alt", "imageMap": __CLASS_IMAGE_MAP},
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
                min_width="250px"
            ),
            Column(
                id="est_payback",
                title="ROI",
                sortable=True,
                searchable=True,
                cell=earn_cell(),
                min_width="120px"
            ),
            Column(
                id="priceFiat",
                title="Cost",
                sortable=True,
                searchable=True,
                cell=cost_cell(),
                min_width="100px"
            ),
            Column(
                id="avgPriceFiat",
                title="Vs 24h Avg",
                width="120px",
                sortable=True,
                cell=__avg_price_cell
            ),
            Column(
                id="hero_class",
                title="Class",
                cell=class_image(),
                width="130px",
                sortable=True,
            ),
            Column(
                id="hero_power",
                title="Power",
                cell=set_image(icon_name='stats-power',
                               attr_name='hero_power'),
                width="80px",
                right=True,
                sortable=True,
            ),
            Column(
                id="hero_health",
                title="Health",
                cell=set_image(icon_name='stats-health',
                               attr_name='hero_health'),
                width="80px",
                right=True,
                sortable=True,
            ),
            Column(
                id="hero_speed",
                title="Speed",
                cell=set_image(icon_name='stats-speed',
                               attr_name='hero_speed'),
                width="80px",
                right=True,
                sortable=True,
            ),
            Column(
                id="hero_stamina",
                title="Stamina",
                cell=set_image(icon_name='stats-stamina',
                               attr_name='hero_stamina'),
                width="90px",
                right=True,
                sortable=True,
            ),
            Column(
                id="hero_bomb_num",
                title="Bomb num",
                cell=set_image(icon_name='stats-bombnum',
                               attr_name='hero_bomb_num'),
                width="80px",
                right=True,
                sortable=True,
            ),
            Column(
                id="hero_bomb_range",
                title="Bomb range",
                cell=set_image(icon_name='stats-bombrange',
                               attr_name='hero_bomb_range'),
                width="80px",
                right=True,
                sortable=True,
            ),
            Column(
                id="rarity_name",
                omit=True,
                title="Rarity"
            ),
            Column(
                id="hero_class_capital",
                omit=True,
                title="Class"
            ),
            Column(
                id="level",
                omit=True
            ),
            Column(
                id="spacer",
                title="",
                width="2px"
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
                ),
            ]
        ),
        Col(
            class_name="col-12 font-small-1",
            children=[
                Row([
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
        children=[
            Col(
                class_name="my-auto col-auto pr-0",
                children=[
                    Image(
                        src=format_template(METABOMB_IMAGE_URL + "/gifs/char-gif/{{ display_id }}.gif", {
                            "display_id": '$.display_id'
                        }),
                        style={"height": "38px"}
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
                                    Span("$.name")
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
                                    #             "contractAddress": HERO_CONTRACT_ADDRESS,
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
    switch_case("$.deal", {"no": "float-right text-success", "yes": "float-right text-danger"})
),


def set_image(icon_name, attr_name):
    return image_cell(
        f"{METABOMB_IMAGE_URL}/icons/stats-icon/{icon_name}.svg",
        f"$.{attr_name}",
        image_size="16px"
    )


def class_image():
    return image_cell(
        image=format_template(METABOMB_IMAGE_URL + "/icons/class-{{ hero_class }}.png", {
            "hero_class": '$.hero_class'
        }),
        content="$.hero_class_capital",
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
        # Col(
        #     class_name="my-auto col-auto pr-0",
        #     children=[
        #         Span(format_datetime("$.last_listing_timestamp"))
        #     ]
        # ),
    ])


__CLASS_IMAGE_MAP = {
    element.capitalize(): f"{METABOMB_IMAGE_URL}/icons/class-{element}.png" for element in
    ["warrior", "assassin", "mage", "support", "ranger"]
}
