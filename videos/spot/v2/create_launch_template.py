from .common import ec2, read_user_data
import botocore.exceptions

def create_launch_template(
    template_name,
    key_name,
    user_data_path,
    ami_id,
    instance_type,
    security_group_id
):
    user_data = read_user_data(user_data_path)

    try:
        response = ec2.create_launch_template(
            LaunchTemplateName=template_name,
            LaunchTemplateData={
                'ImageId': ami_id,  # Amazon Linux 2 (example)
                'InstanceType': instance_type,
                'KeyName': key_name,
                'UserData': user_data,
                "SecurityGroupIds": [security_group_id],

                'IamInstanceProfile': {
                    'Arn': 'arn:aws:iam::911167897535:instance-profile/MyEC2SpotFleetRole',
                    # 'Name': 'MyEC2SpotFleetRole'
                },
            }
        )
        template_id = response['LaunchTemplate']['LaunchTemplateId']
        print(f"Created launch template: {template_id}")
        return template_id
    except botocore.exceptions.ClientError as e:
        if 'AlreadyExistsException' in str(e):
            print(f"Launch template {template_name} already exists.")
            existing = ec2.describe_launch_templates(LaunchTemplateNames=[template_name])
            return existing['LaunchTemplates'][0]['LaunchTemplateId']
        else:
            raise
