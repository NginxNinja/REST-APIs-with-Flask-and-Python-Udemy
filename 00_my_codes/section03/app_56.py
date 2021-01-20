# Your first Flask application
# https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5960110#notes

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world!"

app.run(port=5000)