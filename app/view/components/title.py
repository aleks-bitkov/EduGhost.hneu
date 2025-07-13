import flet as ft


class Title(ft.Text):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.color = ft.Colors.WHITE
        self.size = 24
        self.weight = ft.FontWeight.W_500
        self.selectable = True
