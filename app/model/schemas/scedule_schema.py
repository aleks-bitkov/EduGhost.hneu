
from model.schemas.lesson_shcema import Lesson
from pydantic import BaseModel


class Schedule(BaseModel):
    lessons: list[Lesson]

    def __bool__(self):
        return bool(self.lessons)
