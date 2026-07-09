from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_community, name='community-create'),
    path('', views.list_communities, name='community-list'),
]
