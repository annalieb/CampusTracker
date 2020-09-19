from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
import json
import urllib
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/wellesley')
def wellesley():
    results = get_wellesley_data()
    return render_template('wellesley.html', data=results)

def get_wellesley_data():
    url = "https://www.wellesley.edu/coronavirus/dashboard"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('span', class_='number')
    data = ['Wellesley']
    for r in results:
        data.append(r.text)
    return data # College name, weekly tests, weekly positive cases

def get_mit_data():
    return None

if __name__ == "__main__":
    app.debug = True
    app.run()

# Getting scraping job
# pop = urllib.request.urlopen("https://api.webscraper.io/api/v1/scraping-job/2817859/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU")
# data = [json.loads(pop.read())]

# Data for creating scraping job
# scraping_job_creation = {
# 	"sitemap_id": 331219,
# 	"driver": "fulljs",
# 	"page_load_delay": 2000,
# 	"request_interval": 2000,
# 	"proxy": 0
# }
# Converting to json object?
# json_object = json.dumps(scraping_job_creation)
# new_json = json.loads(json_object)
# print(json_object)
# print(type(json_object))
# data = urllib.parse.urlencode(scraping_job_creation).encode()
# data = data.encode('ascii')
# req = urllib.request.urlopen("https://api.webscraper.io/api/v1/scraping-job?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU", data)
# with req as f:
#     print(f.read().decode('utf-8'))
#resp = urllib.request.urlopen(req)
