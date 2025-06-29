import functools
import json
from collections.abc import Callable

from app.logger import log


def handle_file_errors(operation_name: str, default_return=None):
    """
    Декоратор для обробки помилок файлових операцій

    Args:
        operation_name: назва операції для логування (read, insert, update)
        default_return: повертаеме значення при помилці
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            file_name = ""
            if len(args) > 1:
                file_name = args[1]
            elif "file_name" in kwargs:
                file_name = kwargs["file_name"]

            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                if file_name:
                    log.error("файл %r не знайдено при %s", file_name, operation_name)
                else:
                    log.error("файл не знайдено при %s", operation_name)
                return default_return
            except json.JSONDecodeError:
                if file_name:
                    log.error("невдача декодування файлу %r при %s", file_name, operation_name)
                else:
                    log.error("невдача декодування файлу при %s", operation_name)
                return default_return
            except ValueError:
                if file_name:
                    log.error(
                        "невдача при отримати дані з файлу %r при %s",
                        file_name,
                        operation_name,
                    )
                else:
                    log.error("невдача при отримати даних з файлу при %s", operation_name)
                return default_return
            except Exception:
                if file_name:
                    log.exception("невідома помилка при %s файлу %r", operation_name, file_name)
                else:
                    log.exception("невідома помилка при %s файлу", operation_name)
                return default_return

        return wrapper

    return decorator


@handle_file_errors("читанні", {})
def read(filepath: str, file_name: str = "") -> dict:
    with open(filepath, encoding="utf-8") as file:
        data = file.read()
        if not data or data.strip() == "{}":
            if file_name:
                log.error("файл %s порожній", file_name)
            else:
                log.error("файл порожній")
            return {}
        return json.loads(data)


@handle_file_errors("записі", False)
def write(filepath: str, data: dict, file_name: str = "") -> bool:
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        return True


@handle_file_errors("оновленні", False)
def update(filepath: str, new_data: dict, file_name: str = "") -> bool:
    existing_data = read(filepath, file_name)
    existing_data.update(new_data)
    return write(filepath, existing_data, file_name)
