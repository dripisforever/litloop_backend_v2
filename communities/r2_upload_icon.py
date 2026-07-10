import os
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chats.r2_utils import r2_upload_file, r2_generate_presigned_url
from users.auth_utils import jwt_required
from communities.models import Community, CommunityMembership


@csrf_exempt
@jwt_required
def r2_upload_community_icon(request, community_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    membership = CommunityMembership.objects.filter(community=community, user=request.user).first()
    if not membership or membership.role != 'admin':
        return JsonResponse({'error': 'Only admin can upload community icon'}, status=403)

    if 'icon' not in request.FILES:
        return JsonResponse({'error': 'No file provided in "icon" field.'}, status=400)

    icon_file = request.FILES['icon']

    if not icon_file.content_type.startswith('image/'):
        return JsonResponse({'error': 'File must be an image.'}, status=400)

    ext = os.path.splitext(icon_file.name)[1]
    if not ext:
        ext = '.jpg' if icon_file.content_type == 'image/jpeg' else '.png'

    filename = f"community_icons/{community.id}_{uuid.uuid4()}{ext}"

    try:
        r2_upload_file(icon_file, filename, content_type=icon_file.content_type)

        presigned = r2_generate_presigned_url(filename, method='GET', expiration=604800)

        community.icon = presigned
        community.save(update_fields=['icon'])

        return JsonResponse({
            'message': 'Community icon uploaded successfully',
            'icon': presigned,
            'storage': 'r2',
        })
    except Exception as e:
        return JsonResponse({'error': f'Failed to upload icon: {str(e)}'}, status=500)
