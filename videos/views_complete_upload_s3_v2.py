# https://chatgpt.com/c/67e288cc-78b0-800c-8218-52f71cbe36ef
import boto3
import base64

def get_user_data(s3_bucket, file_name, django_api_url):
    """Read user_data.sh and replace placeholders with actual values"""
    with open("user_data.sh", "r") as f:
        user_data = f.read()

    # Replace placeholders with actual values
    user_data = user_data.replace("{S3_BUCKET}", s3_bucket)
    user_data = user_data.replace("{FILE_NAME}", file_name)
    user_data = user_data.replace("{DJANGO_API_URL}", django_api_url)

    return base64.b64encode(user_data.encode()).decode()

def start_spot_instance(s3_bucket, file_name, django_api_url):
    """Start an EC2 Spot Instance for processing"""
    ec2 = boto3.client("ec2", region_name="us-east-1")

    response = ec2.create_fleet(
        SpotOptions={"AllocationStrategy": "capacity-optimized"},
        TargetCapacitySpecification={"TotalTargetCapacity": 1, "DefaultTargetCapacityType": "spot"},
        LaunchTemplateConfigs=[
            {
                "LaunchTemplateSpecification": {"LaunchTemplateId": "lt-xxxxxxxxxxxxxxxx", "Version": "1"},
                "Overrides": [{"InstanceType": "t3.micro", "SubnetId": "subnet-xxxxxxxx"}]
            }
        ],
        UserData=get_user_data(s3_bucket, file_name, django_api_url)  # Inject values dynamically
    )

    return response
