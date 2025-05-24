import boto3
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

s3 = boto3.client(
    "s3",

    aws_access_key_id=settings.AWS_ACCESS_KEY_QALYBAY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_QALYBAY,
    region_name=settings.AWS_REGION_QALYBAY
)

@csrf_exempt
def start_multipart_upload(request):

    file_name = request.GET.get('file_name')

    response = s3.create_multipart_upload(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME_QALYBAY,
        Key=f"videos/{file_name}",
        ContentType="video/mp4"
    )

    return JsonResponse({"upload_id": response["UploadId"]})


@csrf_exempt
def get_presigned_url(request):



    file_name = request.GET.get('file_name')
    upload_id = request.GET.get('upload_id')


    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME_QALYBAY,
            "Key": f"videos/{upload_id}_{file_name}",
            "ContentType": "video/mp4",
        },
        ExpiresIn=3600,  # 1 hour
    )

    return JsonResponse({"presigned_url": presigned_url})

@csrf_exempt
def complete_multipart_upload(request):
    """Finalize multipart upload and start Spot Instance Fleet for FFmpeg processing"""
    if request.method == "POST":
        data = json.loads(request.body)
        file_name = data["file_name"]
        upload_id = data["upload_id"]

        parts = sorted(data["parts"], key=lambda p: p["PartNumber"])



        for part in parts:
            if not part["ETag"].startswith('"'):
                part["ETag"] = f'"{part["ETag"]}"'

        # Complete multipart upload
        # s3_client = boto3.client("s3", region_name='eu-north-1')
        s3.complete_multipart_upload(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME_QALYBAY,
            Key=f"{file_name}",
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )

        # Start Spot Fleet for processing
        # fleet_id = start_spot_fleet(file_name)

        return JsonResponse({
            "status": "Upload completed",
            # "location": f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/videos/{file_name}",
            "location": f"https://litloop-bucket.s3.amazonaws.com/videos/{file_name}",
            # "fleet_id": fleet_id
        })
