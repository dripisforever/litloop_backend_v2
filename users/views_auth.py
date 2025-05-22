import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from users.models import User
from users.jwt_auth import generate_jwt

def protected_view(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'error': 'Unauthenticated'}, status=401)

    payload = decode_jwt(token)
    if not payload:
        return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    return JsonResponse({'message': f"Hello, {payload['username']}!"})

    
@csrf_exempt
def signup_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data     = json.loads(request.body)
    username = data.get('username')
    email    = data.get('email')
    password = data.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    token = generate_jwt(user)
    return JsonResponse({'token': token})

@csrf_exempt
def signin_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    user = authenticate(email=email, password=password)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    token = generate_jwt(user)
    return JsonResponse({'token': token})
