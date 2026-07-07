from django.conf import settings
# from django.conf.urls import include, re_path
from django.urls import include, re_path
from django.conf.urls.static import static
from django.urls import path

from videos.spot import views_spot
from videos.upload.s3 import s3_views, s3_views_qalybay
from videos.upload.gcs import gcs_video_views_no_drf as gcs_video_views, gcs_native_video_views_no_drf as gcs_native_video_views
from videos.upload.r2 import r2_video_views_no_drf as r2_video_views
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

    # GCS Upload Endpoints (Matches S3 Flow via Boto3/HMAC)
    path('gcs/create_presigned_url/', gcs_video_views.gcs_initiate_video_upload, name='gcs_initiate_video'),
    path('gcs/get_presigned_url/', gcs_video_views.gcs_get_video_part_url, name='gcs_get_video_part'),
    path('gcs/complete_upload/', gcs_video_views.gcs_complete_video_upload, name='gcs_complete_video'),

    # Native GCS Upload Endpoints (Using google-cloud-storage library)
    path('gcs/native/initiate/', gcs_native_video_views.gcs_native_initiate_video_upload, name='gcs_native_initiate_video'),
    path('gcs/native/complete/', gcs_native_video_views.gcs_native_complete_video_upload, name='gcs_native_complete_video'),

    # R2 Upload Endpoints
    path('r2/create_presigned_url/', r2_video_views.r2_initiate_video_upload, name='r2_initiate_video'),
    path('r2/get_presigned_url/', r2_video_views.r2_get_video_part_url, name='r2_get_video_part'),
    path('r2/complete_upload/', r2_video_views.r2_complete_video_upload, name='r2_complete_video'),

    path('create_video/', s3_views_qalybay.create_video  ),



    # ===== VideoWatchHistory =====#
    path('api/save_playback/', views.save_playback_time),
    path('api/get_playback_time/', views.get_playback_time),


    path('<int:video_id>/', views.video_detail_api, name='video-detail'),

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
