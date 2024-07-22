from django.core.cache import cache
from django.conf import settings

from blog.models import Post


def get_queryset():
    if settings.CACHE_ENABLED:
        key = 'post_list'
        queryset = cache.get(key)
        if not queryset:
            queryset = list(Post.objects.filter(is_published=True))
            cache.set(key, queryset, 60 * 60)
        else:
            print("Using cached queryset")
    else:
        queryset = list(Post.objects.filter(is_published=True))
    print(f"Queryset: {queryset}")
    return queryset
