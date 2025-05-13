# common.py
import os
import boto3
import base64

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_V1")
SECRET_KEY = os.environ.get("AWS_SECRET_KEY_V1")
REGION = "eu-north-1"

ec2 = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

def key_pair_exists(key_name):
    try:
        ec2.describe_key_pairs(KeyNames=[key_name])
        return True
    except ec2.exceptions.ClientError:
        return False


def get_base64_user_data(script_path):
    with open(script_path, 'r') as f:
        return base64.b64encode(f.read().encode('utf-8')).decode('utf-8')

def read_user_data(user_data_path):
    with open(user_data_path, 'r') as file:
        return base64.b64encode(file.read().encode()).decode()


def read_user_data_v2(user_data_path):
    with open("shell/simple.sh", "rb") as f:
        user_data_base64 = base64.b64encode(f.read()).decode("utf-8")
