import time 
import redis 
from flask import request, jsonify 


class RateLimiter:
    def __init__(self, redis_host="localhost", redis_port = 6379, redis_db=0):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db = redis_db, decode_responses= True)
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