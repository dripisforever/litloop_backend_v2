import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chats.r2_utils import r2_upload_file, r2_generate_presigned_url
from users.auth_utils import jwt_required_testable


@csrf_exempt
@jwt_required_testable
def upload_background_image(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No file provided in "image" field.'}, status=400)

    image_file = request.FILES['image']

    if not image_file.content_type.startswith('image/'):
        return JsonResponse({'error': 'File must be an image.'}, status=400)

    ext = os.path.splitext(image_file.name)[1]
    if not ext:
        ext = '.jpg' if image_file.content_type == 'image/jpeg' else '.png'

    filename = f"backgrounds/{request.user.id}_{uuid.uuid4()}{ext}"

    try:
        r2_upload_file(image_file, filename, content_type=image_file.content_type)

        presigned_url = r2_generate_presigned_url(filename, method="GET", expiration=604800)

        from todos.models import Profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.background_image = presigned_url
        profile.save()

        return JsonResponse({
            'message': 'Background image uploaded successfully',
            'background_image': presigned_url,
            'storage': 'r2',
        })
    except Exception as e:
        return JsonResponse({'error': f'Failed to upload background image: {str(e)}'}, status=500)
