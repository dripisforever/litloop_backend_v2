import boto3
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

ec2_client = boto3.client("ec2", region_name=settings.AWS_REGION)

@csrf_exempt
def complete_multipart_upload(request):
    """Finalize multipart upload and start Spot Instance Fleet for FFmpeg processing"""
    if request.method == "POST":
        data = json.loads(request.body)
        file_name = data["file_name"]
        upload_id = data["uploadId"]
        parts = sorted(data["parts"], key=lambda p: p["PartNumber"])

        # Complete multipart upload
        s3_client = boto3.client("s3", region_name=settings.AWS_REGION)
        s3_client.complete_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"videos/{file_name}",
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )

        # Start Spot Fleet for processing
        fleet_id = start_spot_fleet(file_name)

        return JsonResponse({
            "status": "Upload completed",
            "location": f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/videos/{file_name}",
            "fleet_id": fleet_id
        })


def start_spot_fleet(file_name):
    """Request an EC2 Spot Fleet for processing the video"""

    user_data_script = f"""
        #!/bin/bash
        sudo apt update && sudo apt install -y ffmpeg awscli python3-pip
        pip3 install requests boto3

        # Download Python processing script
        aws s3 cp s3://my-bucket/scripts/process_video.py /tmp/process_video.py
        chmod +x /tmp/process_video.py

        # Set environment variables
        export S3_BUCKET="my-bucket"
        export FILE_NAME="{file_name}"
        export DJANGO_API_URL="https://mybackend.com"

        # Run the script
        python3 /tmp/process_video.py

        # Terminate instance when done
        shutdown -h now
    """

    response = ec2_client.create_fleet(
        SpotOptions={"AllocationStrategy": "lowestPrice"},
        TargetCapacitySpecification={"TotalTargetCapacity": 1, "DefaultTargetCapacityType": "spot"},
        LaunchTemplateConfigs=[
            {
                "LaunchTemplateSpecification": {
                    "LaunchTemplateName": settings.EC2_LAUNCH_TEMPLATE_NAME,
                    "Version": "$Latest"
                },
                "Overrides": [
                    {"InstanceType": "t3.micro"},
                    {"InstanceType": "t3.small"},
                    {"InstanceType": "t3.medium"},
                ],
            }
        ],
        UserData=user_data_script
    )

    return response["FleetId"]
