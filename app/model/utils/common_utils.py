import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

import aiohttp
from dotenv import find_dotenv, load_dotenv

from app.logger import log

load_dotenv(find_dotenv())

async def get_kyiv_now(format_datetime=False) -> str | datetime:
    log.info("Запит на київський час...")

    _cached_time = ""
    _last_fetched = ""
    today = datetime.today() #  час девайсу по UTC

    if _cached_time and _last_fetched and datetime.now(UTC) - _last_fetched < timedelta(minutes=1):
        log.debug("використовується кешований час")
        if format_datetime:
            return datetime.strptime(_cached_time, "%Y-%m-%d %H:%M:%S")
        return _cached_time

    url = (
        f"http://api.timezonedb.com/v2.1/get-time-zone?"
        f"key={os.getenv('TOKEN_TIMEZONE')}&format=json&by=zone&zone=Europe/Kyiv"
    )
    try:
        async with aiohttp.ClientSession() as session:
            log.debug("надсилання запиту до сервера...")
            response = await session.get(url)


            data = await response.json()

            if response.status == 200 and response.content_type == "application/json":
                log.debug("відповідь від серверу успішна")

                if data["status"] == "OK":
                    _cached_time = data["formatted"]
                    _last_fetched = datetime.now(UTC)

                    log.info("київський час отримано")
                    if format_datetime:
                        return datetime.strptime(_cached_time, "%Y-%m-%d %H:%M:%S")
                    return _cached_time
                else:
                    log.warning("отримано помилку від API: %s", data["message"])
                    log.error(data)
                    log.warning("використовується час девайсу...")

                    if format_datetime:
                        return today
                    return today.strftime("%Y-%m-%d %H:%M:%S")

            else:
                log.error("помилка від серверу з повідомленням %r", data["message"])
                log.warning("використовуємо час девайсу...")

                if format_datetime:
                    return today
                return today.strftime("%Y-%m-%d %H:%M:%S")

    except Exception:
        log.exception("невідома помилка під час отримання київського часу")

    if _cached_time:
        log.info("повернення закешованого часу")
        if format_datetime:
            return datetime.strptime(_cached_time, "%Y-%m-%d %H:%M:%S")
        return _cached_time
    else:
        if format_datetime:
            return today
        return today.strftime("%Y-%m-%d %H:%M:%S")
    
def check_installed_app(paths: list[str]) -> str:
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    return ""

def prevent_sleep() -> bool:
    ...

def allow_sleep() -> bool:
    ...

def system_off(through=300) -> bool:
    ...
    