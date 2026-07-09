import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.auth_utils import jwt_required, jwt_optional
from .models import Community, CommunityMembership


def get_membership(community, user):
    return CommunityMembership.objects.filter(community=community, user=user).first()


def is_admin(community, user):
    membership = get_membership(community, user)
    return membership and membership.role == 'admin'


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


# ─── JOIN community ───

@csrf_exempt
@jwt_required
def join_community(request, community_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    if CommunityMembership.objects.filter(community=community, user=request.user).exists():
        return JsonResponse({'error': 'Already a member'}, status=409)

    CommunityMembership.objects.create(user=request.user, community=community, role='member')

    return JsonResponse(serialize_community(community, request))


# ─── LEAVE community ───

@csrf_exempt
@jwt_required
def leave_community(request, community_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    deleted, _ = CommunityMembership.objects.filter(community=community, user=request.user).delete()
    if not deleted:
        return JsonResponse({'error': 'Not a member'}, status=400)

    return JsonResponse({'left': True, 'community_id': community.id})


# ─── DELETE community (admin only) ───

@csrf_exempt
@jwt_required
def delete_community(request, community_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    membership = get_membership(community, request.user)
    if not membership or membership.role != 'admin':
        return JsonResponse({'error': 'Only the admin can delete this community'}, status=403)

    community.delete()

    return JsonResponse({'deleted': True, 'community_id': community_id})


# ─── UPDATE community (admin only) ───

@csrf_exempt
@jwt_required
def update_community(request, community_id):
    if request.method not in ('PUT', 'PATCH'):
        return JsonResponse({'error': 'Only PUT or PATCH allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    if not is_admin(community, request.user):
        return JsonResponse({'error': 'Only the admin can update this community'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    name = (data.get('name') or '').strip()
    if name and name != community.name:
        if Community.objects.filter(name=name).exists():
            return JsonResponse({'error': 'Community with this name already exists'}, status=409)
        community.name = name

    if 'description' in data:
        community.description = (data.get('description') or '').strip()
    if 'icon' in data:
        community.icon = data.get('icon')
    if 'banner' in data:
        community.banner = data.get('banner')

    community.save()
    return JsonResponse(serialize_community(community, request))


# ─── DETAIL community (lookup by id or @name) ───

@csrf_exempt
@jwt_optional
def detail_community(request, community_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except (Community.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Community not found'}, status=404)

    return JsonResponse(serialize_community(community, request))


@csrf_exempt
@jwt_optional
def detail_community_by_name(request, community_name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        community = Community.objects.get(name=community_name)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    return JsonResponse(serialize_community(community, request))
