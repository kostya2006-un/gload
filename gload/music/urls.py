from django.urls import path
from .views import GenresApiViews,AlbumApiView

urlpatterns = [
    path('genres/',GenresApiViews.as_view(),name = 'genres_api'),

    path('albums/',AlbumApiView.as_view({'get':'list','post':'create'})),
    path('albums/<int:pk>/',AlbumApiView.as_view({'put': 'update','delete':'destroy'})),
]
