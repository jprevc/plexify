Plexify
====================

Plexify is a CLI program, which can be used to automatically arrange media files 
to Plex media library.

Installation
----------------
```bash
git clone https://github.com/jprevc/plexify.git
python -m setup install
```

Then, test that plexify has been installed properly by running:
```bash
plexify --version
```

Integration with uTorrent, BitTorrent
----------------------------------------
Open Options -> Preferences -> Advanced -> Run Program

Under "Run this program when a torrent finishes:", type:
```bash
plexify --torrent_name "%F" --torrent_kind "%K" --label "%L" --download_location "%D" --plex_location {path to plex}
```

Integration with qBitTorrent
-------------------------------
Open Tools -> Options

In Download toolbar, under "Run external program on torrent completion", type:
```bash
plexify --label "%L" --download_location "%F" --plex_location {path to plex}
```

Logging
---------
When calling plex, you can optionally add additional --log option, where you can specify the path to log file, 
to which log messages will be written each time the program is run. You can add --verbose switch, to make messages 
more verbose.  

Media labeling
-------------------
When adding a new torrent, make sure to label it. This will tell program which media handler it needs to run when 
torrent finishes downloading. For example, labeling a torrent with "show" will make it run 
ShowHandler (which will arrange media files to "Season" folder), labeling a torrent with 'movie', will make it run 
MovieHandler (which will add year of release to folder name). 
