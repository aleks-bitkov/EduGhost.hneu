import flet as ft

from view import colors
from view.components.top_panel import TopPanel
from view.views.main_view import MainView

from view.views.settings_view import SettingsView
from logger import log



class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content_view = MainView() # Default
        self.buttons = {}

        self.top_panel = TopPanel(self.page, self.switch_content, self.add_button)
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
        main_column = ft.Column([self.top_panel, self.content_view])
        self.page.add(main_column)

    def add_button(self, key, button):
        self.buttons[key] = button

    def switch_content(self, e):
        if not e:
            log.error('не отримано даних для зміни представлення')

        new_view = e.control.data['view']

        if new_view == "home":
            self.content_view.content = MainView()
        elif new_view == "settings":
            self.content_view.content = SettingsView()

        for view_name, button in self.buttons.items():
            button.set_active(view_name == new_view)

        self.page.update()
