import copy

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.firefox.service import Service as ServiceFirefox

from app.logger import log
from app.model import settings
from app.model.utils.common_utils import check_installed_app


class SeleniumManager:
    def __init__(self):
        self._driver = None
        self._binary_browser = check_installed_app(settings.FIREFOX_PATHS)

        if not self._binary_browser:
            log.error('не знайдено виконуваний файл браузера')

        self._service = ServiceFirefox(executable_path=settings.DRIVER_FILE)
        self._options = copy.deepcopy(settings.FIREFOX_OPTIONS)
        self._options.binary_location = self._binary_browser
    
    @property
    async def driver(self):
        try:
            if not self._driver:
                self._driver = webdriver.Firefox(
                    service=self._service,
                    options=self._options,

                )
            return self._driver
        except SessionNotCreatedException:
            log.critical('не знайдено застосунок Firefox. Встановіть та/або оновіть шляхи до застосунку')
    
    def is_driver_available(self) -> bool:
        return self._driver is not None
    
    async def close(self):
        if self._driver:
            self._driver.quit()
            self._driver = None
