from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer
from .services import delete_old_cover
from .models import Genre,Album,Track,Playlist


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

    def validate_album(self, album):
        user = self.context['request'].user
        if album and album.user != user:
            raise ValidationError("You can only add tracks to albums created by you.")
        return album

    def create(self, validated_data):
        validated_data['album'] = self.validate_album(validated_data['album'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['album'] = self.validate_album(validated_data['album'])

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


class PlayListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Playlist
        fields = "__all__"
