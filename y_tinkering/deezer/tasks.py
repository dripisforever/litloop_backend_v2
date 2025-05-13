# deezer_dl/tasks.py

from celery import shared_task
from config import deezer
from downloader import download_multiple_tracks

@shared_task
def search_and_download(query: str):
    search_data = deezer.search_tracks(query, limit=10)
    track_ids = [track['id'] for track in search_data]
    download_multiple_tracks(track_ids)
