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
import argparse

from babelfish import Language
import subliminal as sbl


def label_to_media_handler_map():
    """
    Returns dictionary (map) which maps labels (specified as label attribute in each media handler implementation)
    to media handler classes.
    """
    module_classes = list(zip(*inspect.getmembers(sys.modules[__name__], inspect.isclass)))[1]
    media_handler_classes = list(filter(lambda x: issubclass(x, MediaHandlerBase), module_classes))

    return {mh_class.label: mh_class for mh_class in media_handler_classes}


class MediaHandlerBase(ABC):
    """
    Base class for any media handler.
    """

    def __init__(self, cli_args: argparse.Namespace, logger):
        self.cli_args = cli_args
        self.logger = logger

    def run(self):
        """
        Runs media conversion algorithm:

        1) Output folder name is determined from the media name.
        2) Media files are copied to the determined output location.
        3) Any post-processing algorithm is run on the output folder (for example subtitle acquisition)
        """
        if self.cli_args.torrent_name:
            torrent_name = self.cli_args.torrent_name
        else:
            torrent_name = os.path.split(self.cli_args.download_location)[-1]

        # get label according to 'label' and 'use_download_folder_as_label' CLI options
        label = self._get_label()

        # determine output folder location
        output_rel_folder_location = self.get_output_folder_name(torrent_name)
        output_abs_folder_location = os.path.join(self.cli_args.plex_location, label, output_rel_folder_location)
        self.logger.info(f"Determined output location: {output_abs_folder_location}")

        # copy media files to plex
        self.logger.info("Started copying media files to output folder.")
        self.copy_torrent_to_plex(output_abs_folder_location)
        self.logger.info("Media files copied successfully.")

        # run post-processing hook (if implemented)
        try:
            self.post_processing_hook(output_abs_folder_location)
        except BaseException as exc:
            self.logger.exception("Post-processing hook failed.")
            raise exc

    def _get_label(self) -> str:
        label = self.cli_args.label

        if self.cli_args.use_download_folder_as_label:
            download_location_folder = os.path.split(self.cli_args.download_location)[-1]

            label = download_location_folder

        return label

    @staticmethod
    @abstractmethod
    def get_output_folder_name(torrent_name: str) -> str:
        """
        Returns output folder name for media files.
        """

    def post_processing_hook(self, output_folder_path: str):
        """
        Post-processing algorithm, which will be called after media files have been moved to output location.
        """

    def copy_torrent_to_plex(self, output_folder_path: str):
        """
        Copies downloaded torrent to plex location.
        """
        download_location = self.cli_args.download_location
        torrent_kind = self.cli_args.torrent_kind
        use_download_folder_as_lab = self.cli_args.use_download_folder_as_label
        output_path = output_folder_path

        # in case torrent_kind is provided or use_download_folder_as_lab is selected, download location is determined
        # by combining download path with torrent name
        if (torrent_kind and torrent_kind == "single") or use_download_folder_as_lab:
            download_location = os.path.join(download_location, self.cli_args.torrent_name)

        if os.path.isdir(download_location):
            copy_handler = copy_tree
        else:
            copy_handler = copyfile

            # in case media is a single file, we need to determine source location for copying by combining file name
            # with generated output folder name
            output_path = os.path.join(output_folder_path, str(download_location.split(os.sep)[-1]))

            # in case media is not a directory, we need to explicitly create directory structure, otherwise copyfile
            # won't work
            self._make_dir_structure(output_folder_path)

        copy_handler(download_location, output_path)

    @staticmethod
    def _make_dir_structure(path):
        try:
            os.makedirs(path)
        except OSError:
            # exception is raised if folder already exists, ignore it
            pass

    @property
    @abstractmethod
    def label(self):
        """
        Specifies label, to which this handler will be matched.
        """

    @staticmethod
    def _remove_clutter_from_string(inp_str):
        return re.sub("[\(\[].*?[\)\]]", "", inp_str).strip()


class MovieHandler(MediaHandlerBase):
    """
    Handler for movie files.
    """

    label = "movie"

    @staticmethod
    def get_output_folder_name(torrent_name: str) -> str:
        # parse movie name and year from torrent name
        movie_name, movie_year = MovieHandler._get_movie_name_and_year(torrent_name)

        movie_name = MovieHandler._remove_clutter_from_string(movie_name)

        # create output folder names and path to which movie will be copied
        output_movie_folder_name = f"{movie_name} ({movie_year})"

        return output_movie_folder_name

    def post_processing_hook(self, output_folder_path: str):
        download_subtitles(output_folder_path, self.cli_args.subtitles)

    @staticmethod
    def _get_movie_name_and_year(torrent_name: str):
        match = re.match(r"(.*?)(\d{4})", torrent_name)
        name = match[1].replace(".", " ").replace("-", "").replace("_", "").strip()
        year = match[2]

        return name, year


class ShowHandler(MediaHandlerBase):
    """
    Handler for shows video files.
    """

    label = 'show'

    @staticmethod
    def get_output_folder_name(torrent_name: str) -> str:
        # parse show name and season number from torrent name
        show_name, season = ShowHandler._get_show_name_and_season(torrent_name)

        show_name = ShowHandler._remove_clutter_from_string(show_name)

        # create output folder names and path to which show videos will be copied
        output_show_folder_path = os.path.join(show_name, "Season " + season)

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

    label = 'default'

    @staticmethod
    def get_output_folder_name(torrent_name: str) -> str:
        return torrent_name


def download_subtitles(video_folder: str, languages: List[str]):
    """
    Downloads best found slovenian and english subtitles for every video file in video folder.
    """

    # scan video folder for video files
    videos = sbl.scan_videos(video_folder, age=timedelta(days=2))

    # download specified subtitles for all found videos
    subtitles = sbl.download_best_subtitles(set(videos), {Language(lang_code) for lang_code in languages})

    # save subtitles next to the videos
    for video in videos:
        sbl.save_subtitles(video, subtitles[video])
