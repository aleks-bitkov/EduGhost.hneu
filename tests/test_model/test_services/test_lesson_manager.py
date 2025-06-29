from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from app.model.repositories.pns_repository import PnsRepository
from app.model.schemas.lesson_shcema import Lesson
from app.model.schemas.scedule_schema import Schedule
from app.model.services.lesson_manager import LessonManager
from app.model.services.zoom_service import ZoomService
from app.model.utils import common_utils
from app.model.utils.selenium_manager import SeleniumManager


class TestLessonManager:

    @pytest.fixture(scope="module")
    def lesson_manager(self):
        lesson1 = Lesson(
            name="Теорія ймовірності процесів",
            type="practice",
            start="09:30",
            end="11:05"
        )
        lesson2 = Lesson(
            name="Теорія ймовірності процесів",
            type="laboratory",
            start="09:30",
            end="11:05"
        )
        lessons = [lesson1, lesson2]
        schedule = Schedule(lessons=lessons)

        username = 'username'
        password = 'password'
        driver = SeleniumManager()
        pns_repo = PnsRepository(username=username, password=password, web_driver=driver)

        zoom_service = ZoomService(web_driver=driver)

        lesson_manager = LessonManager(
            pns_repo=pns_repo,
            zoom_service=zoom_service,
            schedule=schedule
        )

        return lesson_manager


    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_time, expected_result, test_description", [
        ("2024-01-15 09:00:00", False, "час до початку занять"),
        ("2024-01-15 10:30:00", False, "час під час занять"),
        ("2024-01-15 11:05:00", False, "час точно в момент закінчення останнього уроку"),
        ("2024-01-15 11:06:00", True, "час за хвилину після закінчення"),
        ("2024-01-15 12:00:00", True, "час за годину після закінчення"),
        ("2024-01-15 23:59:59", True, "час наприкінці дня"),
    ])
    async def test_check_time_last_lesson(self, lesson_manager, current_time, expected_result, test_description):
        with patch.object(common_utils, 'get_kyiv_now', new_callable=AsyncMock) as mock_get_time:
            mock_get_time.return_value = current_time
            
            result = await lesson_manager._check_time_last_lesson()
            
            assert result is expected_result, f"Невірний результат для випадку, коли {test_description}"
            mock_get_time.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("current_time, lesson, expected_status", [
        ("2024-01-15 08:00:00", Lesson(name="Теорія ймовірності", type="practice", start="9:30", end="11:05"), "upcoming"),
        ("2024-01-15 10:00:00", Lesson(name="Теорія ймовірності", type="practice", start="9:30", end="11:05"), "active"),
        ("2024-01-15 12:00:00", Lesson(name="Теорія ймовірності", type="practice", start="9:30", end="11:05"), "past"),
    ])
    async def test_get_lesson_status(self, lesson_manager, current_time, lesson, expected_status):
        with patch.object(common_utils, 'get_kyiv_now', new_callable=AsyncMock) as mock_get_time:
            mock_get_time.return_value = current_time
            
            result = await lesson_manager.get_lesson_status(lesson)
            
            # Метод возвращает кортеж (status, now, start, end)
            assert isinstance(result, tuple)
            assert len(result) == 4
            
            status, now, start, end = result
            assert status == expected_status

            assert isinstance(now, datetime)
            assert isinstance(start, datetime)
            assert isinstance(end, datetime)
            
            mock_get_time.assert_called_once()
