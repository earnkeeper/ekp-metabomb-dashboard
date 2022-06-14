from app.utils.game_constants import HERO_BOX_NAME_IMAGE
from ekp_sdk.ui import (Col, Container, Div, Image, Row, Span, format_currency,
                        format_percent, format_template, switch_case)


def tile():
    return Container(
        children=[
            Span("Box Floor Prices", "font-medium-2"),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell('common'),
                    boxes_name_count('common'),
                    boxes_price_stats('common')
                ]
            ),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell('premium'),
                    boxes_name_count('premium'),
                    boxes_price_stats('premium')
                ]
            ),
            Div(class_name="mb-1"),
            Row(
                children=[
                    image_cell('ultra'),
                    boxes_name_count('ultra'),
                    boxes_price_stats('ultra')
                ]
            )
        ]
    )


def image_cell(box_type):
    return Col("col-auto pr-0 my-auto", [
        Image(
            src=switch_case(
                f"$.data[0]['{box_type}'].name",
                HERO_BOX_NAME_IMAGE
            ),
            style={"height": "32px"}
        )
    ])


def boxes_name_count(box_type):
    return Col(
        children=[
            Span(
                class_name='d-block font-small-3',
                content=f"$.data[0]['{box_type}'].name"
            ),
            Span(
                class_name='d-block font-small-1',
                content=format_template(
                    "{{ boxes_num }} sales",
                    {
                        "boxes_num": f"$.data[0]['{box_type}'].countBoxes"
                    }
                )
            ),
        ]
    )


def boxes_price_stats(box_type):
    return Col(
        class_name="col-auto",
        children=[
            Span(
                class_name=format_template(
                    'd-block text-right font-small-3 text-{{ color }}',
                    {
                        "color": f'$.data[0]["{box_type}"].color'
                    }
                ),
                content=format_currency(
                    f"$.data[0]['{box_type}'].floorPrice",
                    f"$.data[0]['{box_type}'].fiatSymbol"
                )
            ),
            Span(
                class_name=format_template(
                    'd-block text-right font-small-1 text-{{ color }}',
                    {
                        "color": f'$.data[0]["{box_type}"].color'
                    }
                ),
                content=format_percent(
                    f"$.data[0]['{box_type}'].percDiff",
                )
            ),
        ]
    )
