from ekp_sdk.ui import (Button, Chart, Col, Div, Form, Row, Select, commify,
                        ekp_map, format_currency, is_busy,
                        json_array, sort_by)
from ekp_sdk.util import documents

def form_row(RARITIES_FORM_NAME, CHART_COLLECTION_NAME):
    return Div(
        class_name="pt-1 pl-3",
        children=[
            Form(
                name=RARITIES_FORM_NAME,
                schema={
                    "type": "object",
                    "properties": {
                        "rarity": "string",
                        "currency": "string"
                    },
                    "default": {
                        "rarity": "Common",
                        "currency": "MTB"
                    }
                },
                children=[
                    Row([
                        Col(
                            "col-auto my-auto",
                            [
                                Select(
                                    label="Hero Rarity",
                                    name="rarity",
                                    options=["Common", "Rare",
                                             "Epic", "Legend"],
                                    min_width="120px"
                                ),
                            ],

                        ),
                        Col(
                            "col-auto my-auto",
                            [
                                Select(
                                    label="Currency",
                                    name="currency",
                                    options=["MTB", "Fiat"],
                                    min_width="120px"
                                ),
                            ],

                        ),
                        Col(
                            "col-auto my-auto",
                            [
                                Button(label="Update", is_submit=True,
                                       busy_when=is_busy(CHART_COLLECTION_NAME))
                            ]
                        )
                    ])

                ]
            )
        ]
    )


def chart_row(CHART_COLLECTION_NAME):
    return Chart(
        title="",
        height=350,
        type="line",
        card=False,
        data=documents(CHART_COLLECTION_NAME),
        options={
            "chart": {
                "zoom": {
                    "enabled": False,
                },
                "toolbar": {
                    "show": False,
                },
                "type": "line"
            },
            "xaxis": {
                "type": "datetime",
            },
            "yaxis": [
                {
                    "title": {
                        "text": "Sales Count"
                    },
                    "labels": {
                        "formatter": commify("$")
                    },
                },
                {
                    "title": {
                        "text": "Avg Price"
                    },
                    "labels": {
                        "formatter": commify("$")
                    },
                    "opposite": True,
                },
            ],
            "labels": ekp_map(
                sort_by(
                    json_array(
                        documents(CHART_COLLECTION_NAME)
                    ),
                    "$.timestamp_ms"
                ), "$.timestamp_ms"
            ),
            "stroke": {
                "width": [0, 8],
            },
            "legend": {
                "show": False
            }
        },
        series=[
            {
                "name": "Sales Count",
                "type": "column",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestamp_ms"),
                    "$.number_of_sales"
                )
            },
            {
                "name": "Avg Price",
                "type": "line",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestamp_ms"
                    ),
                    "$.price_avg"
                ),
            },
        ],

    )
