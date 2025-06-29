import logging
import sys
from colorama import Back, Fore, Style, init

init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE + Style.BRIGHT,
        logging.INFO: Fore.GREEN + Style.BRIGHT,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT,
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.CRITICAL: Fore.WHITE + Back.RED + Style.BRIGHT,
    }

    def format(self, record):
        record.levelname = record.levelname.center(8)
        record.module += ".py"
        log_message = super().format(record)
        level_color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        return f"{level_color}{log_message}{Style.RESET_ALL}"

def setup_colored_logging(app_debug_level=logging.DEBUG, third_party_level=logging.WARNING):
    formatter = ColoredFormatter(
        fmt='[%(asctime)s] |%(levelname)8s| line:%(lineno)-4d| %(module)-25s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_formatter = logging.Formatter(
        fmt='[%(asctime)s] |%(levelname)8s| line:%(lineno)-4d| %(module)-25s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setFormatter(file_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(third_party_level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # third_party_loggers = [
    #     'selenium',
    #     'urllib3',
    #     'requests',
    #     'connectionpool',
    #     'selenium.webdriver.remote.remote_connection',
    #     'selenium.webdriver.common.service',
    # ]
    
    # for logger_name in third_party_loggers:
    #     logging.getLogger(logger_name).setLevel(third_party_level)

    return root_logger

def get_app_logger(name):
    """
    Получить логгер для вашего приложения с debug уровнем
    
    Args:
        name: Имя модуля (обычно __name__)
    
    Returns:
        logging.Logger: Настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Ваше приложение может использовать DEBUG
    return logger

# Настройка логирования
setup_colored_logging()

# Создание логгера для вашего приложения
log = get_app_logger(__name__)

if __name__ == "__main__":
    log.debug("Це debug повідомлення")
    log.info("Це info повідомлення") 
    log.warning("Це warning повідомлення")
    log.error("Це error повідомлення")
    log.critical("Це critical повідомлення")
