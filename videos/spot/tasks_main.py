# https://chatgpt.com/c/67f3522d-14c4-800c-a198-ef5f5cc2ab7a
import os
import json
from celery import shared_task

from videos.spot.v2.create_key_pair import create_or_use_key_pair
from videos.spot.v2.create_launch_template import create_launch_template
from videos.spot.v2.create_fleet import launch_fleet

KEY_NAME = "spot-key-pair-v5"
TEMPLATE_NAME = "ffmpeg-spot-template"

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_V1")
SECRET_KEY = os.environ.get("AWS_SECRET_KEY_V1")
REGION = "eu-north-1"

launch_template_name = "ffmpeg-spot-template"
ami_id = "ami-0c1ac8a41498c1a9c"
instance_type = "t3.medium" # "c7i.2xlarge"
security_group_id = "sg-0dd82ea97c83ebd86"

USER_DATA_PATH = os.path.join(os.path.dirname(__file__), "user_data.sh")

@shared_task
def launch_spot_instances_v2():
    key_name = create_or_use_key_pair(KEY_NAME)
    launch_template_id = create_launch_template(
        TEMPLATE_NAME,
        key_name,
        USER_DATA_PATH,
        ami_id,
        instance_type,
        security_group_id
    )
    fleet_id = launch_fleet(launch_template_id)

    print("Fleet created:", json.dumps(fleet_id, indent=2))

    print("Done.")

if __name__ == "__main__":
    main()
