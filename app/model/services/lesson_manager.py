import asyncio
from datetime import datetime

from app.logger import log
from app.model import settings
from app.model.schemas.lesson_shcema import Lesson
from app.model.schemas.link_schema import Link
from app.model.schemas.scedule_schema import Schedule
from app.model.utils import common_utils as utils
from app.model.utils import utils_json as json


class LessonManager:
    def __init__(self, pns_repo, zoom_service, schedule: Schedule):
        self.pns = pns_repo
        self.zoom = zoom_service
        self.lessons = schedule.lessons
        self.links = Link()

    async def _check_time_last_lesson(self):
        last_end_time = self.lessons[-1].end
        now_str = await utils.get_kyiv_now()

        now = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {last_end_time}", "%Y-%m-%d %H:%M")

        return now > end

    async def get_lesson_status(self, lesson: Lesson):
        now_str = await utils.get_kyiv_now()
        now = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
        start = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {lesson.start}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {lesson.end}", "%Y-%m-%d %H:%M")

        if start < now < end:
            return "active", now, start, end
        elif now < start:
            return "upcoming", now, start, end
        elif now > end:
            return "past", now, start, end
        else:
            return "error", now, start, end

    async def handle_lesson_activity(self, lesson: Lesson, activity_type: str):
        link = ""
        log_prefix = ""

        #  ====================================================================
        """  TODO: читання відбуваеться вне залежності від змін
            можна використати прапорець, який повідомить чи була зміна у файлі
        """
        temp = json.read(settings.LINKS_JSON)

        if temp:
            log.info('дані про посилання були оновлені')
            self.links = temp
        #  ====================================================================

        try:
            #  Отримання відповідного посилання залежно від типу поточної активності
            if activity_type == "attendance":
                log_prefix = "to mark"
                link = self.links[lesson.name][lesson.type]["attendance"]
            elif activity_type == "meeting":
                log_prefix = "meeting"
                link = self.links[lesson.name][lesson.type]["zoom"]
            else:
                log.error("unknown type for %s", lesson.name)
        except KeyError:
            log.warning("no link found for %s %r. skipping...", log_prefix, lesson.name)
            return
        except Exception:
            log.exception("unknown error while getting link for %s", log_prefix)
            return

        if not link:
            log.warning("no link for %s, %r", log_prefix, lesson.name)
            return

        status, now, start, end = await self.get_lesson_status(lesson)

        if status == "past":
            log.info("%r закіничлася", lesson.name)
            return
        elif status == "error":
            log.error("помилка при отримані статусу. продовжуємо...")
            return
        elif status == "upcoming":
            log.info("пара %r еще не началась", lesson.name)
            difference = start - now
            seconds_left = int(difference.total_seconds()) + 300

            log.info("продолжим выполнения скрипта через %d с.", seconds_left)
            log.debug("ожидаем начала %s...", lesson.name)

            await asyncio.sleep(seconds_left)
        else:
            pass  # active type 100%

        if activity_type == "meeting":
            await self.zoom.join(link)
        elif activity_type == "attendance":
            await self.pns.put_a_mark(link, lesson.end)
        else:
            log.error("unknown activity type as %r", activity_type)
            return

        now = await self.utils.get_kyiv_now(format_datetime=True)
        to_end_lesson = int((end - now).total_seconds()) - 900

        if to_end_lesson <= 600:
            log.info("до конца %r оставалось <= 10 минут. Пропускаем данную пару", lesson.name)
            return

        if activity_type == "meeting":
            log.info("до окончания %r осталось %d с.", lesson.name, to_end_lesson)
            log.debug("ожидаем конца пары...")

        await asyncio.sleep(to_end_lesson)

        # need kill zoom process
        if activity_type == "meeting":
            try:
                await self.zoom.kill()
            except Exception:
                log.exception("невідома помилка при знищені процесу Zoom")

    async def zoom_meet_processing(self):
        if not self.links:
            log.debug("")
            return

        for lesson in self.schedule:
            await self.handle_lesson_activity(lesson, "meeting")

    async def attendance_processing(self):
        if not self.schedule and not self.links:
            log.debug("не було ні посилань не розкладу Attendance")
            return

        for lesson in self.schedule:
            await self.handle_lesson_activity(lesson, "attendance")
