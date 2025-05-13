#!/bin/bash
set -e

# Update & Install Dependencies
sudo apt update && sudo apt install -y ffmpeg awscli python3-pip
pip3 install requests boto3

# Set Environment Variables
export S3_BUCKET="my-bucket"
export FILE_NAME="{FILE_NAME}"
export DJANGO_API_URL="https://mybackend.com"

# Download Processing Script
aws s3 cp s3://my-bucket/scripts/process_video.py /tmp/process_video.py
chmod +x /tmp/process_video.py

# Run Processing Script with the File Name
python3 /tmp/process_video.py "$S3_BUCKET" "$FILE_NAME" "$DJANGO_API_URL"

# Shutdown instance after processing
shutdown -h now
