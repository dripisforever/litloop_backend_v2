import boto3
from django.conf import settings

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)
bucket_name = settings.AWS_STORAGE_BUCKET_NAME

def multipart_upload(file_obj, key, content_type):
    # 1. Initiate multipart upload
    mpu = s3.create_multipart_upload(Bucket=bucket_name, Key=key, ContentType=content_type)
    upload_id = mpu['UploadId']
    parts = []
    part_number = 1
    chunk_size = 5 * 1024 * 1024  # 5 MB

    try:
        while True:
            data = file_obj.read(chunk_size)
            if not data:
                break

            part = s3.upload_part(
                Bucket=bucket_name,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=data
            )
            parts.append({'ETag': part['ETag'], 'PartNumber': part_number})
            part_number += 1

        # 3. Complete upload
        s3.complete_multipart_upload(
            Bucket=bucket_name,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
    except Exception as e:
        s3.abort_multipart_upload(Bucket=bucket_name, Key=key, UploadId=upload_id)
        raise e
