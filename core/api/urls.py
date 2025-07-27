from django.urls import path
from core.api.views import CustomUserCreateAPIView, LoginAPIView

urlpatterns = [
    path(
        'v1/user/register/',
        CustomUserCreateAPIView.as_view(),
        name='user_register'
    ),
    path(
        'v1/user/login/',
        LoginAPIView.as_view(),
        name='user_login'
    ),
]
