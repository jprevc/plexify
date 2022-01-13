"""
Contains mock classes which can be used for testing media handlers.
"""

from typing import List, Union
from dataclasses import dataclass

from pathlib import Path


@dataclass
class MockCliArgs:
    """
    CLI arguments mock class.
    """

    download_location: Union[str, Path]
    torrent_name: str
    torrent_kind: str
    subtitles: List[str]
    plex_location: Union[str, Path]
    label: str
    use_download_folder_as_label: bool
    verbose: bool
    log: Union[str, Path]
