from collections.abc import Callable

import flet as ft
from controler.common import get_today_schedule
from view.components.commons import PaddingContainer
from view.components.title import Title


class MainView(PaddingContainer, ft.Container):
    def __init__(self, switch_content: Callable, add_button: Callable, page:ft.Page, service_link=None):
        super().__init__()
        self.switch_content = switch_content
        self.service_link = service_link
        self.page = page
        self.add_button = add_button
        self.column_cards = ft.Column([]) # empty, initialization

        self.content = self._content()

    @property
    def subjects_name(self):
        return list(self.service_link.get_subjects_name()) if self.service_link else []

    def _content(self):
        stack = ft.Stack(
            [
                ft.Container(
                    content=ft.Row(
                        [self._left_column(), self._right_column()],
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    )
                ),
                # ft.Container(width=600, height=100, top=0, left=300, content=ft.ListView()),
            ]
        )


        return stack

    def _left_column(self):
        title = Title("Розклад на сьогодні")

        schedule = get_today_schedule()
        lessons = []

        if not schedule:
            lessons.append(
                ft.Text(
                    value='На сьогодні пар немає, відпочиваємо 🥳',
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    width=450,
                    selectable=True,
                )
            )
            return None


        for lesson in schedule.lessons:
            item = self.create_lesson_card(
                lesson.type[:2],
                lesson.name,
                lesson.start,
                lesson.end
            )

            lessons.append(item)


        content = ft.Column([
            ft.Row([title,]),
            ft.Divider(height=15),
            ft.Column(
                lessons,
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
            tooltip="Додати посилання",
            data={"view": "links"},
            on_click=self.switch_content,
        )
        self.add_button("links", button_add)

        cards = []

        for subject_name in self.subjects_name:
            cards.append(
                self.create_link_card(subject_name)
            )

        if not cards:
            cards.append(
                ft.Text("Посилання поки не додані")
            )

        self.column_cards = ft.Column(controls=cards, scroll=ft.ScrollMode.ALWAYS, height=480)

        content = ft.Column(
            [
                ft.Row(
                    controls=[
                        title,
                        button_add,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment= ft.CrossAxisAlignment.CENTER,
                    width=540,
                ),
                ft.Divider(height=15),
                self.column_cards
            ]
        )
        self.page.update()
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
        button_edit = ft.IconButton(
            icon=ft.Icons.EDIT,
            data={"view": "edit", "lesson_name": lesson_name},
            on_click=self.switch_content,
        )
        self.add_button("edit", button_edit)

        button_delete = ft.IconButton(
            icon=ft.Icons.DELETE,
            data={"view": "home", "lesson_name": lesson_name},
            on_click=lambda e: self.service_link.delete(e, self.switch_content),
        )

        self.add_button("delete", button_delete)

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
                            button_edit,
                            button_delete,
                        ])
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
        return card
