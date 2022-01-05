from typing import List, Union
from dataclasses import dataclass

from pathlib import Path

from ..media_handlers import MediaHandlerBase


@dataclass
class MockCliArgs:
    download_location: Union[str, Path]
    torrent_name: str
    torrent_kind: str
    subtitles: List[str]
    plex_location: Union[str, Path]
    label: str
    verbose: bool
    log: Union[str, Path]


class MediaHandlerMock(MediaHandlerBase):

    label = 'mock'

    def get_output_folder_name(self) -> str:
        pass

