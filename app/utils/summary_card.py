from ekp_sdk.ui import Avatar, Card, Col, Container, Row, Span


def summary_card(title, value):
    return Container(
        children=[
            Card(
                class_name="p-1",
                children=[
                    Row([
                        Col("col-auto my-auto pr-0", [
                            Avatar(
                                icon="award",
                                size="sm",
                            )
                        ]),
                        Col("col-auto pr-4", [
                            Span(title, "font-medium-1 font-weight-bold d-block"),
                            Span(
                                content=value,
                                class_name="font-small-1 d-block"
                            ),
                        ]),

                    ])
                ])
        ]
    )
