from collections.abc import Callable

import flet as ft
from view.components import commons


class TopPanel(ft.WindowDragArea):

    def __init__(self, page, switch_content: Callable = None, add_button: Callable = None):
        super().__init__(page)
        self.switch_content = switch_content
        self.add_button = add_button

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
        button_home = commons.NavButton(
            icon=ft.Icons.HOME,
            view="home",
            tooltip="Головна",
            on_click=self.switch_content,
            active=True,
        )
        button_settings = commons.NavButton(
            icon=ft.Icons.SETTINGS,
            view="settings",
            tooltip="Налаштування",
            on_click=self.switch_content,
            active=False,
        )

        button_script = ft.PopupMenuButton(
            icon=ft.Icons.TERMINAL,
            icon_color=ft.Colors.GREY,
            menu_position=ft.PopupMenuPosition.UNDER,
            items=[
                ft.PopupMenuItem(text="Item 1"),
                ft.PopupMenuItem(text="Item 2"),
            ],
            on_open=self.on_open_menu,
            on_cancel=self.on_cancel_menu
        )


        self.add_button("home", button_home)
        self.add_button("settings", button_settings)

        options = ft.Container(
            padding=ft.padding.only(left=25),
            content=ft.Row([
                button_home,
                button_settings,
                button_script,
            ])
        )

        return options

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

    @staticmethod
    def on_open_menu(e):
        e.control.icon_color = ft.Colors.WHITE
        e.control.update()

    @staticmethod
    def on_cancel_menu(e):
        e.control.icon_color = ft.Colors.GREY
        e.control.update()