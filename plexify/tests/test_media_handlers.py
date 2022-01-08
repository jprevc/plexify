"""
Contains tests for media handlers.
"""

import os
from typing import List, Callable, Type, Optional

import pytest

from .mocks import MockCliArgs
from .res.res import get_test_input_location, get_resources_location
from ..media_handlers import DefaultHandler, label_to_media_handler_map, MovieHandler, ShowHandler, MediaHandlerBase
from ..base import get_logger


@pytest.fixture(name='make_cli_args')
def make_cli_args_fixture(
    tmp_path: str,
) -> Callable[..., MockCliArgs]:
    """
    Creates factory for CLI arguments object.
    """

    def make_cli_args(
        download_location: str,
        label: str,
        torrent_kind: Optional[str] = None,
        torrent_name: Optional[str] = None,
        subtitles: Optional[List[str]] = None,
    ) -> MockCliArgs:
        if not subtitles:
            subtitles = []

        return MockCliArgs(
            download_location=download_location,
            torrent_name=torrent_name,
            torrent_kind=torrent_kind,
            subtitles=subtitles,
            plex_location=tmp_path,
            label=label,
            log=os.path.join(get_resources_location(), 'test_log.txt'),
            verbose=True,
        )

    return make_cli_args


@pytest.fixture(name='make_media_handler')
def make_media_handler_fixture() -> Callable[[MockCliArgs], MediaHandlerBase]:
    """
    Creates factory for media handler.
    """

    def make_media_handler(cli_args: MockCliArgs) -> MediaHandlerBase:
        logger = get_logger(cli_args.verbose, cli_args.log)
        return label_to_media_handler_map().get(cli_args.label, DefaultHandler)(cli_args, logger)

    return make_media_handler


@pytest.mark.parametrize('label,expected_class', [('movie', MovieHandler), ('show', ShowHandler)])
def test_correct_media_handler_is_returned(label: str, expected_class: Type[MediaHandlerBase]):
    """
    Test that correct media handler is returned according to passed label.
    """
    assert label_to_media_handler_map()[label] == expected_class


@pytest.mark.parametrize(
    'download_location,label,torrent_name,torrent_kind,expected_output_name',
    [
        (
            get_test_input_location(),
            'movie',
            'Jungle.Cruise.2021.1080p.WEB.H264-TIMECUT',
            'multi',
            os.path.join('movie', 'Jungle Cruise (2021)'),
        ),
        (
            os.path.join(get_test_input_location(), 'Jungle.Cruise.2021.1080p.WEB.H264-TIMECUT'),
            'movie',
            None,
            None,
            os.path.join('movie', 'Jungle Cruise (2021)'),
        ),
        (
            get_test_input_location(),
            'movie',
            'Borat.2.Subsequent.Moviefilm.2020.SLOSubs.XviD-metalcamp.avi',
            'single',
            os.path.join('movie', 'Borat 2 Subsequent Moviefilm (2020)'),
        ),
        (
            os.path.join(get_test_input_location(), 'Borat.2.Subsequent.Moviefilm.2020.SLOSubs.XviD-metalcamp.avi'),
            'movie',
            None,
            None,
            os.path.join('movie', 'Borat 2 Subsequent Moviefilm (2020)'),
        ),
        (
            get_test_input_location(),
            'show',
            'Dexter.S09E02.1080p.WEB.H264-GLHF',
            'multi',
            os.path.join('show', 'dexter', 'Season 09'),
        ),
        (
            os.path.join(get_test_input_location(), 'Dexter.S09E02.1080p.WEB.H264-GLHF'),
            'show',
            None,
            None,
            os.path.join('show', 'dexter', 'Season 09'),
        ),
        (
            get_test_input_location(),
            'show',
            'The.Book.of.Boba.Fett.S01E01.1080p.WEB.h264-KOGi.mkv',
            'single',
            os.path.join('show', 'The Book of Boba Fett', 'Season 01'),
        ),
        (
            os.path.join(get_test_input_location(), 'The.Book.of.Boba.Fett.S01E01.1080p.WEB.h264-KOGi.mkv'),
            'show',
            None,
            None,
            os.path.join('show', 'The Book of Boba Fett', 'Season 01'),
        ),
    ],
)
def test_correct_folder_structure_is_made_in_output_location(
    make_cli_args,
    make_media_handler,
    tmp_path,
    download_location: str,
    label: str,
    torrent_name: str,
    torrent_kind: str,
    expected_output_name: str,
):
    """
    Test that correct folder structure is made in output location.
    """
    movie_handler = make_media_handler(make_cli_args(download_location, label, torrent_kind, torrent_name))
    movie_handler.run()

    # check that correct folder structure has been created
    output_folder = tmp_path
    for folder in expected_output_name.split(os.sep):
        output_folder = os.path.join(output_folder, folder)
        assert os.path.isdir(output_folder)


@pytest.mark.parametrize(
    'media_name,media_handler,expected_output',
    [
        ('Jungle.Cruise.2021.1080p.WEB.H264-TIMECUT', MovieHandler, 'Jungle Cruise (2021)'),
        ('Holidate.2020.HDRip.XviD.AC3-EVO', MovieHandler, 'Holidate (2020)'),
        ('South Park Post COVID 2021 720p AMZN WEBRip x264 GalaxyRG', MovieHandler, 'South Park Post COVID (2021)'),
        ('Dexter.S09E01.1080p.WEB.H264-CAKES', ShowHandler, os.path.join('Dexter', 'Season 09')),
        ('RickAndMorty_S05E02', ShowHandler, os.path.join('RickAndMorty', 'Season 05')),
    ],
)
def test_folder_name_is_correctly_determined(
    media_name: str, media_handler: Type[MediaHandlerBase], expected_output: str
):
    """
    Test that folder name is correctly determined from media name.
    """
    folder_name = media_handler.get_output_folder_name(media_name)

    assert folder_name == expected_output
