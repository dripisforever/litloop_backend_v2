# from __future__ import absolute_import
from django.urls import path
from posts.views import (create_post_with_line_breaks,)


from posts.views_post import (create_post)
from posts.views_postman import (create_post_with_photos)
from posts.create_post_with_video import (create_post_with_video)


from posts.views_post_list import (list_of_posts,post_detail)

from posts.views_search import (SearchTrackView,SearchAlbumView,SearchArtistView,)
from posts.views_create_post_with_media import (create_post_api,)

urlpatterns = [

    # ──────── CREATE POSTS ────────
    path('create/create_post_with_line_breaks',      create_post_with_line_breaks, name="posts"),

    path('create/v4',      create_post, name="posts"),
    path('create/postman', create_post_with_photos, name="posts"),
    path('create/post_with_videos', create_post_with_video, name="posts"),
    path('create_post_api/', create_post_api, name="posts"),


    # ──────── VIEW POSTS ────────
    path('list/',          list_of_posts, name="posts"),
    path('<int:post_id>/', post_detail, name='post_detail'),


    # ──────── FEED ────────

    # ──────── SEARCH ────────
    path('search/artist', SearchArtistView.as_view(), name="search"),
    path('search/album', SearchAlbumView.as_view(), name="search"),
    path('search/track', SearchTrackView.as_view(), name="search"),

    # ──────── MISC ────────
]
