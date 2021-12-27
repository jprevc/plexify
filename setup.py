from setuptools import setup

setup(
    name="PlexifyMedia",
    version="2.0.0",
    description="Copy and arrange media files to Plex home server",
    author="jprevc",
    author_email="jost.prevc@gmail.com",
    packages=["plexify_media"],
    install_requires=["subliminal", "babelfish"],
    scripts=["plexify_media/plexify.py"],
    entry_points={"console_scripts": ["plexify=PlexifyMedia.plexify:main"]},
)
