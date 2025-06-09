from django.urls import path

from users.views_header import (
    signup_view,
    signin_view
)
from users.views_oauth import (
    google_token_exchange_view,
    
)


urlpatterns = [

    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),

    path('callback/', signin_view, name='signin'),
    path('token/', google_token_exchange_view, name='signin'),


]
