import logging


def initialiser_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)

    if len(logger.handlers) == 2:
        return logger

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")

    file_handler.setLevel(logging.WARNING)

    logger.addHandler(file_handler)

    return logger


logger = initialiser_logger()
