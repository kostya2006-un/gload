from django.urls import path
from .views import GenresApiViews,AlbumApiView,AlbumUserApi,AlbumAuthorApi

urlpatterns = [
    path('genres/',GenresApiViews.as_view(),name = 'genres_api'),

    path('albums/',AlbumApiView.as_view({'get':'list','post':'create'}), name = 'albums'),
    path('albums/<int:pk>/',AlbumApiView.as_view({'delete':'destroy','put':'partial_update'})),

    path('albums_users',AlbumUserApi.as_view(),name = 'albums_user'),
    path('albums_author/<int:pk>/',AlbumAuthorApi.as_view(),name = 'albums_author'),
]
