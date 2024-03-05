from django.urls import path
from .views import GenresApiViews

urlpatterns = [
    path('genres/',GenresApiViews.as_view(),name = 'genres_api'),
]
