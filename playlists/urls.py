# from __future__ import absolute_import
from django.urls import path
from playlists.views import (
    playlist_detail,
    playlist_offset
)


urlpatterns = [
    # path('', AlbumListAPIView.as_view(), name="posts"),
    # path('feed/', FeedAPIView.as_view(), name="feed"),

    path('<str:playlist_uri>/', playlist_detail, name="album_detail"),
    path('<str:playlist_uri>/tracks', playlist_offset, name="album_detail"),


]
