from rest_framework import serializers
from rest_framework.serializers import BaseSerializer
from .services import delete_old_cover
from .models import Genre,Album


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "description", "user", "cover", "private")

    def update(self, instance, validated_data):
        cover = instance.cover
        if cover:
            try:
                delete_old_cover(cover.path)
            except ValueError:
                pass
        return super().update(instance, validated_data)