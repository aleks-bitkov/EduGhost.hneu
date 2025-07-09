import flet as ft

from app.view import colors
from app.view.components.top_panel import TopPanel
from app.view.views.main_view import MainView


class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_view = "main"
        self.top_panel = TopPanel(self.page)
        self.setup_page()

    def setup_page(self):
        self.page.window.always_on_top = True

        self.page.window.bgcolor = colors.MAIN_COLOR
        self.page.bgcolor = colors.MAIN_COLOR

        self.page.window.maximizable = False
        self.page.window.resizable = False

        self.page.window.title_bar_hidden = True
        self.page.window.frameless = True
        self.page.window.title_bar_buttons_hidden = True

        self.page.window.width = 750
        self.page.window.height = 450
        self.page.window.min_width = 750
        self.page.window.max_width = 750
        self.page.window.min_height = 450
        self.page.window.max_height = 450

        self.page.window.padding = 0

        self.create_layout()

    def create_layout(self):


        main_column = ft.Column([
            self.top_panel,
            self.get_main_content()
        ])

        self.page.add(main_column)

    @staticmethod
    def get_main_content():
        return MainView()
