from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
import json
import urllib

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/wellesley')
def wellesley():
    pop = urllib.request.urlopen("https://api.webscraper.io/api/v1/scraping-job/2817859/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU")
    data = [json.loads(pop.read())]
    return render_template('wellesley.html', data=data)

if __name__ == "__main__":
    app.debug = True
    app.run()
