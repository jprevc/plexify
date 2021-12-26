"""
This script can be used to automatically "plexify" media files, which can then be properly shown on plex media server.
"""

import argparse
import sys
import os

import plexify_media.media_handler_functions as mhf


def main():
    """
    Main program entry point.
    """
    # parse input arguments
    parser = argparse.ArgumentParser(description="Process arguments passed by torrent client")
    parser.add_argument("--torrent_name", help="name of torrent")
    parser.add_argument("--torrent_kind", help='kind of torrent, can either be "single" or "multi"')
    parser.add_argument("--label", help="label given to downloaded media")
    parser.add_argument("--download_location", help="location of downloaded media")
    parser.add_argument("--plex_location", help="location of plex media storage")

    args = parser.parse_args()

    # write input parameter values to file for debug purposes
    with open(os.path.join(args.plex_location, "plexify_debug.txt"), "a", encoding='utf-8') as dbg_file:
        debug_str = f"label={args.label}, torrent_name={args.torrent_name}, torrent_kind={args.torrent_kind}, " \
                    f"download_location={args.download_location}, plex_location={args.plex_location}\n"
        dbg_file.write(debug_str)

    # if any of parameters was not provided, stop the program and don't do anything
    if not all([args.label, args.download_location, args.plex_location]):
        sys.exit(0)

    # entries in label should be split by _ (ex. movie_sub)
    label_lst = args.label.split("_")

    media_handler_functions = {
        "movie": mhf.movie_handler,
        "show": mhf.show_handler,
        "video": mhf.video_handler,
        "music": mhf.music_handler,
        "image": mhf.image_handler,
    }

    if label_lst[0] not in media_handler_functions:
        raise RuntimeError(f"Label value {label_lst[0]} was not recognised.")

    # call appropriate handler according to media label that was given when downloading a torrent
    media_handler = media_handler_functions[label_lst[0]]
    media_handler(args)


if __name__ == "__main__":
    main()
