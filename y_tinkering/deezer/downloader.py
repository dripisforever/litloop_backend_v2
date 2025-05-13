# deezer_dl/downloader.py

from pydeezer import Downloader
from pydeezer.constants import track_formats
from config import deezer, DOWNLOAD_DIR

def download_single_track(track_id: str, quality=track_formats.MP3_128):
    track = deezer.get_track(track_id)
    track["download"](DOWNLOAD_DIR, quality=quality)

def download_multiple_tracks(track_ids: list, quality=track_formats.MP3_320, concurrent_downloads=2):
    downloader = Downloader(
        deezer=deezer,
        track_ids=track_ids,
        download_dir=DOWNLOAD_DIR,
        quality=quality,
        concurrent_downloads=concurrent_downloads,
    )
    downloader.start()
