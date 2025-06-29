import psutil
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from app.logger import log


class ZoomService:

    def __init__(self, web_driver):
        self.__driver = web_driver

    async def join(self, url_zoom:str):
        btn_launch_xpath = '/html/body/div[1]/div[2]/div[2]/div/div[1]/div'
        log.info('спроба зайти на Zoom...')

        try:
            self.__driver.get(url_zoom)
            log.info('вдалося перейти за посиланням')
        except Exception:
            log.exception('невідома помилка при спробі перейти за посиланням до Zoom')

        try:
            self.__driver.find_element(By.XPATH, btn_launch_xpath).click()
            log.info('зайшли на конференцію Zoom')
        except NoSuchElementException:
            log.error('не вдалося знайти кнопку для входу на конференцію в Zoom')
            log.debug('можливо й зайшли, проте це не точно')
            return
        except Exception:
            log.exception('невідома помилка при знаходженні та натискання кнопки')

    @staticmethod
    async def is_running():
        log.debug('спроба отримати pid Zoom...')
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] and 'zoom' in process.info['name'].lower():
                log.debug('pid Zoom було отримано')
                return process.info['pid']
        log.debug('pid Zoom не вдалося отримати')
        return None

    @staticmethod
    async def kill_process_tree(pid):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)  #  Отримуємо усі дочірні процеси
            for child in children:
                child.kill()
            parent.kill()

            log.info('Zoom та його дочірні процеси завершені')
        except psutil.NoSuchProcess:
            log.info('Zoom вже завершено/не запущено')
        except Exception:
            log.exception('невідома помилка при завершені Zoom процесу')

    async def kill(self):
        pid = await self.is_running()
        log.debug('pid Zoom %s', str(pid))
        if pid:
            log.debug('спроба знищити процеси Zoom...')
            await self.kill_process_tree(pid)
        else:
            log.warning('Zoom не було запущено')
