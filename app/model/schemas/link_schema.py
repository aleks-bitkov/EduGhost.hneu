from pydantic import BaseModel, HttpUrl

from app.model.settings import LINKS_JSON
from app.model.utils import utils_json as json


class ClassSession(BaseModel):
    """Модель для отдельного занятия с валидацией URL"""
    zoom: HttpUrl
    attendance: HttpUrl

class Subject(BaseModel):
    lecture: ClassSession | None = None
    laboratory: ClassSession | None = None
    practice: ClassSession | None = None

class Link(BaseModel):
    subjects: dict[str, Subject]
    
    def __init__(self, subjects: dict[str, Subject] | None = None):
        if subjects is None:
            subjects = json.read(LINKS_JSON, "LINKS_JSON")
        super().__init__(subjects=subjects)
    
    def save(self):
        json.write(LINKS_JSON, self.subjects, "LINKS_JSON")
    
    class Config:
        extra = "allow"
