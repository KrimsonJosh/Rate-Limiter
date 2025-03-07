from flask import Flask 
from rate_limiter import RateLimiter

app = Flask('__main__')
limiter = RateLimiter(4, 60)

@app.get('/')
@limiter.limit()
def main():
    return ("Hello World.") 

if __name__ == '__main__':
    app.run(debug = True)