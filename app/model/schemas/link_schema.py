from model.settings import LINKS_JSON
from model.utils import utils_json as json
from pydantic import BaseModel, HttpUrl


class ClassSession(BaseModel):
    """Модель для отдельного занятия с валидацией URL"""
    zoom: HttpUrl | str = ""
    attendance: HttpUrl | str = ""

class Subject(BaseModel):
    lecture: ClassSession | None = None
    laboratory: ClassSession | None = None
    practice: ClassSession | None = None

class Link(BaseModel):
    subjects: dict[str, Subject]

    def __init__(self, subjects: dict[str, Subject] | None = None):
        if subjects is None:
            subjects = self._load_subjects()
        super().__init__(subjects=subjects)

    def _load_subjects(self) -> dict[str, Subject]:
        """Загружает предметы из JSON файла"""
        try:
            data = json.read(LINKS_JSON, "LINKS_JSON")

            # Проверяем структуру данных
            if isinstance(data, dict):
                if "subjects" in data:
                    # Если есть обертка subjects, берем содержимое
                    return data["subjects"]
                else:
                    # Если нет обертки, считаем что это уже словарь предметов
                    return data
            else:
                return {}
        except Exception:
            return {}

    class Config:
        extra = "allow"

    def save(self):
        """Сохраняет только содержимое subjects без обертки"""
        subjects_dict = {}
        for subject_name, subject in self.subjects.items():
            subjects_dict[subject_name] = subject.model_dump()

        json.write(LINKS_JSON, subjects_dict, "LINKS_JSON")