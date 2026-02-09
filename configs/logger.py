import logging
import sys

# Настройка формата: Время - Имя логгера - Уровень - Сообщение
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DT_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(level: int | str) -> None:

    # 1. Обработчик для вывода в консоль (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DT_FORMAT))

    # 2. Обработчик для записи в файл (для дебага после деплоя)
    file_handler = logging.FileHandler("app_debug.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DT_FORMAT))
    handlers = [console_handler, file_handler]

    logging.basicConfig(
        level=level,
        handlers=handlers,
    )
    quiet_libraries = [
        "telethon",
    ]

    for lib in quiet_libraries:
        logging.getLogger(lib).setLevel(logging.WARNING)
