from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello world!"

if __name__ == "__main__":
    app.debug = True
    app.run()
