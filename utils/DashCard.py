class CardFactory:
    # dbc == dash bootsrap components instant
    def __init__(self, dbc, html) -> None:
        self.dbc = dbc
        self.html = html

    def get_simple_card(self, title, text, bg_color=[69, 69, 69]):
        return self.dbc.Card(
            [
                # dbc.CardImg(src=img_link, top=True, style={"height": "5vw"}),
                self.dbc.CardBody(
                    [
                        self.html.H4(title, className="card-title"),
                        self.html.P(
                            text,
                            className="card-text",
                        ),
                    ]
                ),
            ],
            style={"width": "30rem", "display": "inline-block",
                   "margin": "10px", "background-color": f"rgba({bg_color[0]}, {bg_color[1]}, {bg_color[2]}, 0.6)"},
        )
