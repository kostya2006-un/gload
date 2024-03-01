from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import ProfileSerializer


class ProfileViewApi(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

