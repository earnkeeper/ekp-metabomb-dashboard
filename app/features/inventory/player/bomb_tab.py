from app.utils.game_constants import METABOMB_IMAGE_URL
from app.utils.image_cell import image_cell
from ekp_sdk.ui import (Column, Container, Datatable,
                        commify, format_currency,
                        format_template, is_busy, format_percent, navigate, Image, Row, Col, Span, Div)
from ekp_sdk.util import collection, documents


def bomb_tab(BOMBS_COLLECTION_NAME):
    return Container(
        children=[
            Datatable(
                data=documents(BOMBS_COLLECTION_NAME),
                busy_when=is_busy(collection(BOMBS_COLLECTION_NAME)),
                on_row_clicked=navigate(
                    format_template("https://market.metabomb.io/bomb/{{ token_id }}", {
                        "token_id": "$.id"
                    }),
                    True,
                    True
                ),
                columns=[
                    Column(
                        id="id",
                        title="Token Id",
                        width="100px"
                    ),
                    Column(
                        id="name",
                        cell=name_cell(),
                        min_width='200px',
                    ),
                    Column(
                        id="price",
                        title="MTB Value",
                        format=commify("$.price"),
                        width="120px",
                        sortable=True,
                    ),
                    Column(
                        id="price_fiat",
                        title="Fiat Value",
                        format=format_currency(
                            "$.price_fiat", "$.fiat_symbol"
                        ),
                        width="120px",
                        sortable=True,
                    ),
                    Column(
                        id="skills",
                        title="Skills",
                        cell=skills_cell(),
                        min_width="200px",
                        # right=True
                    ),
                    Column(
                        id="spacer",
                        title="",
                        width="2px"
                    ),
                    Column(
                        id="rarity_name",
                        omit=True,
                        title="Rarity"
                    ),
                    Column(
                        id="level",
                        omit=True
                    ),

                ]
            )
        ]
    )


def name_cell():
    return Div([
        Image(
            src=format_template(METABOMB_IMAGE_URL + "/gifs/bomb-gif/{{ display_id }}.gif", {
                "display_id": '$.display_id'
            }),
            style={
                "height": "32px",
                "marginRight": "8px"
            }
        ),
        Span("$.name"),
        Image(
            src=format_template(
                METABOMB_IMAGE_URL +
                "/icons/element-icon/{{ element }}.png",
                {
                    "element": '$.element'
                }),
            style={
                "height": "14px",
                "marginLeft": "8px"
            }
        )
    ])
    return Row(
        class_name="mt-1",
        children=[
            Col(
                class_name="my-auto col-auto px-0",
                children=[
                    Image(
                        src=format_template(METABOMB_IMAGE_URL + "/gifs/bomb-gif/{{ display_id }}.gif", {
                            "display_id": '$.display_id'
                        }),
                        style={"height": "32px"}
                    )
                ]
            ),
            Col(
                "px-0",
                children=[
                    Row(
                        children=[
                            Col(
                                class_name="col-12 font-small-4",
                                children=[
                                    Row(
                                        children=[
                                            Col(
                                                class_name="col-auto my-auto pr-0",
                                                children=[
                                                    Span("$.name")
                                                ]
                                            ),
                                            Col(
                                                class_name="col-auto my-auto",
                                                children=[
                                                    Image(
                                                        src=format_template(
                                                            METABOMB_IMAGE_URL +
                                                            "/icons/element-icon/{{ element }}.png",
                                                            {
                                                                "element": '$.element'
                                                            }),
                                                        style={
                                                            "height": "14px"}
                                                    )
                                                ]
                                            )

                                        ]
                                    )
                                ]
                            ),
                        ]
                    )

                ]
            )

        ]
    )


def skills_cell():
    return Row(
        children=[
            skill_col(s_id) for s_id in range(1, 7)
        ]
    )


def skill_col(skill_id):
    return Col(
        class_name="my-auto col-auto pr-0",
        children=[
            Image(
                src=format_template(METABOMB_IMAGE_URL + "/icons/skill-icon/skill-{{ skill_id }}.png", {
                    "skill_id": f"$.skill_{skill_id}['skill']"
                }),
                style={"height": "20px", "border-radius": "50%"},
                when=f"$.skill_{skill_id}['skill']",
                tooltip=f"$.skill_{skill_id}['tooltip']",
            )
        ]
    )
