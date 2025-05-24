from django.conf import settings
# from django.conf.urls import include, re_path
from django.urls import include, re_path
from django.conf.urls.static import static
from django.urls import path

from videos.spot import views_spot
from videos.upload import ( s3_views, s3_views_qalybay )
from videos import views
# from . import management_views, views
# from . import views
# from .feeds import IndexRSSFeed, SearchRSSFeed
#
urlpatterns = [

    path('launch-spot/', views_spot.launch_spot, name='launch_spot'),

    path('create_presigned_url/', s3_views_qalybay.create_presigned_url  ),
    path('get_presigned_url/', s3_views_qalybay.get_presigned_url  ),
    path('complete_upload/', s3_views_qalybay.complete_upload  ),

    # ===== VideoWatchHistory =====#
    path('api/save_playback/', views.save_playback_time),
    path('api/get_playback_time/', views.get_playback_time),


    # API VIEWS
    # path('api/v1/search', views.MediaSearch.as_view()),
    # path('api/v1/video', views.MediaList.as_view()),
    # path('api/v1/video/', views.MediaList.as_view()),
    #
    # path('api/v1/video/<str:friendly_token>',views.MediaDetail.as_view(),name='api_get_media',),
    # path('api/v1/video/encoding/<str:encoding_id>',views.EncodingDetail.as_view(),name='api_get_encoding',),
    #
    # path('api/v1/video/<str:friendly_token>/actions',views.MediaActions.as_view(),),
    # path('api/v1/categories', views.CategoryList.as_view()),
    # path('api/v1/tags', views.TagList.as_view()),
    #
    # path('api/v1/comments', views.CommentList.as_view()),
    # path('api/v1/video/<str:friendly_token>/comments',views.CommentDetail.as_view(),),
    # path('api/v1/video/<str:friendly_token>/comments/<uuid:uid>',views.CommentDetail.as_view(),),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
