from django.http import FileResponse, Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
import os
from .serializers import GenresSerializer,AlbumSerializer, TrackSerializer
from .serializers import PlayListSerializer
from rest_framework import generics, viewsets, parsers, views
from .models import Genre, Album, Track, Playlist
from .permisions import IsAuthor
from .services import delete_old_cover
from .classes import Pagination
from django_filters.rest_framework import DjangoFilterBackend


class GenresApiViews(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class AlbumApiView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser, )
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Album.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def perform_destroy(self, instance):
        cover = instance.cover
        if cover:
            try:
                delete_old_cover(cover.path)
            except ValueError:
                pass
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class AlbumUserApi(generics.ListAPIView):

    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name',]

    def get_queryset(self):
        return Album.objects.filter(private = False)


class AlbumAuthorApi(generics.ListAPIView):
    serializer_class = AlbumSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', ]

    def get_queryset(self):
        return Album.objects.filter(user__id = self.kwargs.get('pk'), private = False)


class TrackApiView(viewsets.ModelViewSet):

    parser_classes = (parsers.MultiPartParser,)
    serializer_class = TrackSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        cover = instance.cover
        file = instance.file
        if cover:
            try:
                delete_old_cover(cover.path)
            except ValueError:
                pass
        if file:
            try:
                delete_old_cover(file.path)
            except ValueError:
                pass
        super().perform_destroy(instance)


class TrackUserApi(generics.ListAPIView):
    serializer_class = TrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'genres__name','album__name']

    def get_queryset(self):
        return Track.objects.filter(private = False)


class TrackAuthorApi(generics.ListAPIView):
    serializer_class = TrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'genres__name', 'album__name']

    def get_queryset(self):
        return Track.objects.filter(user__id = self.kwargs.get('pk'), private = False)


class StreamingFileView(views.APIView):

    def set_play(self,track):
        track.listened += 1
        track.save()

    def get(self,request,pk):
        track = get_object_or_404(Track, id = pk)
        if track.private and track.user == request.user:
            if os.path.exists(track.file.path):
                self.set_play(track)
                return FileResponse(open(track.file.path, "rb"), filename=track.file.name)
            else:
                return Http404
        if not track.private:
            if os.path.exists(track.file.path):
                self.set_play(track)
                return FileResponse(open(track.file.path, "rb"), filename=track.file.name)
            else:
                return Http404
        else:
            raise PermissionDenied("You don't have permission to listen this track.")



class DownloadTrackView(views.APIView):

    def set_download(self):
        self.track.download += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(Track, id=pk)

        if self.track.private and self.track.user == request.user:
            if os.path.exists(self.track.file.path):
                self.set_download()
                return FileResponse(open(self.track.file.path, "rb"), filename=self.track.file.name, as_attachment=True)
            else:
                raise Http404
        elif not self.track.private:
            if os.path.exists(self.track.file.path):
                self.set_download()
                return FileResponse(open(self.track.file.path, "rb"), filename=self.track.file.name, as_attachment=True)
            else:
                raise Http404
        else:
            raise PermissionDenied("You don't have permission to download this track.")


class PlayListApiView(viewsets.ModelViewSet):

    parser_classes = (parsers.MultiPartParser,)
    serializer_class = PlayListSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
