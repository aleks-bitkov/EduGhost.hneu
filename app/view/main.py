import flet as ft

from app.view.run import MainApp

async def main(page: ft.Page):
    MainApp(page)

ft.app(target=main)