import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.models import User
from users.jwt_auth import decode_jwt


def _get_current_user(request):
    if request.user.is_authenticated:
        return request.user
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        payload = decode_jwt(auth.split(' ')[1].strip())
        if payload:
            try:
                return User.objects.get(id=payload.get('user_id'))
            except User.DoesNotExist:
                return None
    return None


@csrf_exempt
@require_http_methods(['PUT'])
def update_user_role_view(request, user_id):
    current_user = _get_current_user(request)
    if not current_user or not current_user.is_superuser:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if 'is_staff' in body:
        target.is_staff = bool(body['is_staff'])
    if 'is_superuser' in body:
        target.is_superuser = bool(body['is_superuser'])
    target.save(update_fields=['is_staff', 'is_superuser'])

    return JsonResponse({
        'id': target.id,
        'username': target.username,
        'is_staff': target.is_staff,
        'is_superuser': target.is_superuser,
    })
