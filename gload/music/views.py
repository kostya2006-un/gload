from .serializers import GenresSerializer
from rest_framework import generics
from .models import Genre
# Create your views here.


class GenresApiViews(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer