import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from users.auth_utils import jwt_required, jwt_optional
from posts.models import Post
from posts.serializers_no_drf import serialize_post, handle_media_linking
from .models import Community, CommunityMembership, CommunityPost


def serialize_community_post(cp, request=None):
    data = serialize_post(cp.post, request)
    data['community_id'] = cp.community_id
    data['community_name'] = cp.community.name
    data['status'] = cp.status
    data['requested_by'] = {
        'id': cp.requested_by.id,
        'username': cp.requested_by.username,
        'avatar': cp.requested_by.avatar,
    } if cp.requested_by else None
    data['reviewed_by'] = {
        'id': cp.reviewed_by.id,
        'username': cp.reviewed_by.username,
    } if cp.reviewed_by else None
    data['reviewed_at'] = cp.reviewed_at.isoformat() if cp.reviewed_at else None
    return data


def get_membership(community, user):
    return CommunityMembership.objects.filter(community=community, user=user).first()


def is_admin_or_mod(community, user):
    membership = get_membership(community, user)
    return membership and membership.role in ('admin', 'moderator')


def is_member(community, user):
    return CommunityMembership.objects.filter(community=community, user=user).exists()


# ─── REQUEST a post (member submits) ───

@csrf_exempt
@jwt_required
def request_community_post(request, community_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    if not is_member(community, request.user):
        return JsonResponse({'error': 'You are not a member of this community'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip()
    if not title and not description:
        has_media = bool(data.get('photo_ids') or data.get('video_ids') or data.get('track_ids') or data.get('playlist_ids'))
        if not has_media:
            return JsonResponse({'error': 'title, description, or media is required'}, status=400)

    post = Post.objects.create(
        author=request.user,
        title=title,
        description=description,
    )

    handle_media_linking(post, data)

    cp = CommunityPost.objects.create(
        post=post,
        community=community,
        requested_by=request.user,
        status='approved' if is_admin_or_mod(community, request.user) else 'pending',
        reviewed_by=request.user if is_admin_or_mod(community, request.user) else None,
        reviewed_at=timezone.now() if is_admin_or_mod(community, request.user) else None,
    )

    return JsonResponse(serialize_community_post(cp, request), status=201)


# ─── LIST approved posts (public) ───

@csrf_exempt
@jwt_optional
def list_approved_community_posts(request, community_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    posts = CommunityPost.objects.filter(
        community=community, status='approved'
    ).select_related('post', 'requested_by', 'reviewed_by')

    return JsonResponse({
        'posts': [serialize_community_post(cp, request) for cp in posts],
    })


# ─── LIST pending requests (admin/mod only) ───

@csrf_exempt
@jwt_required
def list_pending_community_posts(request, community_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    if not is_admin_or_mod(community, request.user):
        return JsonResponse({'error': 'Only admins or moderators can view pending requests'}, status=403)

    posts = CommunityPost.objects.filter(
        community=community, status='pending'
    ).select_related('post', 'requested_by')

    return JsonResponse({
        'posts': [serialize_community_post(cp, request) for cp in posts],
    })


# ─── APPROVE a post request (admin/mod) ───

@csrf_exempt
@jwt_required
def approve_community_post(request, community_id, cp_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    if not is_admin_or_mod(community, request.user):
        return JsonResponse({'error': 'Only admins or moderators can approve posts'}, status=403)

    try:
        cp = CommunityPost.objects.get(id=cp_id, community=community)
    except CommunityPost.DoesNotExist:
        return JsonResponse({'error': 'Community post not found'}, status=404)

    if cp.status != 'pending':
        return JsonResponse({'error': f'Post is already {cp.status}'}, status=400)

    cp.status = 'approved'
    cp.reviewed_by = request.user
    cp.reviewed_at = timezone.now()
    cp.save()

    return JsonResponse(serialize_community_post(cp, request))


# ─── REJECT a post request (admin/mod) ───

@csrf_exempt
@jwt_required
def reject_community_post(request, community_id, cp_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    if not is_admin_or_mod(community, request.user):
        return JsonResponse({'error': 'Only admins or moderators can reject posts'}, status=403)

    try:
        cp = CommunityPost.objects.get(id=cp_id, community=community)
    except CommunityPost.DoesNotExist:
        return JsonResponse({'error': 'Community post not found'}, status=404)

    if cp.status != 'pending':
        return JsonResponse({'error': f'Post is already {cp.status}'}, status=400)

    cp.status = 'rejected'
    cp.reviewed_by = request.user
    cp.reviewed_at = timezone.now()
    cp.save()

    return JsonResponse(serialize_community_post(cp, request))


# ─── DELETE a community post (requester if pending, or admin/mod) ───

@csrf_exempt
@jwt_required
def delete_community_post(request, community_id, cp_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE allowed'}, status=405)

    try:
        community = Community.objects.get(id=community_id)
    except Community.DoesNotExist:
        return JsonResponse({'error': 'Community not found'}, status=404)

    try:
        cp = CommunityPost.objects.get(id=cp_id, community=community)
    except CommunityPost.DoesNotExist:
        return JsonResponse({'error': 'Community post not found'}, status=404)

    is_admin_mod = is_admin_or_mod(community, request.user)
    is_requester = cp.requested_by == request.user

    if not (is_admin_mod or (is_requester and cp.status == 'pending')):
        return JsonResponse({'error': 'Not allowed to delete this post'}, status=403)

    post = cp.post
    cp.delete()

    return JsonResponse({'deleted': True, 'post_id': post.id})
