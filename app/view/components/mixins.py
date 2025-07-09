import flet as ft

class PaddingContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = ft.padding.symmetric(20, 25)