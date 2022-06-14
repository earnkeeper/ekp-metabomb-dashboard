from app.features.dashboard.dash_bomb_sale_price_and_volume_page import bomb_form_row, bomb_chart_row
from app.features.dashboard.dash_hero_sale_price_and_volume_page import chart_row, form_row
from app.features.dashboard.dashboard_hero_profit_page import hero_dashboard_profit_calc_page
from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from app.utils.page_title import page_title
from ekp_sdk.ui import Card, Chart, Col, Container, Image, Row, Span, Div, Chart, commify, ekp_map, sort_by, json_array, \
    Hr, Alert, Icon, Paragraphs
from app.features.dashboard.dashboard_fusion_page import fusion_table


def page(OPENS_COLLECTION_NAME, FUSION_COLLECTION_NAME, HERO_DASH_PROFIT_COLLECTION_NAME, CHART_COLLECTION_NAME,
         RARITIES_FORM_NAME, BOMB_RARITIES_FORM_NAME, BOMB_CHART_COLLECTION_NAME):
    return Container(
        children=[
            Div([], "mb-4"),
            page_title('activity', 'Dashboard'),
            Div(class_name="my-4"),
            hero_sales_volume_chart(RARITIES_FORM_NAME, CHART_COLLECTION_NAME),
            Div(class_name="my-4"),
            bomb_sales_volume_chart(BOMB_RARITIES_FORM_NAME, BOMB_CHART_COLLECTION_NAME),
            Div(class_name="my-4"),
            hero_dashboard_profit_calc_page(HERO_DASH_PROFIT_COLLECTION_NAME),
            Div(class_name="my-4"),
            fusion_table(FUSION_COLLECTION_NAME),
            Div(class_name="my-4"),
            hero_drop_rates(OPENS_COLLECTION_NAME),
        ]
    )


def bomb_sales_volume_chart(BOMB_RARITIES_FORM_NAME, BOMB_CHART_COLLECTION_NAME):
    return Div(
        children=[
            title_row("Bomb"),
            Hr("mb-2"),
            Paragraphs(
                [
                    "Check the history of price and number of sales of each bomb rarity on the market. Is now a good time to buy or sell?"
                ],
            ),
            Div(class_name="mt-2"),
            Card(
                children=[
                    bomb_form_row(BOMB_RARITIES_FORM_NAME, BOMB_CHART_COLLECTION_NAME),
                    bomb_chart_row(BOMB_CHART_COLLECTION_NAME),
                ],
            )
        ]
    )


def hero_sales_volume_chart(RARITIES_FORM_NAME, CHART_COLLECTION_NAME):
    return Div(
        children=[
            title_row("Hero"),
            Hr("mb-2"),
            Paragraphs(
                [
                    "Check the history of price and number of sales of each hero rarity on the market. Is now a good time to buy or sell?"
                ],
            ),
            Div(class_name="mt-2"),
            Card(
                children=[
                    form_row(RARITIES_FORM_NAME, CHART_COLLECTION_NAME),
                    chart_row(CHART_COLLECTION_NAME),
                ],
            )
        ]
    )


def title_row(nft_type):
    return Row(
        children=[
            Col(
                children=[Icon("box")],
                class_name='col-auto pr-0'
            ),
            Col(
                children=[
                    Span(f"{nft_type} Price History", "font-medium-3")
                ]
            )
        ],
        class_name="mb-2"
    )


def hero_drop_rates(OPENS_COLLECTION_NAME):
    return Div([
        Span('Actual Hero Drop Rates', 'font-medium-4 font-weight-bold'),
        Hr("mb-2"),
        Span('We scan the binance smart chain in real time, to give you the real hero drop rates as boxes are opened.',
             "d-block mb-2 mt-1"),
        Row([
            Col("col-12 col-md-6", [
                opens_chart_row(
                    OPENS_COLLECTION_NAME,
                    0,
                    "Common Box"
                ),
            ]),
            Col("col-12 col-md-6", [
                opens_chart_row(
                    OPENS_COLLECTION_NAME,
                    1,
                    "Premium Box"
                ),
            ]),
            Col("col-12 col-md-6", [
                opens_chart_row(
                    OPENS_COLLECTION_NAME,
                    2,
                    "Ultra Box"
                ),
            ])
        ])
    ])


def opens_chart_row(OPENS_COLLECTION_NAME, doc_index, box_type):
    return Card(
        [
            Row(
                class_name="mx-1 my-2",
                children=[
                    Col(
                        "col-auto my-auto pr-0", [
                            Image(
                                src=HERO_BOX_NAME_IMAGE[box_type],
                                style={"height": "32px"}
                            )
                        ]
                    ),
                    Col(
                        "col-auto my-auto", [
                            Span(box_type, "font-medium-3 font-weight-bold")
                        ]
                    ),

                ]
            ),
            Chart(
                data=f"$.{OPENS_COLLECTION_NAME}[{doc_index}]",
                type="sankey",
                card=False,
                class_name="mx-2 my-0",
                height=300
            )

        ]
    )
