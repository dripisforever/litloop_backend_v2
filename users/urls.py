from django.urls import path

from users.views_header import (
    signup_view,
    signin_view
)


urlpatterns = [

    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),

]
