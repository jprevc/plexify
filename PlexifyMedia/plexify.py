import argparse
import PlexifyMedia.media_handler_functions as mhf
import sys
import os

def main():
    # parse input arguments
    parser = argparse.ArgumentParser(description='Process arguments passed by torrent client')
    parser.add_argument('--torrent_name', help='name of torrent')
    parser.add_argument('--torrent_kind', help='kind of torrent, can either be "single" or "multi"')
    parser.add_argument('--label', help='label given to downloaded media')
    parser.add_argument('--download_location', help='location of downloaded media')
    parser.add_argument('--plex_location', help='location of plex media storage')

    args = parser.parse_args()

    # write input parameter values to file for debug purposes
    with open(os.path.join(args.plex_location, 'plexify_debug.txt'), 'a') as f:
        debug_str = 'label={}, torrent_name={}, torrent_kind={}, download_location={}, plex_location={}\n'\
            .format(args.label, args.torrent_name, args.torrent_kind, args.download_location, args.plex_location)
        f.write(debug_str)

    # if any of parameters w        as not provided, stop the program and don't do anything
    if not all([args.label, args.download_location, args.plex_location]):
        sys.exit(0)

    # entries in label should be split by _ (ex. movie_sub)
    label_lst = args.label.split('_')

    media_handler_functions = {'movie': mhf.movie_handler,
                               'show': mhf.show_handler,
                               'video': mhf.video_handler,
                               'music': mhf.music_handler,
                               'image': mhf.image_handler}

    if label_lst[0] not in media_handler_functions:
        raise RuntimeError("Label value {} was not recognised.".format(label_lst[0]))

    # call appropriate handler according to media label that was given when downloading a torrent
    media_handler = media_handler_functions[label_lst[0]]
    media_handler(args)


if __name__ == '__main__':
    main()
