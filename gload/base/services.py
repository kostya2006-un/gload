from django.core.exceptions import ValidationError


def get_path_avatar(instance,file):
    return f'avatars/{instance.id}/{file}'


def validate_size_img(obj):
    megabite_limit = 2
    if obj.size > megabite_limit*1024*1024:
        raise ValidationError(f"Максимальный размер файла {megabite_limit}")
