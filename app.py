from flask import Flask 
from rate_limiter.limiter import RateLimiter

app = Flask('__main__')
limiter = RateLimiter()

@app.get('/')
@limiter.limit(max_requests = 5, window = 60)
def main():
    return ("Hello World.") 

if __name__ == '__main__':
    app.run(debug = True)