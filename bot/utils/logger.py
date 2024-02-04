import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_dir='logs', max_log_size=10*1024*1024, backup_count=5):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, f'{name}.log'),
        maxBytes=max_log_size,
        backupCount=backup_count
    )
    file_handler.setFormatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
