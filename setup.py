from setuptools import setup
from plexify.base import version

setup(
    name="plexify",
    version=version,
    description="Copy and arrange media files to Plex home server",
    author="jprevc",
    author_email="jost.prevc@gmail.com",
    packages=["plexify"],
    scripts=["plexify/__main__.py"],
    entry_points={"console_scripts": ["plexify = plexify.__main__:main"]},
    install_requires=["subliminal", "babelfish"],
)
