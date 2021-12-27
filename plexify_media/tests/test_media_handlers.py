import pytest
import os

from .mocks import MockCliArgs, MediaHandlerMock
from .res.res import get_test_input_location, get_test_output_location
from ..media_handlers import MovieHandler


class TestMovieMediaHandler:
    @pytest.fixture(name='cli_args')
    def cli_args_fixture(self):
        yield MockCliArgs(
            download_location=os.path.join(
                os.path.join(get_test_input_location(), 'movies', 'Jungle.Cruise.2021.1080p.WEB.H264-TIMECUT')
            ),
            torrent_name='Jungle.Cruise.2021.1080p.WEB.H264-TIMECUT',
            torrent_kind='multi',
            subtitles=[],
            plex_location=get_test_output_location(),
            label='movie',
        )

    @pytest.fixture(name='media_handler')
    def media_handler_fixture(self, cli_args):
        yield MovieHandler(cli_args)

    @pytest.fixture(name='run_media_handler')
    def run_media_handler_fixture(self, media_handler):
        media_handler.run()

        yield

        # TODO: clean up any produced output

    def test_correct_folder_is_made_in_output_locations(self, run_media_handler):
        assert os.path.isdir(os.path.join(get_test_output_location(), 'movie'))
