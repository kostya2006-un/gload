from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from .services import validate_size_img, get_url_album_cover, get_url_track_cover, get_path_track, delete_old_cover

User = get_user_model()


class Genre(models.Model):
    """Модель жанров трека"""
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_url_album_cover,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_img],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Album.objects.get(pk=self.pk)
            if self.cover != old_instance.cover:
                if old_instance.cover:  # Проверяем, есть ли старый файл обложки
                    delete_old_cover(old_instance.cover.path)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.user}'


class Track(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='tracks')
    genres = models.ManyToManyField(Genre)
    album = models.ForeignKey(Album,on_delete=models.CASCADE,blank=True,null=True)
    likes = models.PositiveIntegerField(default=0)
    download = models.PositiveIntegerField(default=0)
    listened = models.PositiveIntegerField(default=0)
    cover = models.ImageField(
        upload_to=get_url_track_cover,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_img],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    file = models.FileField(
        upload_to=get_path_track,
        validators = [FileExtensionValidator(allowed_extensions=['mp3','wav'])],
    )
    title = models.CharField(max_length=50)
    private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Track.objects.get(pk=self.pk)
            if self.cover != old_instance.cover:
                delete_old_cover(old_instance.cover.path)
            if self.file != old_instance.file:
                delete_old_cover(old_instance.file.path)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.title}'


class Playlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='playlist')
    tracks = models.ManyToManyField(Track, related_name='user_fav_tracks')
    title = models.CharField(max_length=50)

