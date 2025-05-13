# deezer_dl/main.py

from downloader import download_single_track, download_multiple_tracks

if __name__ == "__main__":
    # Download single track
    download_single_track("856558962")

    # Download multiple
    track_ids = [
        "572537082",
        "921278352",
        "927432162",
        "547653622"
    ]
    # download_multiple_tracks(track_ids)
