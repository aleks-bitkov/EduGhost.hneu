"""
    Головний файл для запуску логіки усього застоунку. Тут відбувається налаштування 
    репозиторіїв та сервесів. Основні процеси запускаються асинхронно завдяки об'єкт класу LessonManager
"""
import asyncio
import time
from asyncio import CancelledError

from app.logger import log
from app.model import settings
from app.model.repositories.pns_repository import PnsRepository
from app.model.repositories.shedule_repository import ScheduleRepository
from app.model.schemas.user_shcema import User
from app.model.services.lesson_manager import LessonManager
from app.model.services.zoom_service import ZoomService
from app.model.utils import common_utils as utils
from app.model.utils.selenium_manager import SeleniumManager


class Run:

    running = False
    main_task = None
    tasks = []
    error = False

    @classmethod
    async def run(cls):
        web_driver = None
        zoom = None

        user = User()
        log.info('спроба запуску сценарію...')
        try:
            if not utils.check_installed_app(settings.FIREFOX_PATHS):
                log.error('не знайдено браузер Firefox')
                return

            if not user.login:
                log.debug('логін користувача не заповнено')
                return

            password = user.password
            schedule_url = user.schedule_url

            if not password:
                user.clear()
                return
            if not schedule_url:
                log.error('немає посилання для розкладу')
                return

            utils.prevent_sleep()
            selenium_manager = SeleniumManager()

            try:
                schedule = ScheduleRepository(schedule_url).generate_schedule()
            except AttributeError:
                log.error('не вдалося отримати розклад з сайту')
                return

            if not schedule:
                log.info('на сьогодні пар немає, відпочиваємо')
                return

            log.debug('запуск браузера...')
            web_driver = await selenium_manager.driver
            log.debug('браузер було запущено')


            zoom = ZoomService(web_driver)
            pns = PnsRepository(username=user.login, password=password, web_driver=web_driver)
            am = LessonManager(pns, zoom, schedule)

            t1 = asyncio.create_task(am.zoom_meet_processing(), name="zoom_meet_processing")
            t2 = asyncio.create_task(am.attendance_processing(), name="attendance_processing")
            cls.tasks = [t1, t2]

            try:
                results = await asyncio.gather(*cls.tasks, return_exceptions=True)


                for i, result in enumerate(results):
                    task_name = Run().tasks[i].get_name()
                    if isinstance(result, Exception):
                        Run().error = True
                        log.error(f'задача {task_name} завершилась с ошибкой: {result}')
                        if isinstance(result, CancelledError):
                            log.warning(f'задача {task_name} была отменена')
                        else:
                            log.exception(f'необработанная ошибка в задаче {task_name}', exc_info=result)
                        Run().error = True
                    else:
                        log.info(f'задача {task_name} завершилась успешно')



            except asyncio.CancelledError:
                log.warning('було прервано головний потік')
                for task in cls.tasks:
                    task.cancel()
                await asyncio.gather(*cls.tasks, return_exceptions=True)
                raise

        except CancelledError:
            log.warning('було преравно виконання сценарію')
        except Exception:
            cls.error = True
            log.exception('невідома помилка при запуску/виконанні сценарію')
        finally:

            log.info('завершуємо роботу сценарію...')

            if web_driver: 
                web_driver.quit()

            if user.auto_off:
                log.info('відключення ПК відбудеться через 5 хвилин')
                utils.system_off()
                # os.system('shutdown /s /f /t 300')
            else:
                log.warning('автоматичне виключення ПК не увімкнено')
                utils.allow_sleep()

            cls.running = False
            time.sleep(2)
            if zoom:
                await zoom.kill()
                time.sleep(8)
                await zoom.kill()

            if not cls.error:
                log.info('сценарій було завершено без помилок')
            else:
                log.info("сценарій було завершено з помилками")

    @classmethod
    async def start(cls):
        try:
            if not cls.running:
                cls.running = True
                cls.main_task = asyncio.create_task(cls.run())
                await cls.main_task                         # TODO: ВИКЛЮЧНО ДЕБАГ РЕЖИМ
            else:
                log.info('сценарій вже запущено')
        except Exception:
            log.exception("невідома помилка при старті")

    @classmethod
    async def stop(cls):
        if cls.running and cls.main_task:
            log.warning('зупинка сценарію...')
            cls.main_task.cancel()
            try:
                await cls.main_task
            except asyncio.CancelledError:
                pass
            log.info("сценарій було успішно зупинено")
            cls.running = False

asyncio.run(Run().start())
