#!/bin/bash
export S3_BUCKET="{S3_BUCKET}"
export FILE_NAME="{FILE_NAME}"
export DJANGO_API_URL="https://mybackend.com"

# Install AWSCLI
sudo apt update -y
sudo apt install unzip curl -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws

# DOWNLOAD
aws s3 cp s3://spot-transcoding/spot_transcoding/main.py /tmp/process_video.py

mkdir /tmp/videos
mkdir /tmp/videos/hls
sudo chmod -R 777 /tmp/videos
# access permission
chmod +x /tmp/process_video.py


python3 -m pip install boto3
# Run Processing Script with the File Name
python3 /tmp/process_video.py "$S3_BUCKET" "$FILE_NAME" "$DJANGO_API_URL"
