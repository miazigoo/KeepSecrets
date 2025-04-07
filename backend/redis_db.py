import redis
from environs import Env
from redis.backoff import ConstantBackoff
from redis.exceptions import NoPermissionError
from redis.retry import Retry

env = Env()
env.read_env()

redis_pool = redis.ConnectionPool(
        host=env.str('REDIS_HOST', '127.0.0.1'),
        port=env.int('REDIS_PORT', 6379),
        retry=Retry(ConstantBackoff(10), 30),
        retry_on_error=[
            ConnectionError, TimeoutError, NoPermissionError, ConnectionRefusedError, PermissionError
        ],
        socket_timeout=300,
        socket_connect_timeout=300,
        health_check_interval=300,
    )

def get_redis_connection():
    return redis.StrictRedis(connection_pool=redis_pool, db=0)

