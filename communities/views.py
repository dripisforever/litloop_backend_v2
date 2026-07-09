import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.auth_utils import jwt_required
from .models import Community, CommunityMembership


def serialize_community(community, request=None):
    user_is_member = False
    user_role = None
    if request and request.user.is_authenticated:
        membership = CommunityMembership.objects.filter(
            user=request.user, community=community
        ).first()
        if membership:
            user_is_member = True
            user_role = membership.role

    return {
        'id': community.id,
        'name': community.name,
        'description': community.description,
        'icon': community.icon,
        'banner': community.banner,
        'created_by': community.created_by_id,
        'created_by_username': community.created_by.username,
        'member_count': CommunityMembership.objects.filter(community=community).count(),
        'user_is_member': user_is_member,
        'user_role': user_role,
        'created_at': community.created_at.isoformat() if community.created_at else None,
    }


@csrf_exempt
@jwt_required
def create_community(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    name = (data.get('name') or '').strip()
    if not name:
        return JsonResponse({'error': 'name is required'}, status=400)

    if Community.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Community with this name already exists'}, status=409)

    community = Community.objects.create(
        name=name,
        description=(data.get('description') or '').strip(),
        icon=data.get('icon'),
        banner=data.get('banner'),
        created_by=request.user,
    )

    CommunityMembership.objects.create(
        user=request.user,
        community=community,
        role='admin',
    )

    return JsonResponse(serialize_community(community, request), status=201)


@csrf_exempt
def list_communities(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    communities = Community.objects.all().order_by('-created_at')
    return JsonResponse({
        'communities': [serialize_community(c, request) for c in communities],
    })
