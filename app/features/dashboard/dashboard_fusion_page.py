from ekp_sdk.ui import (Col, Column, Container, Datatable, Div,
                        Icon, Row, Span, Hr,
                        format_currency, format_template, is_busy, switch_case, commify, Paragraphs)
from ekp_sdk.util import documents, collection


def fusion_table(FUSION_COLLECTION_NAME):
    return Container(
        children=[
            title_row(),
            Hr("mb-2"),
            Paragraphs(
                [
                    "Do you want a rare hero? Is it cheaper to create one using fusion or buy directly from the market?",
                    "Use the table below to decide."
                ],
            ),
            table_row(FUSION_COLLECTION_NAME)
        ]
    )


def title_row():
    return Row(
        children=[
            Col(
                children=[Icon("box")],
                class_name='col-auto pr-0'
            ),
            Col(
                children=[
                    Span("Fusion Cost Calculator", "font-medium-3")
                ]
            )
        ],
        class_name="mb-2"
    )


def table_row(FUSION_COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(FUSION_COLLECTION_NAME),
        busy_when=is_busy(collection(FUSION_COLLECTION_NAME)),
        show_export=False,
        show_last_updated=False,
        pagination=False,
        card=False,
        columns=[
            Column(
                id="target_name",
                width="130px",
                cell=target_cell(),
            ),
            Column(
                id="inputs",
                cell=materials_cell(),
                min_width="160px"
            ),
            Column(
                id="input_costs",
                title="Input costs",
                cell=input_costs(),
                right=True,
                width="160px"
            ),
            Column(
                id="fusion_fees",
                title="Fusion Fees",
                cell=fusion_fees(),
                right=True,
                width="160px"
            ),
            Column(
                id="total_costs",
                title="Fusion Cost",
                cell=total_costs(),
                right=True,
                width="160px"
            ),
            Column(
                id="market_value",
                title="Market Cost",
                cell=market_value(),
                right=True,
                width="160px"
            ),
            Column(
                id="spacer",
                title="",
                width="10px"
            )
        ]
    )


def target_cell():
    return Row(
        children=[
            Col(
                class_name="col-auto px-0",
                children=[
                    Div(
                        [],
                        style={
                            "backgroundColor": switch_case('$.target_name', {
                                'Rare': '#65F44E',
                                'Epic': '#C13EFA',
                                'Legend': '#FEFC01',
                                'Mythic': '#EB9A29',
                                'Meta': '#E8483A',
                            }),
                            "width": 6,
                            "height": '100%',
                            "marginRight": '0.6rem',
                        }
                    )
                ],
            ),
            Col(
                class_name="col-auto px-0",
                children=[
                    Span("$.target_name", "font-small-5 font-weight-bold")
                ],
            ),
        ],
        class_name="mx-0")


def materials_cell():
    return Row(
        children=[
            Col(
                class_name="col-12 font-small-5 font-weight-bold",
                children=[
                    Span(
                        format_template(
                            "2 x {{ input_hero_rarity }} @ Lv {{ inputs_required_level }}",
                            {
                                "input_hero_rarity": "$.input_hero_rarity",
                                "inputs_required_level": "$.inputs_required_level"
                            }
                        ))],
            ),
            Col(
                class_name="col-12 font-small-1",
                children=[
                    Span(
                        format_template(
                            "{{ inputs_count }} x {{ input_hero_rarity }} @ Lv 1",
                            {
                                "input_hero_rarity": "$.input_hero_rarity",
                                "inputs_count": "$.inputs_count"
                            }
                        ),
                    )
                ],

            ),
        ])


def input_costs():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.inputs_cost_fiat", "$.fiat_symbol"))
            ],
        ),
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_template(
                        "{{ inputs_count }} x {{ input_floor_price_fiat }}",
                        {
                            "inputs_count": "$.inputs_count",
                            "input_floor_price_fiat": format_currency(f"$.input_floor_price_fiat", "$.fiat_symbol")
                        }
                    ),
                    "float-right font-small-1"
                )
            ],
        )
    ])


def fusion_fees():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(format_currency("$.fusion_fees_fiat", "$.fiat_symbol"))
            ],
        ),
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_template(
                        "{{ fusion_fees_mtb }} MTB",
                        {
                            "fusion_fees_mtb": commify("$.fusion_fees_mtb"),
                        }
                    ),
                    "float-right font-small-1"
                )
            ],
        )
    ])


def total_costs():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_currency("$.total_cost_fiat", "$.fiat_symbol"),
                    format_template("text-{{ color }}", {
                        "color": "$.total_cost_color"
                    })
                )
            ],
        ),
    ])


def market_value():
    return Row([
        Col(
            class_name="col-12 text-right",
            children=[
                Span(
                    format_currency("$.market_value_fiat", "$.fiat_symbol"),
                    format_template("text-{{ color }}", {
                        "color": "$.market_value_color"
                    })
                )
            ],
        ),
    ])
