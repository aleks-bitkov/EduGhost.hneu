import asyncio
from datetime import datetime, timedelta

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
        """  TODO: читання відбувається вне залежності від змін
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
                log_prefix = "відмітки"
                link = self.links[lesson.name][lesson.type]["attendance"]
            elif activity_type == "meeting":
                log_prefix = "відвідування"
                link = self.links[lesson.name][lesson.type]["zoom"]
            else:
                log.error("не зрозумілий тип активності для %r", lesson.name)
        except KeyError:
            log.warning("пари %r не знайдено у доданих. ігоруємо...", lesson.name)
            return
        except Exception:
            log.exception("невідома помилка під час отримання посилання для %s %r", log_prefix, lesson.name)
            return

        if not link:
            log.warning("немає посилання %s для %r. ігноруємо...", log_prefix, lesson.name)
            return

        status, now, start, end = await self.get_lesson_status(lesson)

        if status == "past":
            log.info("%r закіничлася", lesson.name)
            return
        elif status == "error":
            log.error("помилка при отримані статусу. ігноруємо...")
            return
        elif status == "upcoming":
            log.info("пара %r ще не почалась", lesson.name)
            log.debug("зараз %s, початок о %s", str(start), str(now))
            difference = start - now
            seconds_left = int(difference.total_seconds()) # + 300

            log_start_time = (start + timedelta(seconds=300)).strftime("%H:%M")

            log.info("очікуємо до %s. Залишилось ~ %s", log_start_time, utils.format_time(seconds_left))
           
            await asyncio.sleep(seconds_left)
        else:
            pass  # active type 100%

        if activity_type == "meeting":
            await self.zoom.join(link)
        elif activity_type == "attendance":
            await self.pns.put_a_mark(link, lesson.end)
        else:
            log.error("не зрозумілий такий тип як %r", activity_type)
            return

        now = await utils.get_kyiv_now(format_datetime=True)
        to_end_lesson = int((end - now).total_seconds()) - 900

        if to_end_lesson <= 600:
            log.info("до кінця %r залишилось <= 10 хвилин. пропускаємо цю пару", lesson.name)
            return

        if activity_type == "meeting":
            log.info("до закінчення %r залишилось %s.", lesson.name, utils.format_time(to_end_lesson))

        await asyncio.sleep(to_end_lesson)

        # need kill zoom process
        if activity_type == "meeting":
            try:
                await self.zoom.kill()
            except Exception:
                log.exception("невідома помилка при знищені процесу Zoom")

    async def zoom_meet_processing(self):
        if not self.links:
            log.debug("не отримано посилань")
            return

        for lesson in self.lessons:
            await self.handle_lesson_activity(lesson, "meeting")

    async def attendance_processing(self):
        if not self.links:
            log.debug("не отримано посилань")
            return

        for lesson in self.lessons:
            await self.handle_lesson_activity(lesson, "attendance")


# user = User()
# selenium_manager = SeleniumManager()
# web_driver = asyncio.run(selenium_manager.driver)

# zoom = ZoomService(web_driver)
# pns = PnsRepository(username=user.login, password=user.password, web_driver=web_driver)


# lessons=[
#     Lesson
#     (
#         name='ТЕОРІЯ ЙМОВІРНОСТЕЙ ТА МАТЕМАТИЧНА СТАТИСТИКА', 
#         type='laboratory', 
#         start='18:12', 
#         end='23:59'
#     ),
#     Lesson
#     (
#         name='ФІЛОСОФІЯ',
#         type='practice',
#         start='12:10', 
#         end='23:59'
#     )
# ]

# schedule = Schedule(lessons=lessons)

# lm = LessonManager(pns_repo=pns, zoom_service=zoom, schedule=schedule)

# async def foo:
#     t1 = asyncio.create_task(lm.attendance_processing())
#     t2 = asyncio.create_task(lm.zoom_meet_processing())

#     asyncio.gather(t1, t2)
