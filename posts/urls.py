# from __future__ import absolute_import
from django.urls import path
from .views import (
    PostDetailAPIView,
    PostListAPIView,
    # PostLikeAPIView,
    # PostSearchAPIView,
    TrackDetailAPIView,
    SearchTrackAPIView,
    SearchAlbumAPIView,
    SearchArtistAPIView,
    ArtistDetailAPIView,
    AlbumDetailAPIView,
    ArtistAlbumsDetailAPIView,
    ArtistRelatedArtistsDetailAPIView,
    FeedAPIView,
    PostCreateAPIView,
    NewReleasesAPIView,

    ViewsUP,
    create_post_with_line_breaks,


)
from .view import (
    PostLikeView,
    PostLikersView,
)
from .views_post import (
     create_post
)
from .views_post_list import (
     list_of_posts
)

from posts.views_postman import (
     create_post_with_photos
)
from posts.views_base import (
    PostCreateViewV2,
)


urlpatterns = [

    # ──────── POSTS ────────
    path('', PostListAPIView.as_view(), name="posts"),
    path('create/', PostCreateAPIView.as_view(), name="posts"),
    path('create/v2', create_post_with_line_breaks, name="posts"),
    path('create/v3', PostCreateViewV2.as_view(), name="posts"),
    path('create/v4', create_post, name="posts"),
    path('create/postman', create_post_with_photos, name="posts"),
    path('list/', list_of_posts, name="posts"),

    path('<int:id>/', PostDetailAPIView.as_view(), name="post"),
    path('<int:id>/like/', PostLikeView.as_view(), name="post-like"),
    path('<int:id>/likers/', PostLikersView.as_view(), name="post-likers"),
    path('<int:id>/impressions/', PostDetailAPIView.as_view(), name="post"),

    # ──────── FEED ────────
    path('feed/', FeedAPIView.as_view(), name="feed"),
    path('feed/upd/', NewReleasesAPIView.as_view(), name="feed"),

    # ──────── SEARCH ────────
    path('search/artist', SearchArtistAPIView.as_view(), name="search"),
    path('search/album', SearchAlbumAPIView.as_view(), name="search"),
    path('search/track', SearchTrackAPIView.as_view(), name="search"),

    # ──────── MISC ────────
    path('up', ViewsUP.as_view()),
]
