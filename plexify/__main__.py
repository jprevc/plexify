"""
This script can be used to automatically "plexify" media files, which can then be properly shown on plex media server.
"""

import argparse

from plexify.base import version, get_logger, get_label
import plexify.media_handlers as mhf


def main():
    """
    Main program entry point.
    """
    # parse input arguments
    parser = argparse.ArgumentParser(description="Process arguments passed by torrent client")
    parser.add_argument("--torrent_name", required=False, help="name of torrent")
    parser.add_argument("--torrent_kind", required=False, help='kind of torrent, can either be "single" or "multi"')

    label_group = parser.add_mutually_exclusive_group(required=True)
    label_group.add_argument("--label", help="label given to downloaded media")
    label_group.add_argument(
        "--use_download_folder_as_label",
        action='store_true',
        help="If specified, program will use last folder from download_location as a label. This is useful for some "
        "clients, which can't pass label as an argument.",
    )

    parser.add_argument("--download_location", required=True, help="location of downloaded media")
    parser.add_argument("--plex_location", required=True, help="location of plex media storage")
    parser.add_argument("--log", required=False, help="If specified, log messages will be written to this file")
    parser.add_argument("--verbose", action='store_true', required=False, help="Print verbose log messages")
    parser.add_argument("--version", action='version', version=f"Plexify: {version}", help="Print version and exit.")
    parser.add_argument(
        "--subtitles",
        action="append",
        required=False,
        default=[],
        help="If specified, program will attempt to find subtitles of the specified language code.",
    )

    args = parser.parse_args()

    logger = get_logger(args.verbose, args.log)

    logger.info(f"Using plexify version: {version}")
    logger.info(f"Started running program with arguments: {args.__dict__}")

    # call appropriate handler according to media label that was given when downloading a torrent
    media_handler = mhf.label_to_media_handler_map().get(get_label(args), mhf.DefaultHandler)
    media_handler(args, logger).run()

    logger.info("Media files handled successfully.")


if __name__ == "__main__":
    main()
