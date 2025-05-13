# create_key_pair.py
from videos.spot.v2.common import ec2, key_pair_exists

def create_or_use_key_pair(key_name):
    if key_pair_exists(key_name):
        print(f"Key pair '{key_name}' already exists.")
        return key_name
    else:
        response = ec2.create_key_pair(KeyName=key_name)
        with open(f"{key_name}.pem", 'w') as f:
            f.write(response['KeyMaterial'])
        print(f"Created and saved key pair '{key_name}.pem'")
        return key_name

# if __name__ == "__main__":
#     create_or_use_key_pair("my-spot-key")
