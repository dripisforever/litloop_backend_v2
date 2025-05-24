import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from users.jwt_auth import generate_jwt, decode_jwt
from users.models import User


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email    = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user = User.objects.create_user(email=email, username=username, password=password)
        return JsonResponse({'message': 'User created'})



@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('email_or_username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = generate_jwt(user)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)



import jwt, datetime

def cookie_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'iat': datetime.datetime.utcnow()
            }
            
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            res = JsonResponse({'message': 'Logged in'})
            res.set_cookie(
                key='jwt',
                value=token,
                httponly=True,
                samesite='Lax'
            )
            return res
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
