from rest_framework.exceptions import ValidationError
import os

def get_url_album_cover(instance,file):
    return f'album/user_{instance.user.id}/{file}'


def get_url_track_cover(instance,file):
    return f'track/user_{instance.user.id}/{file}'


def get_path_track(instance,file):
    return f'track_path/user_{instance.user.id}/{file}'


def validate_size_img(obj):
    megabite_limit = 2
    if obj.size > megabite_limit*1024*1024:
        raise ValidationError(f"Максимальный размер файла {megabite_limit}")

def delete_old_cover(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)