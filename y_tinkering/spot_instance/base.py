# reference: https://chatgpt.com/c/78da8b25-6981-42d3-ad0a-fc1a9ca9c9db
import boto3
import time
import base64

# Initialize the EC2 client
ec2 = boto3.client('ec2')

def get_user_data(script_path):
    with open(script_path, 'r') as file:
        script_content = file.read()
    return base64.b64encode(script_content.encode('utf-8')).decode('utf-8')

# User data scripts
user_data_cassandra = get_user_data('install_cassandra.sh')
user_data_django = get_user_data('install_django.sh')
user_data_celery = get_user_data('install_celery.sh')

# Function to launch a new EC2 Spot Instance
def create_spot_instance(user_data, instance_type):
    spot_instance_request = {
        'LaunchTemplateConfigs': [
            {
                'LaunchTemplateSpecification': {
                    'LaunchTemplateName': 'your-launch-template-name',  # Replace with your launch template name
                    'Version': '$Latest'  # or specify a version
                },
                'Overrides': [
                    {
                        'InstanceType': instance_type,  # Replace with desired instance type
                        'MaxPrice': '0.01',  # Replace with your max price for spot instance
                        'SubnetId': 'subnet-0bb1c79de3EXAMPLE',  # Replace with your subnet ID
                        'UserData': user_data
                    }
                ]
            }
        ],
        'TargetCapacitySpecification': {
            'TotalTargetCapacity': 1,  # Number of instances
            'OnDemandTargetCapacity': 0,
            'SpotTargetCapacity': 1,
            'DefaultTargetCapacityType': 'spot'
        },
        'SpotOptions': {
            'AllocationStrategy': 'lowestPrice',
            'InstanceInterruptionBehavior': 'terminate',  # Or 'stop' if you want to stop the instance
        }
    }

    response = ec2.create_fleet(
        SpotOptions=spot_instance_request['SpotOptions'],
        LaunchTemplateConfigs=spot_instance_request['LaunchTemplateConfigs'],
        TargetCapacitySpecification=spot_instance_request['TargetCapacitySpecification']
    )

    fleet_id = response['FleetId']
    print(f"Spot Fleet Request ID: {fleet_id}")

    return fleet_id

# Function to monitor the state of the instances in the fleet
def monitor_fleet(fleet_id, user_data, instance_type):
    while True:
        # Describe fleet instances
        response = ec2.describe_fleet_instances(FleetId=fleet_id)
        instance_ids = [instance['InstanceId'] for instance in response['ActiveInstances']]

        # Describe the status of instances
        if instance_ids:
            response = ec2.describe_instance_status(InstanceIds=instance_ids)

            for status in response['InstanceStatuses']:
                instance_id = status['InstanceId']
                state = status['InstanceState']['Name']

                if state == 'terminated':
                    print(f"Instance {instance_id} was terminated. Relaunching...")
                    create_spot_instance(user_data, instance_type)

        else:
            print("No active instances found. Relaunching...")
            create_spot_instance(user_data, instance_type)

        time.sleep(60)  # Monitor every 60 seconds

if __name__ == "__main__":
    # Launch Cassandra instance with seed node setup
    fleet_id_cassandra = create_spot_instance(user_data_cassandra, 't3.micro')

    # Launch Django instance
    fleet_id_django = create_spot_instance(user_data_django, 't3.micro')

    # Launch Celery instance
    fleet_id_celery = create_spot_instance(user_data_celery, 't3.micro')

    # Monitor all fleets concurrently
    monitor_fleet(fleet_id_cassandra, user_data_cassandra, 't3.micro')
    monitor_fleet(fleet_id_django, user_data_django, 't3.micro')
    monitor_fleet(fleet_id_celery, user_data_celery, 't3.micro')
