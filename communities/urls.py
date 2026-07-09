from django.urls import path
from . import views, post_views

urlpatterns = [
    path('create/', views.create_community, name='community-create'),
    path('', views.list_communities, name='community-list'),

    # Community posts
    path('<int:community_id>/posts/request/', post_views.request_community_post, name='community-post-request'),
    path('<int:community_id>/posts/', post_views.list_approved_community_posts, name='community-posts'),
    path('<int:community_id>/posts/pending/', post_views.list_pending_community_posts, name='community-posts-pending'),
    path('<int:community_id>/posts/<int:cp_id>/approve/', post_views.approve_community_post, name='community-post-approve'),
    path('<int:community_id>/posts/<int:cp_id>/reject/', post_views.reject_community_post, name='community-post-reject'),
    path('<int:community_id>/posts/<int:cp_id>/', post_views.delete_community_post, name='community-post-delete'),

    # Membership
    path('<int:community_id>/join/', views.join_community, name='community-join'),
    path('<int:community_id>/leave/', views.leave_community, name='community-leave'),
    path('<int:community_id>/delete/', views.delete_community, name='community-delete'),
]
