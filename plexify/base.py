import logging
import os

version = "2.2.0"


def get_logger(is_verbose: bool, log_path: str = None) -> logging.Logger:
    """
    Create logger instance.

    :param is_verbose: If True, logger will log also "debug" messages.
    :param log_path: If provided, logger will output messages to this text file.

    :return: Logger instance.
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


def get_label(cli_args) -> str:
    """
    Get media label, according to 'label' and 'use_download_folder_as_label' options.

    :return: Media label.
    """
    if cli_args.use_download_folder_as_label:
        return os.path.split(cli_args.download_location)[-1]
    else:
        return cli_args.label
