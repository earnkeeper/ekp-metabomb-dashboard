from app.utils.game_constants import (HERO_BOX_NAME_CONTRACT,
                                      HERO_BOX_NAME_IMAGE, MTB_ICON)
from ekp_sdk.util import collection, documents
from ekp_sdk.ui import (Col, Column, Container, Datatable, Div, Image, Link,
                        Paragraphs, Row, Span, commify,
                        format_currency, format_mask_address, format_percent,
                        format_template, is_busy, switch_case, format_age)
from ekp_sdk.util import documents, collection


def listings_tab(LISTINGS_COLLECTION_NAME):
    return Container(
        children=[
            Paragraphs(
                [
                    "The live Metabomb marketplace! Think it looks the same as the offical one, look again 👀",
                    "Compare every price to the 24 hour average and check prices in your currency (select at top of page)",
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
        default_sort_field_id="timestamp",
        pagination_per_page=18,
        disable_list_view=True,
        search_hint="Search by token id or box name...",
        filters=[
            {"columnId": "item", "icon": "cil-spa"},
        ],
        columns=[
            Column(
                id="last_listing_timestamp",
                title="Listed",
                sortable=True,
                format=format_age("$.last_listing_timestamp"),
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
                id="avgPriceFiat",
                title="Vs 24h Avg",
                width="120px",
                sortable=True,
                right=True,
                cell=__avg_price_cell
            ),
            Column(
                id="type",
                omit=True,
                format=format_currency("$.priceFiat", "$.fiatSymbol")
            ),
            Column(
                id="spacer",
                title="",
                width="2px"
            ),
        ]
    )


__avg_price_cell = Span(
    format_percent("$.pcAboveAvgFiat"),
    switch_case("$.deal", {"no": "float-right text-success", "yes": "float-right text-danger"})
),


def image_text_cell(src, text):
    return Row([
        Col("col-auto my-auto", [
            Image(
                src=src,
                style={"height": "20px"}
            )
        ]),
        Col("pl-0 my-auto", [Span(text)])
    ])

def name_cell():
    return Row(
        children=[
            Col(
                class_name="my-auto col-auto pr-0",
                children=[
                    Image(
                        src=switch_case("$.name", HERO_BOX_NAME_IMAGE),
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
                                                "contractAddress": switch_case("$.name", HERO_BOX_NAME_CONTRACT),
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