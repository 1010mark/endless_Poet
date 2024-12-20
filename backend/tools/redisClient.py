import redis
__cache = None

def get_redis_client():
    global __cache
    if __cache is None:
        __cache = redis.Redis(host='redis', port=6379)
    try:
        __cache.ping()  # 接続確認
    except redis.ConnectionError:
        __cache = redis.Redis(host='redis', port=6379)  # 再接続
    return __cache
