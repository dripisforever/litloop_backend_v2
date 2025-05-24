#ref https://github.com/HackSoftware/Django-React-GoogleOauth2-Example/blob/main/server/auth/apis.py
import json
from urllib.parse import urlencode

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.core.serializers import serialize


# from api.mixins import ApiErrorsMixin, PublicApiMixin, ApiAuthMixin

from users.services import user_record_login, user_change_secret_key, user_get_or_create

from .services import (
    jwt_login,
    google_get_access_token,
    twitch_get_access_token,
    google_get_user_info,
    twitch_get_user_info
)


def redirect_to_google_oauth_url(self):
    url = "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount"
    response_type = "code"
    client_id = ""
    redirect_uri = "http://localhost:8000/auth/google/callback"
    prompt = "select_account"
    access_type = "offline"
    scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    oauth_redirect_url = f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&prompt={prompt}&access_type={access_type}&scope={scope}'
    return redirect(oauth_redirect_url)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    redirect_uri = "http://localhost:3001/auth/spotify/callback"
    access_token = spotify_get_access_token(code=code, redirect_uri=redirect_uri)

    user_data = google_get_user_info(access_token=access_token)

    profile_data = {
        'email': user_data['email'],
        'avatar': user_data['picture'],
        'username': user_data['given_name']

    }
    user, _ = user_get_or_create(**profile_data)

    return user


class GoogleLoginApiOld(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def put(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        # login_url = f'{settings.BASE_FRONTEND_URL}/login'
        #
        # if error or not code:
        #     params = urlencode({'error': error})
        #     return redirect(f'{login_url}?{params}')

        redirect_uri = "http://localhost:8000/auth/google/callback"
        # redirect_uri = "http://localhost:3000/auth/google/callback"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'email': user_data['email'],
            'avatar': user_data['picture'],
            'username': user_data['given_name']
        }

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**profile_data)

        # REDIRECT TO REACT APP
        # client_callback_url = "http://localhost:3001/auth/callback"
        client_callback_url = "http://localhost:3001/auth/callback?token="+access_token

        # response = redirect(client_callback_url)
        response = client_callback_url
        response = jwt_login(response=response, user=user)
        last = redirect(response)
        return last
        # return response


        # BRAINSTORM
        # response = redirect('http://localhost:3001/auth/callback')
        # response['Set-Cookie'] = 'Test'
        # del response['Test']
        # response['Authorization'] = 'Bearer '+ jwt
        #
        # return response


class GoogleLoginApi(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def put(self, request, *args, **kwargs):
        code = request.data.get('code', False)

        redirect_uri = "http://localhost:3001/auth/google/callback"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        # user_data = twitch_get_user_info(access_token=access_token)
        #
        # profile_data = {
        #     'email': user_data['email'],
        #     'avatar': user_data['picture'],
        #     'username': user_data['given_name']
        # }
        #
        # # We use get-or-create logic here for the sake of the example.
        # # We don't have a sign-up flow.
        # user, _ = user_get_or_create(**profile_data)

        return Response(access_token)


class TwitchLoginApi(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def put(self, request, *args, **kwargs):
        code = request.data.get('code', False)

        redirect_uri = "http://localhost:3001/auth/twitch/callback"
        access_token = twitch_get_access_token(code=code, redirect_uri=redirect_uri)

        # user_data = twitch_get_user_info(access_token=access_token)
        #
        # profile_data = {
        #     'email': user_data['email'],
        #     'avatar': user_data['picture'],
        #     'username': user_data['given_name']
        # }
        #
        # # We use get-or-create logic here for the sake of the example.
        # # We don't have a sign-up flow.
        # user, _ = user_get_or_create(**profile_data)

        return Response(access_token)
