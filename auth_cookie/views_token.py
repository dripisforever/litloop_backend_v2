from django.http import JsonResponse
import jwt, datetime

def token_login(request):
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
            return JsonResponse({'access': token})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
