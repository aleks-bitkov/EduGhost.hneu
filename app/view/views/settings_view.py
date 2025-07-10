import flet as ft
from view.components import commons
from view.components.input import Input
from view.components.title import Title


class SettingsView(ft.Container):
    def __init__(self):
        super().__init__()

        self.content = self._content()

    def _content(self):
        return ft.Container(
            content=ft.Row([
                self._left_column(),
                self._right_column(),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START)
        )

    def _left_column(self) -> ft.Column:
        title_pns = Title("Налаштування PNS")
        login = Input(label="логін", data="login")
        password = Input(label="пароль", data="password")
        personal_schedule_url = Input(label="особисте посилання на розклад", data="url")

        msg = commons.about_more_msg("особисті дані зберігаються виключно на вашому пристрої, детальніше про це можна почитати тут")

        title_link = Title("Налаштування послань")
        row_btns = ft.Row(
            [
                ft.TextButton(text="Імпорт"),
                ft.TextButton(text="Експорт"),
            ]
        )


        return ft.Column([title_pns, login, password, personal_schedule_url, msg, title_link, row_btns])


    def _right_column(self)-> ft.Column:
        title_app = Title("Налаштування застосунку")
        check_boxes_row = ft.Row([])

        title_third_app = Title("Налаштування зовнішніх застосунків")
        path_firefox = Input("шлях до Firefox", data="path Firefox")
        path_zoom = Input("шлях до Zoom", data="path Zoom")

        msg = commons.about_more_msg("детальніще про налаштування самого застосунку, налаштування зовнішніх застосунків та експорт/імпорт даних можна почитати тут ")
        return ft.Column([title_app, check_boxes_row, title_third_app, path_firefox, path_zoom, msg])