ACCESS_KEY=
SECRET_KEY=

# reference: https://stackoverflow.com/q/38049391
def gather_public_ip():
    regions = ['us-west-2', 'eu-central-1', 'ap-southeast-1']
    combined_list = []   ##This needs to be returned

    for region in regions:
        instance_information = [] # I assume this is a list, not dict
        ip_dict = {}
        client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=region,)
        instance_dict = client.describe_instances().get('Reservations')

        for reservation in instance_dict:
            for instance in reservation['Instances']: # This is rather not obvious
               if instance[u'State'][u'Name'] == 'running' and instance.get(u'PublicIpAddress') is not None:

                    ipaddress = instance[u'PublicIpAddress']
                    tagValue = instance[u'Tags'][0][u'Value'] # 'Tags' is a list, took the first element, you might wanna switch this
                    zone = instance[u'Placement'][u'AvailabilityZone']
                    info = ipaddress, tagValue, zone
                    instance_information.append(info)
        combined_list.append(instance_information)
    return combined_list
