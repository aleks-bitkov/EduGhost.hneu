import flet as ft

from view.components.commons import PaddingContainer
from view.components.title import Title


class MainView(PaddingContainer, ft.Container):
    def __init__(self):
        super().__init__()
        self.content = self._content()

    def _content(self):
        return ft.Container(
            content=ft.Row([
                self._left_column(),
                self._right_column()
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START)
        )

    def _left_column(self):
        title = Title("Розклад на сьогодні")

        cards = []

        for i in range(10):
            cards.append(self.create_lesson_card(i+1, f"Філософія {i+1}", f"0{i+2}:0{i+5}", f"0{i+3}:{i+10}"))

        if not cards:
            cards.append(
                ft.Text(
                    value='На сьогодні пар немає, відпочиваємо 🥳',
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    width=450,
                    selectable=True,
                )
            )

        content = ft.Column([
            ft.Row([title,]),
            ft.Divider(height=15),
            ft.Column(
                cards,
                scroll=ft.ScrollMode.ALWAYS,
                height=480
            )
        ])

        return content

    def _right_column(self):
        title = Title("Додані посилання")
        button_add = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color=ft.Colors.WHITE,
            tooltip="Додати посилання"

        )

        cards = []

        for i in range(10):
            cards.append(
                self.create_link_card(f"Філософія {i+1}")
            )

        content = ft.Column(
            [
                ft.Row(
                    controls=[
                        title,
                        button_add,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=500,
                ),
                ft.Divider(height=15),
                ft.Column(cards, scroll=ft.ScrollMode.ALWAYS, height=480),
            ]
        )
        return content

    def create_lesson_card(self, number, lesson_name, lesson_start, lesson_end):
        card = ft.Container(
            bgcolor="#413D3D",
            width=540,
            height=60,
            padding=ft.padding.symmetric(5, 15),
            border_radius=ft.border_radius.all(10),
            content=ft.Row(
                [
                    ft.Text(value=number, size=26, weight=ft.FontWeight.W_900),
                    ft.Text(
                        value=lesson_name,
                        size=20,
                        weight=ft.FontWeight.W_400,
                        text_align=ft.TextAlign.LEFT,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        width=370,
                        selectable=True,
                    ),
                    ft.Column(
                        [
                            ft.Text(value=lesson_start, text_align=ft.TextAlign.CENTER, size=16),
                            ft.Text(value="—", text_align=ft.TextAlign.CENTER),
                            ft.Text(value=lesson_end, text_align=ft.TextAlign.CENTER, size=16),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=-7,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
        return card

    def create_link_card(self, lesson_name):
        data = {
            "lesson_name": lesson_name,
        }
        card = ft.Container(
            bgcolor="#413D3D",
            width=540,
            height=60,
            padding=ft.padding.symmetric(5, 15),
            border_radius=ft.border_radius.all(10),
            content=ft.Row(
                [
                    ft.Text(
                        value=lesson_name,
                        size=20,
                        weight=ft.FontWeight.W_400,
                        text_align=ft.TextAlign.LEFT,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        width=370,
                        selectable=True,
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, data=data),
                            ft.IconButton(icon=ft.Icons.DELETE, data=data),
                        ])
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
        return card
