import logging
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from photos.models import Photo
from users.auth_utils import jwt_required
from chats.r2_utils import get_r2_client, r2_generate_presigned_url

logger = logging.getLogger(__name__)


@csrf_exempt
@jwt_required
def r2_initiate_photo_upload(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    filename = str(data.get("filename", "unknown"))
    content_type = str(data.get("content_type", "image/jpeg"))
    key = f"photo/{filename}"

    client = get_r2_client()
    try:
        response = client.create_multipart_upload(
            Bucket=settings.R2_BUCKET_NAME,
            Key=key,
            ContentType=content_type
        )
        return JsonResponse({"upload_id": response["UploadId"], "key": key})
    except Exception as e:
        logger.exception("R2 Photo Initiate Failed")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@jwt_required
def r2_get_photo_part_url(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    key = data.get("key")
    upload_id = data.get("upload_id")
    part_number = int(data.get("part_number", 1))

    client = get_r2_client()
    try:
        url = client.generate_presigned_url(
            ClientMethod="upload_part",
            Params={
                "Bucket": settings.R2_BUCKET_NAME,
                "Key": key,
                "UploadId": upload_id,
                "PartNumber": part_number,
            },
            ExpiresIn=3600,
        )
        return JsonResponse({"url": url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@jwt_required
def r2_complete_photo_upload(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    key = data.get("key")
    upload_id = data.get("upload_id")
    parts = data.get("parts")

    client = get_r2_client()
    try:
        client.complete_multipart_upload(
            Bucket=settings.R2_BUCKET_NAME,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        filename = key.split("/")[-1]
        obj = Photo.objects.create(filename=filename, s3_key=key, status='draft', user=request.user)

        album_id = data.get("album_id")
        album_item_id = None
        if album_id:
            try:
                from photos.models import PhotoAlbum
                album = PhotoAlbum.objects.get(id=album_id, user=request.user)
                item = album.add_photo(obj)
                if item:
                    album_item_id = item.id
            except (PhotoAlbum.DoesNotExist, ValueError):
                pass

        return JsonResponse({
            "status": "completed",
            "id": obj.id,
            "album_item_id": album_item_id,
            "location": r2_generate_presigned_url(key, method="GET", expiration=604800)
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
