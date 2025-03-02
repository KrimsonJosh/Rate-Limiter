import time 
import redis 
from flask import request, jsonify 

redis_client = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True)

def rate_limiter(max_requests: int, window: int):
    '''
        Rate Limiting decorator Using redis fixed window counter
        :max requests: max allowed requests within window
        :window: time (in seconds)
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            client_IP = request.remote_addr 
            key = f"rate_limit{client_IP}"

            # Current Request Count 
            current_count = redis_client.get(key) 

            if current_count is None:
                # First request, initialize 
                redis_client.setex(key, window, 1)
            else:
                current_count = int(current_count) 
                if current_count >= max_requests:
                    return jsonify({
                        "error": "Rate Limit Exceeded",
                        "retry_after": redis_client.ttl(key)
                    }), 429 
                redis_client.incr(key) # Increments count 

            return func(*args, **kwargs) 
        return wrapper 
    return decorator