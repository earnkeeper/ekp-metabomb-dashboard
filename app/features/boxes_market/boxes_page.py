from app.features.boxes_market.history.boxes_history_tab import history_tab
from app.features.boxes_market.listings.boxes_listings_tab import listings_tab
from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import (Card, Col, Container, Div, Image, Row, Span, Tab, Tabs,
                        format_currency, format_template, switch_case, Alert)


def boxes_page(LISTINGS_COLLECTION_NAME, HISTORY_COLLECTION_NAME, SUMMARY_COLLECTION_NAME):
    return Container(
        children=[
            Div([], "mb-4"),
            page_title('shopping-bag', 'Box Market'),
            summary_row(SUMMARY_COLLECTION_NAME),
            Tabs(
                [
                    Tab(
                        label="Listings",
                        children=[listings_tab(LISTINGS_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="History",
                        children=[history_tab(HISTORY_COLLECTION_NAME)]
                    ),
                ]
            ),
        ]
    )


def summary_row(SUMMARY_COLLECTION_NAME):
    return Container(
        context=f"$.{SUMMARY_COLLECTION_NAME}[0]",
        children=[
            Row([
                Col("col-auto", [
                    summary_card("common"),
                ]),
                Col("col-auto", [
                    summary_card("premium"),
                ]),
                Col("col-auto", [
                    summary_card("ultra"),
                ]),
                Col("col-auto", [
                    summary_card("bomb"),
                ])
            ])
        ]
    )


def summary_card(boxId):
    return Container(
        context=f"$.{boxId}",
        children=[
            Div(
                children=[
                    Card(
                        class_name="p-1",
                        children=[
                            Row([
                                Col("col-auto", [
                                    Image(
                                        src=switch_case("$.name", HERO_BOX_NAME_IMAGE),
                                        style={"height": "64px"}
                                    )
                                ]),
                                Col("col-auto pr-4", [
                                    Span("$.name", "font-medium-3 font-weight-bold d-block"),
                                    Span(
                                        content=format_template(
                                            "Floor Price: {{ price }}",
                                            {
                                                "price": format_currency("$.floorPrice", "$.fiatSymbol")
                                            }
                                        ),
                                        class_name="font-small-2 d-block"
                                    ),
                                    Div(style={"marginBottom": "2px"}),
                                    Span(
                                        content=format_template(
                                            "24h Avg Price: {{ price }}",
                                            {
                                                "price": format_currency("$.avgPrice", "$.fiatSymbol")
                                            }
                                        ),
                                        class_name="font-small-2 d-block"
                                    )
                                ]),

                            ])
                        ]),
                ],
                when="$.name"
            )
        ]
    )
