from rest_framework import serializers
from rest_framework.serializers import BaseSerializer
from .services import delete_old_cover
from .models import Genre,Album,Track


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

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


class TrackSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    download = serializers.IntegerField(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Track
        fields = "__all__"

    def update(self, instance, validated_data):
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

        return super().update(instance, validated_data)
