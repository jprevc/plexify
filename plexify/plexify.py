"""
This script can be used to automatically "plexify" media files, which can then be properly shown on plex media server.
"""

import argparse
import sys
import logging
import plexify.media_handlers as mhf
from plexify.base import version


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


def main():
    """
    Main program entry point.
    """
    # parse input arguments
    parser = argparse.ArgumentParser(description="Process arguments passed by torrent client")
    parser.add_argument("--torrent_name", required=False, help="name of torrent")
    parser.add_argument("--torrent_kind", required=False, help='kind of torrent, can either be "single" or "multi"')
    parser.add_argument("--label", help="label given to downloaded media")
    parser.add_argument("--download_location", help="location of downloaded media")
    parser.add_argument("--plex_location", help="location of plex media storage")
    parser.add_argument("--log", required=False, help="If specified, log messages will be written to this file")
    parser.add_argument("--verbose", action='store_true', required=False, help="Print verbose log messages")
    parser.add_argument("--version", action='store_true', required=False, help="Print version and exit.")
    parser.add_argument(
        "--subtitles",
        action="append",
        required=False,
        default=[],
        help="If specified, program will attempt to find subtitles of the specified language code.",
    )

    args = parser.parse_args()

    logger = get_logger(args.verbose, args.log)

    if args.version:
        print(f"Plexify: {version}")
        sys.exit(-2)

    logger.info(f"Using plexify version: {version}")
    logger.info(f"Started running program with arguments: {args.__dict__}")

    # if any of parameters was not provided, stop the program and don't do anything
    if not all([args.label, args.download_location, args.plex_location]):
        logger.error("Some of the arguments were not provided, exiting...")
        sys.exit(-1)

    # call appropriate handler according to media label that was given when downloading a torrent
    media_handler = mhf.label_to_media_handler_map().get(args.label, mhf.DefaultHandler)
    media_handler(args, logger).run()

    logger.info("Media files handled successfully.")


if __name__ == "__main__":
    main()
