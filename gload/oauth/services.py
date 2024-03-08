import os
from rest_framework.exceptions import ValidationError


def get_url_pat(instance,file):
    return f'avatars/{instance.id}/{file}'


def validate_size_img(obj):
    megabite_limit = 2
    if obj.size > megabite_limit*1024*1024:
        raise ValidationError(f"Максимальный размер файла {megabite_limit}")


def delete_old_cover(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
