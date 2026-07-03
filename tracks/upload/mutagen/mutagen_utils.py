import tempfile
import os
from django.conf import settings
from chats.r2_utils import get_r2_client


def extract_track_metadata(r2_key):
    """
    Download the file from R2 and extract artist/title using mutagen.
    Returns dict with 'name' and 'artist', or empty strings on failure.
    """
    name = ""
    artist = ""
    tmp = None
    try:
        client = get_r2_client()
        tmp = tempfile.NamedTemporaryFile(delete=False)
        client.download_file(settings.R2_BUCKET_NAME, r2_key, tmp.name)
        tmp.close()

        from mutagen import File as MutaFile
        audio = MutaFile(tmp.name)
        if audio is not None:
            tags = audio.tags
            if tags:
                if 'TIT2' in tags:
                    name = str(tags['TIT2'].text[0])
                elif 'title' in [str(k).lower() for k in tags.keys()]:
                    name = str(list(tags.values())[0])
                if 'TPE1' in tags:
                    artist = str(tags['TPE1'].text[0])
    except Exception:
        pass
    finally:
        if tmp and os.path.exists(tmp.name):
            os.unlink(tmp.name)
    return {"name": name or "", "artist": artist or ""}
