import pytest
import redis
from flask import Flask 
from rate_limiter import RateLimiter

test_redis = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

@pytest.fixture 
def app():
    app = Flask(__name__)
    limiter = RateLimiter(test_redis) 

    @app.route('/')
    @limiter.limit(max_requests=3, window=10)
    def home():
        return "Hello World"
    return app 

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture 
def flush_redis():
    # Flush Redis to ensure clean state each time.
    test_redis.flushdb()

def test_rate_limit():
    for _ in range(3):
        res = client.get('/')
        assert res.status_code == 200

    # 4th request Breaks Limit 
    res = client.get('/') 
    assert res.status_code == 429
