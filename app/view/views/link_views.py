import flet as ft
from view.components.button import Button
from view.components.commons import PaddingContainer
from view.components.input import Input
from view.components.title import Title


class LinkView(PaddingContainer, ft.Container):
    def __init__(self, link_service, subject_info=None, subject="", is_save_data=False, switch_content=None):
        super().__init__()
        self.link_service = link_service

        self.subject_info = subject_info
        self.is_save_data = is_save_data
        self.subject = subject
        self.switch_content = switch_content
        self.content = self._content()

    def _content(self):
        main_title = Title("Налаштування посилань")
        return ft.Container(
            content=ft.Column(
                [
                    main_title,
                    Input("Назва пари", "pair_name", self.subject, self.is_save_data, self.link_service),
                    ft.Column(
                        [
                            self.generate_row(
                                title_row="Налаштування лекції",
                                data_pns="lecture_attendance",
                                data_meeting="lecture_zoom",
                                value_pns=self.subject_info.lecture.attendance if self.subject_info else "",
                                value_meeting=self.subject_info.lecture.zoom if self.subject_info else "",
                            ),
                            self.generate_row(
                                title_row="Налаштування практичної",
                                data_pns="practice_attendance",
                                data_meeting="practice_zoom",
                                value_pns=self.subject_info.practice.attendance if self.subject_info else "",
                                value_meeting=self.subject_info.practice.zoom if self.subject_info else "",
                            ),
                            self.generate_row(
                                title_row="Налаштування лабораторної",
                                data_pns="laboratory_attendance",
                                data_meeting="laboratory_zoom",
                                value_pns=self.subject_info.laboratory.attendance if self.subject_info else "",
                                value_meeting=self.subject_info.laboratory.zoom if self.subject_info else "",
                            ),
                            ft.Row(
                                [
                                    Button(
                                        text="Зберегти",
                                        on_click=lambda e: self.link_service.save_to_file(self.switch_content, e),
                                        data={"view": "home"}
                                    ),
                                ]
                            ),
                        ],
                        expand=True,
                    ),
                ],
            )
        )

    def generate_row(self, title_row: str, data_pns, data_meeting, value_pns="", value_meeting=""):
        title = ft.Container(
            content=ft.Row(
                [
                    ft.Container(height=1, width=470, bgcolor=ft.Colors.WHITE),
                    Title(title_row),
                    ft.Container(height=1, width=470, bgcolor=ft.Colors.WHITE),
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        row_inputs = ft.Row(
            [
                Input("Посилання для відмітки на PNS", data_pns, value_pns, self.is_save_data, self.link_service),
                Input("Посилання для відвідування Zoom", data_meeting, value_meeting,self.is_save_data, self.link_service),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ft.Column([title, row_inputs])



    def _left_column(self):
        lecture = Input("Посилання для відмітки на PNS ", data=None, value=None)
        practice = Input("Посилання для відмітки на PNS ", data=None, value=None)
        laboratory = Input("Посилання для відмітки на PNS ", data=None, value=None)

        return ft.Column([lecture, practice, laboratory])

    def _right_column(self):
        lecture = Input("Посилання для відвідування Zoom  ", data=None, value=None)
        practice = Input("Посилання для відвідування Zoom ", data=None, value=None)
        laboratory = Input("Посилання для відвідування Zoom ", data=None, value=None)

        return ft.Column([lecture, practice, laboratory])