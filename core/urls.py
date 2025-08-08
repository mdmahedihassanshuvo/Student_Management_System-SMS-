from django.urls import path

# LOCAL IMPORTS
from core.views import (
    RegisterView,
    LoginView,
    LogoutAPIView
)

app_name = 'core'

urlpatterns = [
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutAPIView.as_view(),
        name='logout'
    ),
]