"""
Contains various media handler functions.
"""

import re
import os
from distutils.dir_util import copy_tree
from shutil import copyfile
from datetime import timedelta

from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, scan_videos


def movie_handler(cli_args):
    """
    Handler for movie files.
    """

    def get_movie_name_and_year(torrent_name):
        match = re.match(r"(.*?)(\d{4})", torrent_name)
        name = match[1].replace(".", " ").replace("-", "").replace("_", "").strip()
        year = match[2]

        return name, year

    # parse movie name and year from torrent name
    movie_name, movie_year = get_movie_name_and_year(cli_args.torrent_name)

    # create output folder names and path to which movie will be copied
    output_movie_folder_name = f"{movie_name} ({movie_year})"
    output_movie_folder_path = os.path.join(cli_args.plex_location, "movies", output_movie_folder_name)

    # copy movie to plex
    copy_torrent_to_plex(
        cli_args.torrent_name, cli_args.torrent_kind, cli_args.download_location, output_movie_folder_path
    )

    # try to find subtitles if it was specified in label
    if "sub" in cli_args.label.split("_"):
        download_subtitles(output_movie_folder_path)


def show_handler(cli_args):
    """
    Handler for shows.
    """

    def get_show_name_and_season(download_folder):
        match = re.match(r"(.*)[S|s](\d{1,2})", download_folder)
        name = match[1].replace(".", " ").replace("-", " ").replace("_", " ").strip()
        season = match[2]

        return name, season

    # parse show name and season number from torrent name
    show_name, season = get_show_name_and_season(cli_args.torrent_name)

    # create output folder names and path to which show videos will be copied
    output_show_folder_path = os.path.join(cli_args.plex_location, "shows", show_name, "Season " + season)

    # copy torrent to plex
    copy_torrent_to_plex(
        cli_args.torrent_name, cli_args.torrent_kind, cli_args.download_location, output_show_folder_path
    )

    # try to find subtitles if it was specified in label
    if "sub" in cli_args.label.split("_"):
        download_subtitles(output_show_folder_path)


def video_handler(cli_args):
    """
    Handler for videos
    """
    default_handler(cli_args, "video")


def music_handler(cli_args):
    """
    Handler for music files.
    """
    default_handler(cli_args, "music")


def image_handler(cli_args):
    """
    Handler for images.
    """
    default_handler(cli_args, "photos")


def default_handler(cli_args, output_folder_name):
    """
    Default media handler.
    """
    output_folder_path = os.path.join(cli_args.plex_location, output_folder_name, cli_args.torrent_name)
    copy_torrent_to_plex(cli_args.torrent_name, cli_args.torrent_kind, cli_args.download_location, output_folder_path)


def download_subtitles(video_folder):
    """Downloads best found slovenian and english subtitles for every video file in video folder"""

    # scan video folder for video files
    videos = scan_videos(video_folder, age=timedelta(days=2))

    # download english and slovenian subtitles for all found videos
    subtitles = download_best_subtitles(videos, {Language("eng"), Language("slv")})

    # save subtitles next to the videos
    for video in videos:
        save_subtitles(video, subtitles[video])


def copy_torrent_to_plex(torrent_name, torrent_kind, download_location, output_folder_path):
    """Copies downloaded torrent to plex location"""
    if torrent_kind == "multi":
        copy_tree(download_location, output_folder_path)
    elif torrent_kind == "single":
        os.mkdir(output_folder_path)
        copyfile(os.path.join(download_location, torrent_name), os.path.join(output_folder_path, torrent_name))
    else:
        raise ValueError(f"torrent_kind should either be 'single' or 'multi' and not {torrent_kind}")
