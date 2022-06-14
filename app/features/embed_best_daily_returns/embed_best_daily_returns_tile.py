from ekp_sdk.ui import (Col, Container, Div, Image, Row, Span, format_currency,
                        format_percent, format_template)

from app.utils.game_constants import METABOMB_IMAGE_URL


def tile():
    return Container(
        children=[
            Span("Best Daily Returns", "font-medium-2"),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell(0),
                    hero_token_id(0),
                    hero_cost(0),
                    hero_daily_return(0)
                ]
            ),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell(1),
                    hero_token_id(1),
                    hero_cost(1),
                    hero_daily_return(1)
                ]
            ),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell(2),
                    hero_token_id(2),
                    hero_cost(2),
                    hero_daily_return(2)
                ]
            )
        ]
    )

# def row_cell(row_index):
#     Div(class_name="mb-1"),
#     Row(
#         children=[
#             image_cell(row_index),
#             hero_token_id(row_index),
#             hero_cost(row_index),
#             hero_daily_return(row_index)
#         ]
#     ),


def image_cell(row_index):
    return Col("col-auto pr-0 my-auto", [
        Image(
            src=format_template(METABOMB_IMAGE_URL + "/gifs/char-gif/{{ display_id }}.gif", {
                "display_id": f"$.data[{row_index}].display_id"
            }),
            style={"height": "32px"}
        )
    ])


def hero_token_id(row_index):
    return Col(
        children=[
            Span(
                class_name='d-block font-small-1',
                content=format_template(
                    "#{{ token_id }}",
                    {
                        "token_id": f"$.data[{row_index}].token_id"
                    }
                )
            ),
            Span(
                class_name='d-block font-small-3',
                content=f"$.data[{row_index}].hero_rarity"
            ),
        ]
    )


def hero_cost(row_index):
    return Col(
        class_name='col-auto',
        children=[
            Span(
                class_name='d-block text-right font-small-1 text-{{ color }}',
                content='Cost'
                ),
            Span(
                class_name='d-block font-small-3',
                content=format_currency(f"$.data[{row_index}].cost", f"$.data[{row_index}].fiatSymbol")
            ),
        ]
    )

def hero_daily_return(row_index):
    return Col(
        class_name="col-auto",
        children=[
            Span(
                class_name=format_template(
                    'd-block text-right font-small-1 text-{{ color }}',
                    {
                        "color": f'$.data[{row_index}].color'
                    }
                ),
                content="Daily"
            ),
            Span(
                class_name=format_template(
                    'd-block text-right font-small-3 text-{{ color }}',
                    {
                        "color": f'$.data[{row_index}].color'
                    }
                ),
                content=format_currency(
                    f"$.data[{row_index}].daily",
                    f"$.data[{row_index}].fiatSymbol"
                )
            )
        ]
    )
