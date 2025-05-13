# REFERENCE: https://stackoverflow.com/questions/67386981/ffmpeg-python-tracking-transcoding-process
import subprocess as sp
import shlex
import json
from threading import Thread
import time


def progress_reader(procs, q):
    while True:
        if procs.poll() is not None:
            break  # Break if FFmpeg sun-process is closed

        progress_text = procs.stdout.readline()  # Read line from the pipe

        # Break the loop if progress_text is None (when pipe is closed).
        if progress_text is None:
            break

        progress_text = progress_text.decode("utf-8")  # Convert bytes array to strings

        # Look for "frame=xx"
        if progress_text.startswith("frame="):
            frame = int(progress_text.partition('=')[-1])  # Get the frame number
            q[0] = frame  # Store the last sample


# Build synthetic video for testing:
sp.run(shlex.split('ffmpeg -y -f lavfi -i testsrc=size=320x240:rate=30 -f lavfi -i sine=frequency=400 -f lavfi -i sine=frequency=1000 -filter_complex amerge -vcodec libx265 -crf 17 -pix_fmt yuv420p -acodec aac -ar 22050 -t 30 input.mp4'))

# Use FFprobe for counting the total number of frames
command = \
    f'ffprobe -v error -select_streams v:0' \
    f'-count_packets -show_entries stream=nb_read_packets'\
    f'-of csv=p=0 -of json input.mp4'

data = sp.run(shlex.split(command), stdout=sp.PIPE).stdout
dict = json.loads(data)  # Convert data from JSON string to dictionary
tot_n_frames = float(dict['streams'][0]['nb_read_packets'])  # Get the total number of frames.

# Execute FFmpeg as sub-process with stdout as a pipe
# Redirect progress to stdout using -progress pipe:1 arguments
cmd = \
    f'ffmpeg -y -loglevel error' \
    f' -i input.mp4 -acodec libvorbis -vcodec libvpx-vp9' \
    f' -crf 20 -pix_fmt yuv420p -progress pipe:1 output.webm'

process = sp.Popen(shlex.split(cmd), stdout=sp.PIPE)

q = [0]  # We don't really need to use a Queue - use a list of of size 1
progress_reader_thread = Thread(target=progress_reader, args=(process, q))  # Initialize progress reader thread
progress_reader_thread.start()  # Start the thread

while True:
    if process.poll() is not None:
        break  # Break if FFmpeg sun-process is closed

    time.sleep(1)  # Sleep 1 second (do some work...)

    n_frame = q[0]  # Read last element from progress_reader - current encoded frame
    progress_percent = (n_frame/tot_n_frames)*100   # Convert to percentage.
    print(f'Progress [%]: {progress_percent:.2f}')  # Print the progress


process.stdout.close()          # Close stdin pipe.
progress_reader_thread.join()   # Join thread
process.wait()
