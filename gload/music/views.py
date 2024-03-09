from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import GenresSerializer,AlbumSerializer
from rest_framework import generics, viewsets, parsers
from .models import Genre,Album
from .permisions import IsAuthor
from .services import delete_old_cover


class GenresApiViews(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class AlbumApiView(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthor]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def perform_destroy(self, instance):
        delete_old_cover(instance.cover.path)
        instance.delete()
