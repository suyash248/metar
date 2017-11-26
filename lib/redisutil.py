"""
For initializing redis connection pool. Any utility functions related to redis operations will reside here.
"""
import redis
from settings import REDIS

redis_conn_pool = redis.ConnectionPool(host=REDIS.get('HOST', 'localhost'),
                                       port=REDIS.get('PORT', 6379),
                                       db=REDIS.get('DB', 0),
                                       password=REDIS.get('PASSWORD', None))
redis_connection = redis.Redis(connection_pool=redis_conn_pool)