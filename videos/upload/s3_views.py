import boto3
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from videos.models import Video
from photos.models import Photo
# from tracks.models import TrackV2

s3 = boto3.client("s3", region_name=settings.AWS_REGION)


@api_view(["POST"])
def create_presigned_url(request):
    """
    Step 1: Initiate multipart upload.
    """
    data = request.data
    filename = data["filename"]
    content_type = data["content_type"]

    response = s3.create_multipart_upload(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=filename,
        ContentType=content_type,
    )

    return JsonResponse({
        "upload_id": response["UploadId"],
        "key": response["Key"],
    })


@api_view(["POST"])
def get_presigned_url(request):
    """
    Step 2: Generate a presigned URL for a specific part number.
    """
    data = request.data
    upload_id = data["upload_id"]
    key = data["key"]
    part_number = int(data["part_number"])

    url = s3.generate_presigned_url(
        ClientMethod="upload_part",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": key,
            "UploadId": upload_id,
            "PartNumber": part_number,
        },
        ExpiresIn=3600,
    )

    return JsonResponse({"url": url})


@api_view(["POST"])
def complete_upload(request):
    """
    Step 3: Finalize multipart upload.
    """
    data = request.data
    upload_id = data["upload_id"]
    key       = data["key"]
    parts     = data["parts"]  # [{ PartNumber: 1, ETag: "..." }, ...]

    
    response = s3.complete_multipart_upload(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )
    key = response['Key']
    cloudfront_url = f"https://d3fxu5f9ok11ds.cloudfront.net/{key}"

    # Object.objects.create()
    # https://chatgpt.com/c/68081760-2fc4-800c-8946-98760a9575f5
    # media_type = data["media_type"]
    # model = {"photo": Photo, "video": Video, "track": TrackV2}.get(media_type)
    # if model:
    #     obj = model.objects.create(filename=key.split("/")[-1], s3_key=key)
    #     return JsonResponse({
    #         "status": "completed",
    #         "id": obj.id,
    #         # "location": f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{key}",
    #         "location": cloudfront_url
    #     })

    return JsonResponse({
        "message": "Upload completed successfully",
        "location": cloudfront_url,

        # "location": response["Location"],
        "key": key,
    })
