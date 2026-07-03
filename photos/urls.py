from django.urls import path
from videos.upload.s3 import s3_views_qalybay
from photos.upload.r2 import r2_photo_views_no_drf as r2_photo_views
from photos.upload.gcs import gcs_photo_views_no_drf as gcs_photo_views
from photos.views import photo_album_detail_api, photo_album_create_api, photo_album_add_photo_api, photo_album_upload_api

urlpatterns = [
    path('create_presigned_url/', s3_views_qalybay.create_presigned_url),
    path('get_presigned_url/', s3_views_qalybay.get_presigned_url),
    path('complete_upload/', s3_views_qalybay.complete_upload),

    # GCS Upload Endpoints
    path('gcs/create_presigned_url/', gcs_photo_views.gcs_initiate_photo_upload, name='gcs_initiate_photo'),
    path('gcs/get_presigned_url/', gcs_photo_views.gcs_get_photo_part_url, name='gcs_get_photo_part'),
    path('gcs/complete_upload/', gcs_photo_views.gcs_complete_photo_upload, name='gcs_complete_photo'),

    # R2 Upload Endpoints
    path('r2/create_presigned_url/', r2_photo_views.r2_initiate_photo_upload, name='r2_initiate_photo'),
    path('r2/get_presigned_url/', r2_photo_views.r2_get_photo_part_url, name='r2_get_photo_part'),
    path('r2/complete_upload/', r2_photo_views.r2_complete_photo_upload, name='r2_complete_photo'),

    # Photo Album Create
    path('album/create/', photo_album_create_api, name='photo_album_create'),

    # Photo Album Detail
    path('album/<str:friendly_token>/', photo_album_detail_api, name='photo_album_detail'),

    # Photo Album Add Photo
    path('album/<int:photo_album_id>/add/', photo_album_add_photo_api, name='photo_album_add_photo'),

    # Photo Album Upload Photo
    path('album/<int:photo_album_id>/upload/', photo_album_upload_api, name='photo_album_upload'),
]
