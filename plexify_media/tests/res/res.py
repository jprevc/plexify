"""
Contains some helper methods to obtain resource files.
"""

import os


def get_resources_location() -> str:
    """
    Returns path to resources folder.
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_test_input_location() -> str:
    """
    Returns path to 'test_input' folder.
    """
    return os.path.join(get_resources_location(), 'test_input')
