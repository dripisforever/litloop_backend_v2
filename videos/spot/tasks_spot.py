from celery import shared_task
import boto3
import os

from videos.spot.v2.create_key_pair import create_or_use_key_pair
from videos.spot.v2.create_launch_template import create_launch_template
from videos.spot.v2.create_fleet import launch_fleet

KEY_NAME = "spot-key-pair-v5"
TEMPLATE_NAME = "ffmpeg-spot-template"
REGION = "eu-north-1"

launch_template_name = "ffmpeg-spot-template"
ami_id = "ami-0c1ac8a41498c1a9c"
instance_type = "t3.medium" # "c7i.2xlarge"
security_group_id = "sg-0dd82ea97c83ebd86"
USER_DATA_PATH = os.path.join(os.path.dirname(__file__), "user_data.sh")

@shared_task
def launch_spot_instances_v1(key_name=KEY_NAME, template_name=TEMPLATE_NAME, user_data_path=USER_DATA_PATH):
    # Check for key pair and create if necessary
    key_name = create_or_use_key_pair(key_name)

    # Create launch template
    launch_template_id = create_launch_template(
        TEMPLATE_NAME,
        key_name,
        USER_DATA_PATH,
        ami_id,
        instance_type,
        security_group_id
    )

    # Create Spot Fleet request
    fleet_id = launch_fleet(launch_template_id)

    return f"Spot Fleet requested successfully with ID: {fleet_id}"
