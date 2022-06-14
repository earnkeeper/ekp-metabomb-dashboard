from ekp_sdk.ui import (Card, Col, Column, Container, Datatable, Div, Hr, Icon,
                        Link, Paragraphs, Row, Span, commify, format_currency,
                        format_template, switch_case)


def hero_dashboard_profit_calc_page(HERO_DASH_PROFIT_COLLECTION_NAME):
    return Container(
        children=[
            title_row(),
            Hr("mb-2"),            
            Span("Use the table below to calculate how much MTB your heroes will earn each day.", "d-block"),
            Div(style={"marginTop": "8px"}),
            Span("Want to automatically calculate earning for the heroes you own? Try our "),
            Link(content="Inventory", href="players"),
            Span(" page."),
            Div(style={"marginTop": "24px"}),
            Row([
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        0,
                        "Common"
                    ),
                ]),
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        1,
                        "Rare"
                    ),
                ]),
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        2,
                        "Epic"
                    ),
                ]),
                Col("col-12 col-md-6", [
                    table_row(
                        HERO_DASH_PROFIT_COLLECTION_NAME,
                        3,
                        "Legend"
                    ),
                ]),
            ]),
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
                    Span("Hero Profit Calculator", "font-medium-3")
                ]
            )
        ],
        class_name="mb-2"
    )


def table_row(HERO_DASH_PROFIT_COLLECTION_NAME, doc_index, hero_type):
    return Card(
        [
            Row(
                class_name="mx-1 mt-1",
                children=[

                    Col(
                        class_name="col-auto px-0",
                        children=[
                            Div(
                                [],
                                style={
                                    "backgroundColor": switch_case(hero_type, {
                                        'Common': "#D1CCCC",
                                        'Rare': '#65F44E',
                                        'Epic': '#C13EFA',
                                        'Legend': '#FEFC01',
                                    }),
                                    "width": 6,
                                    "height": '100%',
                                    "marginRight": '0.6rem',
                                }
                            ),
                        ],
                    ),
                    Col(
                        "col-auto my-auto", [
                            Span(format_template("{{ hero_type }} Hero",
                                                 {"hero_type": hero_type}), "font-medium-3 font-weight-bold")
                        ]
                    ),

                ]
            ),
            Datatable(
                card=False,
                class_name="mt-1",
                data=f"$.{HERO_DASH_PROFIT_COLLECTION_NAME}[{doc_index}].*",
                show_export=False,
                show_last_updated=False,
                pagination=False,
                columns=[
                    Column(
                        id="power",
                        value="$.power",
                        width="100px",
                    ),
                    Column(
                        id="market_value",
                        cell=Div([
                            Div(
                                when="$.market_value",
                                children=[
                                    Span(
                                        format_currency(
                                            "$.market_value",
                                            "$.fiat_symbol"
                                        ),
                                    )
                                ]
                            ),
                            Div(
                                when={"not": "$.market_value"},
                                children=[
                                    Span("?")
                                ]
                            )
                        ])
                    ),
                    Column(
                        id="mtb_per_day",
                        value=commify("$.mtb_per_day"),
                    ),
                    Column(
                        id="roi",
                        cell=Div([
                            Div(
                                when="$.roi",
                                children=[
                                    Span(
                                        format_template(
                                            "{{ roi }} days",
                                            {"roi": "$.roi"}
                                        ),
                                    )
                                ]
                            ),
                            Div(
                                when={"not": "$.market_value"},
                                children=[
                                    Span("?")
                                ]
                            )
                        ])
                    ),
                ]
            ),
            Div(style={"height": "4px"})

        ]
    )
