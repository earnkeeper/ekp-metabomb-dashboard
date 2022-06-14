from app.utils.game_constants import METABOMB_IMAGE_URL
from app.utils.image_cell import image_cell
from ekp_sdk.ui import (Column, Container, Datatable,
                        commify, format_currency,
                        format_template, is_busy, format_percent, navigate, Image)
from ekp_sdk.util import collection, documents



def hero_tab(HEROES_COLLECTION_NAME):
    return Container(
        children=[
            Datatable(
                data=documents(HEROES_COLLECTION_NAME),
                busy_when=is_busy(collection(HEROES_COLLECTION_NAME)),
                on_row_clicked=navigate(
                    format_template("https://market.metabomb.io/hero/{{ token_id }}", {
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
                        cell=__name_cell,
                        min_width='200px'
                    ),
                    Column(
                        id="price",
                        title="MTB Value",
                        format=commify("$.price"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="price_fiat",
                        title="Fiat Value",
                        format=format_currency(
                            "$.price_fiat", "$.fiat_symbol"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="mtb_per_day",
                        title="MTB / day",
                        format=commify("$.mtb_per_day"),
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="est_payback",
                        title="ROI",
                        width="120px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="est_roi",
                        title="APR",
                        format=format_percent("$.est_roi"),
                        width="100px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_class",
                        title="Class",
                        cell=class_image(),
                        width="120px",
                        sortable=True,
                    ),
                    Column(
                        id="hero_power",
                        title="Power",
                        cell=set_image(icon_name='stats-power',
                                       attr_name='hero_power'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_health",
                        title="Health",
                        cell=set_image(icon_name='stats-health',
                                       attr_name='hero_health'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_speed",
                        title="Speed",
                        cell=set_image(icon_name='stats-speed',
                                       attr_name='hero_speed'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_stamina",
                        title="Stamina",
                        cell=set_image(icon_name='stats-stamina',
                                       attr_name='hero_stamina'),
                        width="90px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_bomb_num",
                        title="Bomb num",
                        cell=set_image(icon_name='stats-bombnum',
                                       attr_name='hero_bomb_num'),
                        width="80px",
                        right=True,
                        sortable=True,
                    ),
                    Column(
                        id="hero_bomb_range",
                        title="Bomb range",
                        cell=set_image(icon_name='stats-bombrange',
                                       attr_name='hero_bomb_range'),
                        width="80px",
                        right=True,
                        sortable=True,
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


__name_cell = image_cell(
    format_template(METABOMB_IMAGE_URL + "/gifs/char-gif/{{ display_id }}.gif", {
        "display_id": '$.display_id'
    }),
    "$.name"
)

def class_image():
    return image_cell(
        image=format_template(METABOMB_IMAGE_URL + "/icons/class-{{ hero_class }}.png", {
            "hero_class": '$.hero_class'
        }),
        content="$.hero_class_capital",
        image_size="16px"
    )


def set_image(icon_name, attr_name):
    return image_cell(
        f"{METABOMB_IMAGE_URL}/icons/stats-icon/{icon_name}.svg",
        f"$.{attr_name}",
        image_size="16px"
    )
