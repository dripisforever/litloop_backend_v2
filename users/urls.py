from django.urls import path
from .views import (
    UserView,
    RegisterView,
    VerifyEmail,
    LoginAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserDetailByIdAPIView,
    # UserAvatarListAPIView,
    CurrentUserView,
    CurrentUserViewAPI,
    UserLikedPostsList,
    UserPostsList,
    # UserLikeListAPIView
)

from users.views_auth import (signin_view)

# from posts.views import


from django.urls import path
from .views import *


urlpatterns = [

    # ──────── AUTH & REGISTRATION ────────
    path('signup/', RegisterView.as_view(), name="register"),
    path('signin/', signin_view, name="login"),
    path('email_verify/', VerifyEmail.as_view(), name="email-verify"),

    # ──────── USER DATA ────────
    path('<int:id>/', UserDetailByIdAPIView.as_view(), name="user_detail_by_id"),
    path('<str:username>/', UserDetailAPIView.as_view(), name="user_detail"),
    path('list/', UserListAPIView.as_view(), name="users"),
    path('me/', CurrentUserView.as_view(), name="current_user"),
    path('current_user/', CurrentUserViewAPI.as_view(), name="current_user_v2"),


    # ──────── AVATAR & PROFILE ────────
    path('<int:id>/avatar/', UserView.as_view(), name="user_avatar"),

    # ──────── TWITCH SYNC ────────
    path('twitch/<int:id>/update/', UserView.as_view(), name="twitch_user"),
    path('twitch/update/', UpdateCurrentUserView.as_view(), name="twitch_user"),

    # ──────── USER CONTENT ────────
    path('<int:id>/likes/', UserLikedPostsList.as_view(), name="user_likes"),
    path('<int:id>/posts/', UserPostsList.as_view(), name="user_posts"),
]



# https://dev.litloop.co/oauth/applications/new
# https://dev.litloop.co/oauth/applications/318262
