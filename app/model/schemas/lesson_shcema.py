from pydantic import BaseModel


class Lesson(BaseModel):
    name: str
    type: str
    start: str
    end: str
