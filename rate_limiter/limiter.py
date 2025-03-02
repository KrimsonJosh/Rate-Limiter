import redis 
from flask import request, jsonify 
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB, RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

class RateLimiter:
    def __init__(self, max_requests=RATE_LIMIT_MAX_REQUESTS, window=RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.window = window
    '''
        Rate Limiting decorator Using redis fixed window counter
        :max requests: max allowed requests within window
        :window: time (in seconds)
    '''
    def limit(self, max_requests: int, window: int):
        def decorator(func):
            def wrapper(*args, **kwargs):
                client_ip = request.remote_addr
                key = f"rate_limit:{client_ip}"

                current_count = self.redis.get(key)
                if current_count is None:
                    self.redis.setex(key, window, 1)
                else:
                    current_count = int(current_count)
                    if current_count >= max_requests:
                        return jsonify({"error": "Rate limit exceeded"}), 429
                    self.redis.incr(key)

                return func(*args, **kwargs)

            return wrapper
        return decorator