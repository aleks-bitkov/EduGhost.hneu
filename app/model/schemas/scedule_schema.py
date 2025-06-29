
from pydantic import BaseModel

from app.model.schemas.lesson_shcema import Lesson


class Schedule(BaseModel):
    lessons: list[Lesson]
