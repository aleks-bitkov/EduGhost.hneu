import flet as ft
from controler.link_service import LinkService
from controler.user_service import UserService
from model.schemas.link_schema import Link
from model.schemas.user_shcema import User
from view.run import MainApp


async def main(page: ft.Page):
    user = User()
    link = Link()

    user_service = UserService(user)
    link_service = LinkService(link)

    MainApp(page, user_service, link_service)

ft.app(target=main)