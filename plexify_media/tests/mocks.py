from typing import List
from dataclasses import dataclass

from ..media_handlers import MediaHandlerBase


@dataclass
class MockCliArgs:
    download_location: str
    torrent_name: str
    torrent_kind: str
    subtitles: List[str]
    plex_location: str
    label: str


class MediaHandlerMock(MediaHandlerBase):

    label = 'mock'

    def get_output_folder_name(self) -> str:
        pass

