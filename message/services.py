from django.conf import settings
from django.core.cache import cache

from .models import Message


def get_messages_from_cache():
    """ Получает данные из кэша, если кэш пуст, получает данные из БД """
    if not settings.CACHE_ENABLED:
        return Message.objects.all()
    key = 'object_list'
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages
