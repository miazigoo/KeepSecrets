def cache_control(func):
    """ Декоратор для добавления no-cache-headers """
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return wrapper