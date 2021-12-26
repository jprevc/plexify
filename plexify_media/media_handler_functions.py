"""
Contains various media handler functions.
"""

import re
import os
import sys
import inspect
from distutils.dir_util import copy_tree
from shutil import copyfile
from datetime import timedelta
from abc import ABC, abstractmethod
from typing import List

from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, scan_videos


def label_to_media_handler_map():
    module_classes = list(zip(*inspect.getmembers(sys.modules[__name__], inspect.isclass)))[1]
    media_handler_classes = list(filter(lambda x: issubclass(x, MediaHandlerBase), module_classes))

    return {mh_class.label: mh_class for mh_class in media_handler_classes}


class MediaHandlerBase(ABC):
    """
    Base class for any media handler.
    """

    def __init__(self, cli_args):
        self.cli_args = cli_args

    def run(self):
        output_folder_location = self.get_output_folder_location()

        # copy media files to plex
        self.copy_torrent_to_plex(output_folder_location)

        self.post_processing_hook(output_folder_location)

    @abstractmethod
    def get_output_folder_location(self) -> str:
        pass

    def post_processing_hook(self, output_folder_path: str):
        pass

    def copy_torrent_to_plex(self, output_folder_path: str):
        """
        Copies downloaded torrent to plex location.
        """
        if self.cli_args.torrent_kind == "multi":
            copy_tree(self.cli_args.download_location, output_folder_path)
        elif self.cli_args.torrent_kind == "single":
            os.mkdir(output_folder_path)
            copyfile(
                os.path.join(self.cli_args.download_location, self.cli_args.torrent_name),
                os.path.join(output_folder_path, self.cli_args.torrent_name),
            )
        else:
            raise ValueError(f"torrent_kind should either be 'single' or 'multi' and not {self.cli_args.torrent_kind}")

    @classmethod
    @property
    @abstractmethod
    def label(cls):
        pass


class MovieHandler(MediaHandlerBase):
    """
    Handler for movie files.
    """

    @classmethod
    @property
    @abstractmethod
    def label(cls):
        return 'movie'

    def get_output_folder_location(self) -> str:
        # parse movie name and year from torrent name
        movie_name, movie_year = self._get_movie_name_and_year(self.cli_args.torrent_name)

        # create output folder names and path to which movie will be copied
        output_movie_folder_name = f"{movie_name} ({movie_year})"
        output_movie_folder_path = os.path.join(self.cli_args.plex_location, "movies", output_movie_folder_name)

        return output_movie_folder_path

    def post_processing_hook(self, output_folder_path: str):
        download_subtitles(output_folder_path, self.cli_args.subtitles)

    @staticmethod
    def _get_movie_name_and_year(torrent_name: str):
        match = re.match(r"(.*?)(\d{4})", torrent_name)
        name = match[1].replace(".", " ").replace("-", "").replace("_", "").strip()
        year = match[2]

        return name, year


class ShowHandler(MediaHandlerBase):
    @classmethod
    @property
    @abstractmethod
    def label(cls):
        return 'show'

    def get_output_folder_location(self) -> str:
        # parse show name and season number from torrent name
        show_name, season = self._get_show_name_and_season(self.cli_args.torrent_name)

        # create output folder names and path to which show videos will be copied
        output_show_folder_path = os.path.join(self.cli_args.plex_location, "shows", show_name, "Season " + season)

        return output_show_folder_path

    def post_processing_hook(self, output_folder_path: str):
        download_subtitles(output_folder_path, self.cli_args.subtitles)

    @staticmethod
    def _get_show_name_and_season(download_folder: str):
        match = re.match(r"(.*)[S|s](\d{1,2})", download_folder)
        name = match[1].replace(".", " ").replace("-", " ").replace("_", " ").strip()
        season = match[2]

        return name, season


class DefaultHandler(MediaHandlerBase):
    """
    Default media handler.
    """

    @classmethod
    @property
    @abstractmethod
    def label(cls):
        return 'default'

    def get_output_folder_location(self) -> str:
        return os.path.join(self.cli_args.plex_location, self.cli_args.label, self.cli_args.torrent_name)


def download_subtitles(video_folder: str, languages: List[str]):
    """
    Downloads best found slovenian and english subtitles for every video file in video folder.
    """
    # scan video folder for video files
    videos = scan_videos(video_folder, age=timedelta(days=2))

    # download specified subtitles for all found videos
    subtitles = download_best_subtitles(set(videos), {Language(lang_code) for lang_code in languages})

    # save subtitles next to the videos
    for video in videos:
        save_subtitles(video, subtitles[video])
