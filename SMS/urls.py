from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def custom_admin_login(request):
    return redirect('/accounts/login/?next=' + request.GET.get('next', '/manage/')) # noqa


urlpatterns = [
    path(
        'manage/',
        admin.site.urls
    ),

    # api url includes...................
    path(
        '',
        include('core.api.urls')
    ),
]

# Add this at the end of the file to serve static files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )