from videos.spot.v2.common import ec2
from videos.spot.v2.create_launch_template import create_launch_template
from videos.spot.v2.create_key_pair import create_or_use_key_pair

def launch_fleet(launch_template_id):
    response = ec2.create_fleet(
        SpotOptions={
            "AllocationStrategy": "lowestPrice",
            "SingleInstanceType": True,
            "InstanceInterruptionBehavior": "terminate"
        },
        LaunchTemplateConfigs=[
            {


                "LaunchTemplateSpecification": {
                    "LaunchTemplateId": launch_template_id,
                    "Version": "$Latest"
                },
            }
        ],
        TargetCapacitySpecification={
            "TotalTargetCapacity": 1,
            "DefaultTargetCapacityType": "spot",
        },
        Type="instant"
    )
    return response
