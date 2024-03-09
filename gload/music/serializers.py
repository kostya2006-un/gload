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
        cover = instance.cover  # Получаем файл обложки
        if cover:
            try:
                delete_old_cover(cover.path)  # Удаляем старое изображение обложки
            except ValueError:
                pass  # Если нет файла, ничего не делаем
        return super().update(instance, validated_data)