from app.features.inventory.player.box_tab import box_tab
from app.features.inventory.player.hero_tab import hero_tab
from app.features.inventory.player.bomb_tab import bomb_tab
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Tabs, Tab, count, sum, format_currency, Icon, \
    Link, format_template, Div, format_mask_address

from app.utils.summary_card import summary_card


def page(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME, BOMBS_COLLECTION_NAME):
    return Container(
        children=[
            Row(
                children=[
                    Col(
                        class_name='col-auto pr-0 my-auto',
                        children=[
                            Icon(
                                size="lg",
                                name="user"
                            )
                        ],
                    ),
                    Col(
                        class_name="my-auto",
                        children=[
                            Span("Inventory", "font-large-1")
                        ]
                    ),
                ],
            ),
            Div([], "mt-1"),
            Link(
                content=format_mask_address({
                    "method": "replace",
                    "params": ["$.shared.client.path", "inventory/", ""]
                }),
                class_name="d-block font-small-2",
                external_icon=True,
                external=True,
                href=format_template(
                    "https://bscscan.com/address/{{ address }}",
                    {
                        "address": {
                            "method": "replace",
                            "params": ["$.shared.client.path", "inventory/", ""]
                        }
                    }
                )
            ),
            Div([], "mt-1"),
            summary_row(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME, BOMBS_COLLECTION_NAME),
            Tabs(
                [
                    Tab(
                        label="Heroes",
                        children=[hero_tab(HEROES_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="Boxes",
                        children=[box_tab(BOXES_COLLECTION_NAME)]
                    ),
                    Tab(
                        label="Bombs",
                        children=[bomb_tab(BOMBS_COLLECTION_NAME)]
                    ),
                ]
            ),
            Div([], "mt-1"),
            Row(

                children=[
                    Col(
                        class_name="col-auto",
                        children=[Icon(name="cib-discord")],
                    ),
                    Col(
                        class_name="col-auto px-0",
                        children=[
                            Link(
                                content="Join us on discord.",
                                external=True,
                                href="https://discord.com/invite/RHnnWBAkes"
                            )],
                    ),
                    Col(
                        class_name="col-auto",
                        children=[Span(
                            "We research earning potential for games daily"
                        )],
                    ),

                ]
            ),
            Div([], "mt-3"),
        ],
    )


def summary_row(HEROES_COLLECTION_NAME, BOXES_COLLECTION_NAME, BOMBS_COLLECTION_NAME):
    return Container(
        children=[
            Row([
                Col(
                    "col-auto",
                    [
                        summary_card(
                            format_template("{{ hero_count }} Heroes", {
                                "hero_count": count(
                                    f"$.{HEROES_COLLECTION_NAME}.*"
                                )
                            }),
                            format_currency(
                                sum(
                                    f"$.{HEROES_COLLECTION_NAME}..price_fiat"
                                ),
                                f"$.{HEROES_COLLECTION_NAME}[0].fiat_symbol"
                            ),
                        ),
                    ]
                ),
                Col(
                    "col-auto",
                    [
                        summary_card(
                            format_template("{{ boxes_count }} Boxes", {
                                "boxes_count": count(
                                    f"$.{BOXES_COLLECTION_NAME}.*"
                                )
                            }),
                            format_currency(
                                sum(
                                    f"$.{BOXES_COLLECTION_NAME}..price_fiat"
                                ),
                                f"$.{BOXES_COLLECTION_NAME}[0].fiat_symbol"
                            ),
                        ),
                    ]
                ),
                Col(
                    "col-auto",
                    [
                        summary_card(
                            format_template("{{ bomb_count }} Bombs", {
                                "bomb_count": count(
                                    f"$.{BOMBS_COLLECTION_NAME}.*"
                                )
                            }),
                            format_currency(
                                sum(
                                    f"$.{BOMBS_COLLECTION_NAME}..price_fiat"
                                ),
                                f"$.{BOMBS_COLLECTION_NAME}[0].fiat_symbol"
                            ),
                        ),
                    ]
                ),
                Col(
                    "col-auto",
                    [
                        summary_card(
                            "Token Value",
                            format_template(
                                "{{ mtb_balance }} ({{ fiat_balance }} )",
                                {
                                    "mtb_balance": format_currency(
                                        f"$.{BOXES_COLLECTION_NAME}[0].balance_mtb"
                                    , ""),
                                    "fiat_balance": format_currency(
                                        f"$.{BOXES_COLLECTION_NAME}[0].balance_fiat"
                                    , "$.fiat_symbol"),
                                }
                            ),
                            # format_currency(
                            #     sum(
                            #         f"$.{BOMBS_COLLECTION_NAME}..price_fiat"
                            #     ),
                            #     f"$.{BOMBS_COLLECTION_NAME}[0].fiat_symbol"
                            # ),
                        ),
                    ]
                ),
            ])
        ]
    )
