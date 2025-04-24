from django.core.cache import cache


class CacheMixin:
    def set_get_cache(self, query, cache_name: str, cache_time: int):
        """
        Установить/ взять кеш.

        Args:
            query: Запрос в базу данных.
            cache_name: Название кэша.
            cache_time: Время кэширования в секундах.
        """
        data = cache.get(cache_name)
        if not data:
            data = query
            cache.set(cache_name, data, cache_time)
        return data
