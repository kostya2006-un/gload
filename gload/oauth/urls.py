from django.urls import include, path, re_path

urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'', include('djoser.urls.authtoken')),
]