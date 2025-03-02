import pytest
from flask import Flask 
from rate_limiter.limiter import RateLimiter

app = Flask(__name__)
limiter = RateLimiter() 

@app.route('/')
@limiter.limit(max_requests=3, window=10)
def home():
    return "Hello World"

client = app.test_client()

def test_rate_limit():
    for _ in range(3):
        res = client.get('/')
        assert res.status_code() == 200

    # 4th request Breaks Limit 
    res = client.get('/') 
    assert res.status_code() == 429
