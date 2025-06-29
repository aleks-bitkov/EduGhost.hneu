import asyncio
import time
from datetime import datetime

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app.logger import log
from app.model import settings
from app.model.utils import common_utils as utils


class PnsRepository:
    def __init__(self, username:str, password:str, web_driver: WebDriver):
        self.__username = username
        self.__password = password
        self.__driver = web_driver
        self.__isLogin = False

    async def login(self):

        if self.__isLogin:
            log.info('вхід вже було виконано')
            return

        log.info('спроба увійти до PNS...')
        try:
            log.debug('спроба отримати сторінку логіну pns...')
            self.__driver.get(settings.PNS_LOGIN_URL)
            log.debug('сторінка логіну було отримано')
        except Exception:
            log.exception('невідома помилка при отримані сторінки логіну pns')
            return

        time.sleep(7) # щоб не стрибати від одного процесу до іншого, конкретно чекаємо

        try:
            log.debug('спроба знайти поле логіну та надіслати значення...')
            self.__driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(self.__username)
            log.debug('вдалося надіслати значення логіну')
            time.sleep(2)
        except Exception:
            log.exception('невідома помилка при надсиланні логіну')
            return

        try:
            log.debug('спроба знайти поле паролю, надіслати значення та "натиснути" Enter...')
            self.__driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.__password + Keys.RETURN)
            log.debug('вдалося надіслати значення паролю та "натиснути" Enter')
            time.sleep(2)
        except Exception:
            log.exception('невідома помилка при вході до PNS')
            return

        self.__isLogin = await self._is_login()
        
        if self.__isLogin:
            log.info('вдалося увійти до PNS')
        else:
            log.error('не вдалося увійти до PNS. невірний логін або пароль')

        return self.__isLogin

    async def put_a_mark(self, url_attendance:str, end):
        is_link = True

        if not self.__isLogin:
            await self.login()

            if not self.__isLogin:
                return

        try:
            log.debug('спроба отримати сторінку для проставлення відмітки...')
            self.__driver.get(url_attendance)
            log.debug('вдалося отримати сторінку з відміткою')
        except Exception:
            log.exception('невідома помилка при отримані сторінки відмітки\nсторінка: %r', url_attendance)
            return

        try:
            link = self.__driver.find_element(By.LINK_TEXT, "Відправити відвідуваність")
            link.click()
        except NoSuchElementException:
            log.warning('кнопку "Відправити відвідуваність" не вдалося знайти одразу')
            is_link = await self.re_mark(url_attendance, end)
        except Exception:
             log.exception('невідома помилка при пошуку посилання "Відправити відвідуваність"')
             return

        if not is_link:
            return

        time.sleep(2)

        try:
            wait = WebDriverWait(self.__driver, 10)
            labels = wait.until(ec.presence_of_all_elements_located((By.TAG_NAME, "label")))

            for label in labels:
                try:
                    input_element = label.find_element(By.TAG_NAME, "input")
                    span_element = label.find_element(By.TAG_NAME, "span")

                    if span_element.text.strip() == "Присутній":
                        input_element.click()
                        break
                except NoSuchElementException:
                    log.debug('пропущено label, не має бути критичним')
                    continue
                except Exception:
                    log.exception('невідома помилка при обробці label')

            time.sleep(2)

            try:
                self.__driver.find_element(By.ID, 'id_submitbutton').click()
                log.info('відмітку про присутність було поставлено')
            except NoSuchElementException:
                log.error('не знайдено кнопки для відмічання присутності')
            except Exception:
                log.exception('невідома помилка при пошуку кнопки для відмічання присутності')
        except NoSuchElementException:
            log.error('не вдалося знайти labels')
        except Exception:
            log.exception('невідома помилка при спробі поставити відвідуваність')

    async def re_mark(self, url:str, end):
        attempt = 1

        log.debug('спроби повторного проставляння відмітки')
        while attempt < 5:
            attempt += 1

            log.info('спробуємо поставити відмітку знов через ~15хвилин')
            await asyncio.sleep(900)  # 15 хвилин
            now_str = await utils.get_kyiv_now()
            now = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")
            dat_end = datetime.strptime(f"{now.strftime('%Y-%m-%d')} {end}", "%Y-%m-%d %H:%M")
            if now >= dat_end:
                log.info('не має сенсу намагатись, оскільки вже пара пропущена')
                break

            log.debug('оновлюємо сторінку...')
            self.__driver.get(url) #  перезавантаження сторінки відмітки
            time.sleep(3) # зупинка потоку, для повного завантаження сторінки
            log.debug('сторінка повинна була оновитися')

            log.info('повторна спроба поставити відмітку (%d/5)', attempt)

            try:
                log.debug('шукаємо знов посилання для відмітки...')
                link = self.__driver.find_element(By.LINK_TEXT, "Відправити відвідуваність")
                log.debug('посилання було знайдено. Спроба натисунти...')
                link.click()
                log.debug('вдалося натиснути на посилання "Відправити відвідуваність"')
                log.info('вдалося знайти кнопку "Відправити відвідуваність"')
                return True
            except NoSuchElementException:
                log.info('невдала спроба, посилання все ще немає')
            except Exception:
                log.exception('при пошуку посилання "Відправити відвідуваність"')

        log.warning('не вдалося знайти посилання. відмітку не проставлено')
        return False

    async def _is_login(self):
        error_class = 'loginerrors' #  на сторінці div з таким класом 

        log.debug('пошук елемента про помилку входу')
        try:
            self.__driver.find_element(By.CLASS_NAME, error_class)
            log.debug('елемент було знайдено')
            return False
        except NoSuchElementException:
            log.debug('елемент незнайдений, скоріше вхід був успішним')
            return True
        except Exception:
            log.exception('невідома помилка при перевірці входу')
