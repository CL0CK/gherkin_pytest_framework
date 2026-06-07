import os
import sys
import codecs
from loguru import logger

os.makedirs("logs", exist_ok=True)

logger.remove()
logger.add(
    codecs.getwriter("utf-8")(sys.stdout.buffer),
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{message}</cyan>",
)
logger.add(
    "logs/test_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="DEBUG",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | "
           "{level: <8} | "
           "{message}",
)


def get_logger():
    return logger
