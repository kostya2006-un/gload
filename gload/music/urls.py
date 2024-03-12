from django.urls import path
from .views import GenresApiViews,AlbumApiView,AlbumUserApi,AlbumAuthorApi
from .views import TrackApiView, TrackUserApi, TrackAuthorApi, StreamingFileView, DownloadTrackView
from .views import PlayListApiView

urlpatterns = [
    path('genres/',GenresApiViews.as_view(),name = 'genres_api'),

    path('albums/',AlbumApiView.as_view({'get':'list','post':'create'}), name = 'albums'),
    path('albums/<int:pk>/',AlbumApiView.as_view({'delete':'destroy','put':'partial_update'})),

    path('albums_users',AlbumUserApi.as_view(),name = 'albums_user'),
    path('albums_author/<int:pk>/',AlbumAuthorApi.as_view(),name = 'albums_author'),

    path('tracks/', TrackApiView.as_view({'get':'list','post':'create'})),
    path('tracks/<int:pk>/', TrackApiView.as_view({'put':'update','delete':'destroy'})),

    path('tracks_users/',TrackUserApi.as_view(), name = 'tracks_users'),
    path('tracks_author/<int:pk>/',TrackAuthorApi.as_view(), name = 'tracks_author'),

    path('stream_track/<int:pk>/',StreamingFileView.as_view()),
    path('download_track/<int:pk>/',DownloadTrackView.as_view()),

    path('playlists/', PlayListApiView.as_view({'get': 'list', 'post': 'create'})),
    path('playlists/<int:pk>/', PlayListApiView.as_view({'put': 'update', 'delete': 'destroy'})),

]
