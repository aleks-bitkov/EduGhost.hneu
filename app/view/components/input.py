import flet as ft
from controler.IService import IService


class Input(ft.Container):
    def __init__(self, label:str, data, value, is_save_data = False, service: IService = None):
        super().__init__()
        self.label = label
        self.data = data
        self.value = value
        self.is_save_data = is_save_data
        self.service = service
        self.content = self._content()
        self.width = 500


    def _content(self):
        if self.is_save_data:
            self.service.data[self.data] = self.value

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
                    value=self.value,
                    data=self.data,
                    on_blur=self.service.save if self.service else None,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        return content
