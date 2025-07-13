import flet as ft
from logger import log
from view.components import commons
from view.components.button import Button
from view.components.input import Input
from view.components.title import Title


class SettingsView(ft.Container):
    def __init__(self, user_service):
        super().__init__()
        self.user_service = user_service
        self.user = self.user_service.get()
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
        login = Input(label="логін", data="login", value=self.user.login, service=self.user_service)
        password = Input(label="пароль", data="password", value=self.user.password, service=self.user_service)
        personal_schedule_url = Input(label="особисте посилання на розклад", data="url", value=self.user.schedule_url, service=self.user_service)

        msg = commons.about_more_msg("особисті дані зберігаються виключно на вашому пристрої, детальніше про це можна почитати тут")

        title_link = Title("Налаштування послань")
        row_btns = ft.Row(
            [
                Button("імпорт посилань"),
                Button("експорт посилань"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=500,
            expand=True,
        )


        return ft.Column([title_pns, login, password, personal_schedule_url, msg, ft.Divider(height=20), title_link, row_btns])


    def _right_column(self)-> ft.Column:
        title_app = Title("Налаштування застосунку")
        check_boxes_row = ft.Row(
            [
                ft.Checkbox(
                    label="aвто-завершення",
                    label_style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.W_400,
                        color=ft.Colors.WHITE,
                    ),
                    data="auto_off",
                    value=self.user.auto_off,
                    on_change=self.handle_change_checkbox,
                ),
                ft.Checkbox(
                    label="aвто-запуск",
                    label_style=ft.TextStyle(
                        size=24,
                        weight=ft.FontWeight.W_400,
                        color=ft.Colors.WHITE,
                    ),
                    value=self.user.auto_start,
                    data="auto_start",
                    on_change=self.handle_change_checkbox,
                ),
            ],
            spacing=70,
        )

        title_third_app = Title("Налаштування зовнішніх застосунків")
        path_firefox = Input("шлях до Firefox", data="path Firefox", value="/usr/bin/firefox", service=self.user_service)
        path_zoom = Input("шлях до Zoom", data="path Zoom", value="/usr/bin/zoom", service=self.user_service)

        msg = commons.about_more_msg("детальніще про налаштування самого застосунку, налаштування зовнішніх застосунків та експорт/імпорт даних можна почитати тут ")
        return ft.Column([title_app, check_boxes_row,ft.Divider(height=30), title_third_app, path_firefox, path_zoom, msg])

    def handle_change_checkbox(self, e):

        if e.control.data == "auto_off":
            self.user.auto_off = e.control.value
        elif e.control.data == "auto_start":
            self.user.auto_start = e.control.value
        else:
            log.error("не зрозуміле значення для збереження у користувача")

        self.user.save()
        log.debug("дані користувача оновлені")