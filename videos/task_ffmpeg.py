# https://chatgpt.com/c/67e288cc-78b0-800c-8218-52f71cbe36ef
import os
import boto3
import subprocess
from celery import shared_task
from django.conf import settings

s3_client = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)

@shared_task
def process_video_to_hls(file_name):
    """Download video, convert to HLS, and upload segments to S3"""
    local_video = f"/tmp/{file_name}"
    local_hls = f"/tmp/{file_name}_hls"

    # Download video from S3
    s3_client.download_file(settings.AWS_STORAGE_BUCKET_NAME, f"videos/{file_name}", local_video)

    # Convert to HLS using FFmpeg
    os.makedirs(local_hls, exist_ok=True)
    hls_output = f"{local_hls}/output.m3u8"

    ffmpeg_cmd = [
        "ffmpeg", "-i", local_video, "-profile:v", "baseline", "-level", "3.0",
        "-start_number", "0", "-hls_time", "10", "-hls_list_size", "0", "-f", "hls", hls_output
    ]

    subprocess.run(ffmpeg_cmd, check=True)

    # Upload HLS files to S3
    for root, _, files in os.walk(local_hls):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = f"hls/{file_name}/{file}"
            s3_client.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

    return f"HLS conversion complete for {file_name}"
