from django.urls import path
from .views import WorkListCreateView, ArtistListCreateView, RegisterView, ObtainAuthTokenView,OpenTokenInfoView,OpenObtainAuthTokenView
from .views import obtain_token

from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('api/works/', WorkListCreateView.as_view(), name='work-list-create'),
    path('api/artists/', ArtistListCreateView.as_view(), name='artist-list-create'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', ObtainAuthTokenView.as_view(), name='login'),
    path('api/token/', obtain_token, name='obtain_token'),
    path('api/token-info/', OpenTokenInfoView.as_view(), name='open-token-info'),
]
