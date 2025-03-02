from flask import Flask 

app = Flask('__main__')

@app.get('/')
def main():
    return ("Hello World.") 

if __name__ == '__main__':
    app.run(debug = True)