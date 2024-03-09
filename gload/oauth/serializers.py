from rest_framework import serializers
from .models import CustomUser
from .services import delete_old_cover


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','bio', 'avatar','username','avatar']

    def update(self, instance, validated_data):
        delete_old_cover(instance.avatar.path)
        return super().update(instance,validated_data)
