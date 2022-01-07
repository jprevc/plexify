from setuptools import setup
from plexify_media.base import version

setup(
    name="plexify",
    version=version,
    description="Copy and arrange media files to Plex home server",
    author="jprevc",
    author_email="jost.prevc@gmail.com",
    packages=["plexify"],
    install_requires=["subliminal", "babelfish"],
    scripts=["plexify/plexify.py"],
    entry_points={"console_scripts": ["plexify=plexify.plexify:main"]},
)
