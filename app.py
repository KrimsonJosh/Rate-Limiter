from flask import Flask 
from rate_limiter import rate_limiter

app = Flask('__main__')

@app.get('/')
@rate_limiter(max_requests = 5, window = 60)
def main():
    return ("Hello World.") 

if __name__ == '__main__':
    app.run(debug = True)