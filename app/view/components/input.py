import flet as ft


class Input(ft.Container):
    def __init__(self, label:str, data):
        super().__init__()
        self.label = label
        self.data = data
        self.content = self._content()
        self.width = 500


    def _content(self):

        content = ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        value=self.label,
                        size=20,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_300,
                    ),
                    padding=ft.padding.only(left=30),
                ),
                ft.TextField(
                    border=ft.InputBorder.OUTLINE,
                    border_radius=20,
                    bgcolor="#312F2F",
                    border_color=ft.Colors.TRANSPARENT,
                    focused_border_color=ft.Colors.TRANSPARENT,
                    border_width=0,
                    data=self.data,
                    on_blur=lambda e: print(f"on_blur = {e}; {e.control.data=}"),
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        return content
