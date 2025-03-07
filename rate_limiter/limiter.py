import redis 
from flask import request, jsonify 
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB, RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW
import time
import logging

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

logging.basicConfig(level=logging.INFO)

class RateLimiter:
    def __init__(self, redis_client, max_requests=RATE_LIMIT_MAX_REQUESTS, window=RATE_LIMIT_WINDOW):
        self.max_requests = max_requests
        self.window = window
        self.redis_client = redis_client
    '''
        Rate Limiting decorator Using redis sliding window counter
        :max requests: max allowed requests within window
        :window: time (in seconds)
    '''
    def limit(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                client_ip = request.remote_addr
                key = f"rate_limit:{client_ip}"
                current_time = int(time.time())
                pipeline = redis_client.pipeline() 
                # Remove Outdated entries 
                pipeline.zremrangebyscore(key, 0, current_time - self.window)
                # Count current entries within dynamic window
                pipeline.zcard(key) 
                # Add the current request 
                pipeline.zadd(key, {f"{current_time}-{time.time()}": current_time}) 
                # Set expiry for key to automatically clean old keys
                pipeline.expire(key, self.window+1)
                results = pipeline.execute() 

                request_count = results[1] 
                # If limit reached, block the request
                if request_count > self.max_requests:
                    return jsonify({"error": "Rate Limit Exceeded"}), 429

         
                return func(*args, **kwargs)

            return wrapper
        return decorator
    
    def get_client_identifier(self):
        """
        Returns an Identifier for rate-limiting
        """
        return f"ip:{request.remote_addr}" 
    
    def log_rate_limit_violation(self, client_id):
        self.redis_client.incr("rate_limit_violations_total") 
        self.redis_client.zincrby("blocked clients", 1, client_id)
        logging.warning(f"Rate limit exceeded for {client_id}")