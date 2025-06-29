
from pydantic import BaseModel

from model.schemas.lesson_shcema import Lesson


class Schedule(BaseModel):
    lessons: list[Lesson]
