from rest_framework import parsers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import ProfileSerializer


class ProfileViewApi(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, )

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return CustomUser.objects.filter(user=self.request.user)


