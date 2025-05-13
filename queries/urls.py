# from __future__ import absolute_import
from django.urls import path
from queries.views import (
    # SearchQueryAPIView,
    BingQueryView,
    BraveQueryView,
    BraveImagesSearchView,
    GoogleFirefoxQueryView,
    GoogleQueryView,
)



urlpatterns = [

    path('bing/search', BingQueryView.as_view(), name="search"),

    path('brave/search', BraveQueryView.as_view(), name="search"),
    path('brave/images/search', BraveImagesSearchView.as_view(), name="search"),

    path('google/firefox/search', GoogleFirefoxQueryView.as_view(), name="search"),
    path('google/search', GoogleQueryView.as_view(), name="search"),


]
