import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
            request.user = user  # attach user to request for the view
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return JsonResponse({"error": "Invalid token or user not found"}, status=401)

        return view_func(request, *args, **kwargs)
    return wrapper
