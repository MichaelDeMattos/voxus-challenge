# -*- coding: utf-8 -*-

import os
import redis.asyncio as redis

redis_pool = redis.ConnectionPool.from_url(os.getenv("REDIS_URI"))
redis_client = redis.Redis(connection_pool=redis_pool, max_connections=1000)
