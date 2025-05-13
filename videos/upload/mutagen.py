from mutagen import File

audio = File("yourfile.mp3")

# Common metadata
print(audio.tags)  # shows all metadata
print(audio.get("TIT2"))  # Title
print(audio.get("TPE1"))  # Artist
print(audio.get("TALB"))  # Album

# Duration in seconds
print(audio.info.length)


from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, PictureType
from PIL import Image
from io import BytesIO
import os

def read_artwork(audio_path):
    """Reads and displays artwork from an audio file (MP3)."""
    try:
        audio = MP3(audio_path)
        if 'APIC:' in audio.tags:
            artwork = audio.tags['APIC:'][0].data
            mime_type = audio.tags['APIC:'][0].mime
            print(f"Artwork found in '{os.path.basename(audio_path)}'. MIME type: {mime_type}")
            try:
                image = Image.open(BytesIO(artwork))
                image.show()
            except Exception as e:
                print(f"Error displaying image: {e}")
        else:
            print(f"No artwork found in '{os.path.basename(audio_path)}'.")
    except Exception as e:
        print(f"Error reading audio file '{os.path.basename(audio_path)}': {e}")
