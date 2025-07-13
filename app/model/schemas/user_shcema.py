import os

import keyring
from dotenv import load_dotenv
from model import settings
from model.utils import utils_json as json
from pydantic import BaseModel, HttpUrl

load_dotenv(settings.ENV_PATH)


class User(BaseModel):
    auto_off : bool
    auto_start: bool
    schedule_url: HttpUrl
    login: str

    def __init__(self, **kwargs):
        kwargs = json.read(settings.PROFILE_JSON, "PROFILE_JSON")
        super().__init__(**kwargs)

    def save(self):
        data = self.model_dump(mode='json')
        json.write(settings.PROFILE_JSON, data, "PROFILE_JSON")

    @property
    def password(self):
        return keyring.get_password(os.getenv("SERVICE_NAME"), self.login)
    
    @password.setter
    def password(self, value):
        keyring.set_password(os.getenv("SERVICE_NAME"), self.login, value)

    def clear(self):
        try:
            keyring.delete_password(os.getenv("SERVICE_NAME"), self.login)
        except keyring.errors.PasswordDeleteError:
            pass #  пароля вже не має 

        self.auto_off = False
        self.schedule_url = HttpUrl("http://www.rozklad.hneu.edu.ua/schedule/schedule?group=-1&student=-1")
        self.login = ""
        self.save() 
    
    class Config:
        extra = "allow"