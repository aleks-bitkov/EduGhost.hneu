
import flet as ft


class TopPanel(ft.WindowDragArea):

    def __init__(self, page):
        super().__init__(page)
        self.content = self._content()
        self.page = page
        self.maximizable = False


    def _content(self):
        content = ft.Container(
            content=ft.Row([
                self._options(),
                self.closed_minimized(),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor= "#352F2F"
        )

        return content


    def _options(self):
        button_script = ft.TextButton(
            content=ft.Text(
                value="Скрипт",
                size=18,
                color=ft.Colors.WHITE,
            ),
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.TRANSPARENT,  # отключаем фон при наведении
                text_style={
                    ft.ControlState.DEFAULT: ft.TextStyle(decoration=ft.TextDecoration.NONE),
                    ft.ControlState.HOVERED: ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                },
            ),
            on_hover=lambda e: self.work_with_script(e),
        )

        button_settings = ft.TextButton(
            content=ft.Text(
                value="Налаштування",
                size=18,
                color=ft.Colors.WHITE,
            ),
            style=ft.ButtonStyle(
                overlay_color=ft.Colors.TRANSPARENT,  # отключаем фон при наведении
                text_style={
                    ft.ControlState.DEFAULT: ft.TextStyle(decoration=ft.TextDecoration.NONE),
                    ft.ControlState.HOVERED: ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                },
            ),
            on_click=lambda e: self.work_with_settings(e),
        )

        options = ft.Container(
            padding=ft.padding.only(left=25),
            content=ft.Row([
                button_script,
                button_settings,
            ])
        )

        return options

    def work_with_script(self, e=None):
        ...

    def work_with_settings(self, e=None):
        ...

    def closed_minimized(self):
        button_minimize = ft.IconButton(
            icon=ft.Icons.MINIMIZE,
            icon_color=ft.Colors.WHITE,
            icon_size=25,
            on_click=lambda e: self.minimize(e),
        )

        button_close = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=ft.Colors.WHITE,
            icon_size=25,
            on_click=lambda _: self.page.window.close()
        )

        content = ft.Container(
            content=ft.Row([button_minimize, button_close]),
            padding=ft.padding.only(right=25),
        )
        return content

    def minimize(self, e=None):
        self.page.window.minimized = True if self.page.window.minimized else False
        self.page.update()