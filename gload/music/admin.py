from django.contrib import admin
from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name','created_at')
    list_display_links = ('user',)
    list_filter = ('user',)


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title','created_at')
    list_display_links = ('user',)
    list_filter = ('genres','created_at',)
    search_fields = ('user','title','genres',)


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','title')
    list_display_links = ('user',)
    list_filter = ('user','tracks__title',)
