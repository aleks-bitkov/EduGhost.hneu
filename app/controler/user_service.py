from controler.IService import IService
from logger import log


class UserService(IService):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def save(self, e) -> None:
        log.debug("оновлення даних користувача")
        data = e.control.data
        value = e.control.value

        if data == "login":
            self.user.login = value
        elif data == "password":
            self.user.password = value
        else:
            log.error('не зрозумілі дані для користувача')
            return None

        self.user.save()
        return None

    def get(self):
        return self.user
