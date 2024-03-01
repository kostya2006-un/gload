from django.urls import include, path, re_path
from .views import ProfileViewApi

urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'', include('djoser.urls.authtoken')),
    path('profile/',ProfileViewApi.as_view(),name = 'profile_api')
]
