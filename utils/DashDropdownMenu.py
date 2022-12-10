class DropDownMenuFactory:
    def __init__(self, dcc) -> None:
        self.dcc = dcc

    def get_instance(self, id, values):
        return self.dcc.Dropdown(id=id,
                                 options=values, style={"width": "350px", "color": "black"})
