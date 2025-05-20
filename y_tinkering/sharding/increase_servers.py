import boto3

ec2_client = boto3.client('ec2', region_name='us-east-1')
asg_client = boto3.client('autoscaling', region_name='us-east-1')

# 1. Create Launch Template with Spot Instances config
launch_template_name = 'litloop-spot-template'

response = ec2_client.create_launch_template(
    LaunchTemplateName=launch_template_name,
    LaunchTemplateData={
        'ImageId': 'ami-0abcdef1234567890',  # your AMI
        'InstanceType': 't3.medium',
        'KeyName': 'your-keypair',
        'SecurityGroupIds': ['sg-0abcdef1234567890'],  # your security group
        'UserData': '''#!/bin/bash
        echo "export SHARD_COUNT=150" >> /etc/environment
        # Add more bootstrap commands here
        ''',
        'InstanceMarketOptions': {
            'MarketType': 'spot',
            'SpotOptions': {
                'MaxPrice': '0.05',  # max spot price in USD (optional)
                'SpotInstanceType': 'one-time',
                'InstanceInterruptionBehavior': 'terminate'
            }
        }
    }
)

launch_template_id = response['LaunchTemplate']['LaunchTemplateId']
print(f"Created Launch Template with ID: {launch_template_id}")

# 2. Create Auto Scaling Group with desired capacity 10
asg_name = 'litloop-spot-asg'

response = asg_client.create_auto_scaling_group(
    AutoScalingGroupName=asg_name,
    LaunchTemplate={
        'LaunchTemplateId': launch_template_id,
        'Version': '$Latest'
    },
    MinSize=10,
    MaxSize=10,
    DesiredCapacity=10,
    VPCZoneIdentifier='subnet-0abc1234,subnet-0def5678',  # your subnets
    Tags=[
        {
            'Key': 'Name',
            'Value': 'litloop-spot-instance',
            'PropagateAtLaunch': True
        }
    ]
)

print(f"Created Auto Scaling Group: {asg_name}")
