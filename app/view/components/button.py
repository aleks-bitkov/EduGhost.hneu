import flet as ft


class Button(ft.Container):
    def __init__(self, text: str, on_click=None, data=None):
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.data = data

        self.content = self._content()
        self.bgcolor = "#353535"
        self.border = ft.border.all(1, ft.Colors.TRANSPARENT)
        self.border_radius = 15
        self.padding = ft.padding.symmetric(10, 5)
        self.on_hover = self._on_hover


    def _content(self):
        return ft.TextButton(
            text=self.text,
            content=ft.Text(
                value=self.text,
                size=24,
                color=ft.Colors.WHITE
            ),
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.TRANSPARENT,
            ),
            data=self.data,
            on_click=self.on_click,
        )

    def _on_hover(self, e):
        if e.data == "true":
            self.bgcolor = "#000000"  # Цвет при наведении
        else:
            self.bgcolor = "#353535"  # Исходный цвет
        self.update()


