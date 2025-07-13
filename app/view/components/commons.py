import flet as ft


class PaddingContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.padding = ft.padding.symmetric(20, 25)

class NavButton(ft.IconButton):
    def __init__(self, icon, view, tooltip, on_click, active):
        super().__init__()
        self.icon = icon
        self.tooltip = tooltip
        self.data = {"view": view}
        self.style = ft.ButtonStyle(
            overlay_color=ft.Colors.TRANSPARENT,
            icon_color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE if active else ft.Colors.GREY,
                ft.ControlState.HOVERED: ft.Colors.WHITE if active else ft.Colors.RED,
                ft.ControlState.FOCUSED: ft.Colors.WHITE if active else ft.Colors.RED,
            },
        )
        self.on_click = on_click

    def set_active(self, active: bool):
        self.style.icon_color = {
            ft.ControlState.DEFAULT: ft.Colors.WHITE if active else ft.Colors.GREY,
            ft.ControlState.HOVERED: ft.Colors.WHITE if active else ft.Colors.RED,
            ft.ControlState.FOCUSED: ft.Colors.WHITE if active else ft.Colors.RED,
        }
        self.update()




def about_more_msg(msg):
    return ft.Text(
        value=msg,
        color="#A3E528",
        size=16,
        selectable=True,
        width=500,
    )
