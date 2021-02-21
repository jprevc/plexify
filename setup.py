from setuptools import setup

setup(
    name="PlexifyMedia",
    version="1.1",
    description="Copy and arrange media files to Plex home server",
    author="jprevc",
    author_email="jost.prevc@gmail.com",
    packages=['PlexifyMedia'],
    install_requires=['subliminal', 'babelfish'],

    scripts=['PlexifyMedia/plexify.py'],
    entry_points={
        'console_scripts': ['plexify=PlexifyMedia.plexify:main']
    }

)
