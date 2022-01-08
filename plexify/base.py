import logging

version = "2.1.0"


def get_logger(is_verbose: bool, log_path: str = None):
    """
    Create logger instance.

    :param is_verbose: If True, logger will log also "debug" messages.
    :param log_path: If provided, logger will output messages to this text file.
    """
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG if is_verbose else logging.INFO)

    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

