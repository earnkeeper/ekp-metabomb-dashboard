from app.utils.game_constants import (MTB_ICON, METABOMB_IMAGE_URL)
from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, commify,
                        format_age, format_currency, format_mask_address,
                        format_template, is_busy)
from ekp_sdk.util import collection, documents

from shared.constants import HERO_CONTRACT_ADDRESS


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
                id="level",
                omit=True,
            ),
            Column(
                id="spacer",
                title="",
                width="2px"
            ),
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
                                    Link(
                                        class_name="font-small-1",
                                        href=format_template(
                                            "https://bscscan.com/token/{{ contractAddress }}?a={{ tokenId }}",
                                            {
                                                "contractAddress": HERO_CONTRACT_ADDRESS,
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
