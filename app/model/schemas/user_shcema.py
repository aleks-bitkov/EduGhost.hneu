import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pydantic import BaseModel, HttpUrl

from model.settings import PROFILE_JSON
from model.utils import utils_json as json


class User(BaseModel):
    schedule_url: HttpUrl
    login: str

    def __init__(self, **kwargs):
        kwargs = json.read(PROFILE_JSON, "PROFILE_JSON")
        super().__init__(**kwargs)

    def save(self):
        data = self.model_dump(mode='json')
        json.write(PROFILE_JSON, data, "PROFILE_JSON")
    
    class Config:
        extra = "allow"
