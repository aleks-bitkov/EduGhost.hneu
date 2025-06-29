from pathlib import Path

from selenium.webdriver.firefox.options import Options as FirefoxOptions

BASE_DIR = Path.cwd()
MODEL_DIR = BASE_DIR.joinpath('app', 'model')
DATA_DIR = MODEL_DIR.joinpath('data')
DRIVER_FILE = MODEL_DIR.joinpath('drivers', 'geckodriver')


PROFILE_JSON = DATA_DIR.joinpath('profile.json')
LINKS_JSON = DATA_DIR.joinpath('links.json')

MAPPED_TYPE_LESSON = {
    "лекція": "lecture",
    "практ.зан.": "practice",
    "лаб.зан.": "laboratory"
}

MONTH_MAP = {
    "January": "січня",
    "February": "лютого",
    "March": "березеня",
    "April": "квітня",
    "May": "травеня",
    "June": "червня",
    "July": "липня",
    "August": "серпня",
    "September": "вересня",
    "October": "жовтня",
    "November": "листопада",
    "December": "грудня",
}

#  конфігураця для Firefox
DEFAULT_PATHS_FIREFOX = [
    #  Шляхи за замовчуванням у Windows
    r"C:\Program Files\Mozilla Firefox\firefox.exe",

    #  Шляхи за замовчуванням Linux
    "/usr/bin/firefox",

    #  Шляхи за замовчуванням MacOS
    ...
]

FIREFOX_PATHS = DEFAULT_PATHS_FIREFOX #  TODO: кастомний шлял для застосунку

FIREFOX_OPTIONS = FirefoxOptions()
FIREFOX_OPTIONS.set_preference("network.protocol-handler.external.zoommtg", True)
FIREFOX_OPTIONS.set_preference("network.protocol-handler.expose.zoommtg", True)
FIREFOX_OPTIONS.set_preference("network.protocol-handler.warn-external.zoommtg", False)
# FIREFOX_OPTIONS.add_argument("--headless")


#  конфігурація для Zoom

DEFAULT_PATHS_ZOOM = [
    #  Шляхи за замовчуванням у Windows
    Path.home() / "AppData" / "Roaming" / "Zoom" / "bin" / "Zoom.exe",
    Path.home() / "AppData" / "Roaming" / "Zoom" / "bin" / "zoom.exe",

    #  Шляхи за замовчуванням Linux
    "/snap/bin/zoom-client",

    #  Шляхи за замовчуванням MacOS
    ...
]

ZOOM_PATHS = DEFAULT_PATHS_ZOOM #  TODO: кастомний шлял для застосунку
