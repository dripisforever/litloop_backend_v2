import subprocess
import os
import json
from celery import shared_task
from time import sleep
from celery import Celery
from django.conf import settings
from videos.models import Video


@shared_task
def video_encode(duration,video_id):
    try:
        sleep(duration)
        obj = Video.objects.filter(status='Pending',id=video_id).first()
        if obj:
            obj.status = 'Processing'
            obj.is_running = True
            obj.save()

            ###### HLS
            input_video_path = obj.video_file.path

            print(f'input_video_path: {input_video_path}')

            output_directory = os.path.join(os.path.dirname(input_video_path), 'hls_output')

            print(f'output_directory: {output_directory}')
            os.makedirs(output_directory, exist_ok=True)

            output_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '_hls.m3u8'
            output_hls_path = os.path.join(output_directory, output_filename)


            ####### thumb
            input_thumbnail_path = obj.video_file.path
            output_thumbnail_directory = os.path.join(os.path.dirname(input_thumbnail_path))

            os.makedirs(output_thumbnail_directory, exist_ok=True)

            basename_thumb = os.path.basename(input_thumbnail_path)
            output_thumbnail_filename = os.path.splitext(basename_thumb)[0] + '_thumbnail.jpg'
            output_thumbnail_path = os.path.join(output_thumbnail_directory, output_thumbnail_filename)




            # getting video duration/length
            command = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",

                input_video_path
            ]
            result = subprocess.run(command, shell=False,
                                    check=True, stdout=subprocess.PIPE)
            output_json = json.loads(result.stdout)

            video_length = None
            for stream in output_json['streams']:
                if stream['codec_type'] == 'video':
                    video_length = float(stream['duration'])
                    break

            if video_length is not None:
                obj.duration = video_length


            # Use ffmpeg to create HLS segments
            cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-c:v', 'h264',
                '-c:a', 'aac',
                '-hls_time', '5',
                '-hls_list_size', '0',
                # "-hls_base_url", "{{ dynamic_path }}/",
                "-movflags", "+faststart",
                '-y',
                output_hls_path
            ]


            subprocess.run(cmd, check=True)


            # generate

            # files = " ".join([f.media_file.path for f in encodings if f.media_file])
            # cmd = "{0} --segment-duration=4 --output-dir={1} {2}".format(settings.MP4HLS_COMMAND, output_dir, files)

            output_hls_path_v2 = settings.MEDIA_URL + 'videos/hls_output/'+ output_filename
            # generate thumbnail
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-ss', '2',
                '-vframes', '1',
                '-q:v', '2',
                '-y',
                output_thumbnail_path
            ]
            subprocess.run(ffmpeg_cmd, check=True)


            # Update the Video object status to 'Processed' or something similar
            # obj.hls_file = output_hls_path
            obj.hls_file = output_hls_path_v2
            obj.thumbnail = output_thumbnail_path
            obj.status = 'Completed'
            obj.is_running = False
            obj.save()

            print(f'HLS segments generated and saved at: {output_hls_path}')
        else:
            print('No video with status "Pending" found.')
        return True

    except Exception as e:
        print(e)

        return False
