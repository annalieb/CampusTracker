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
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/wellesley')
def wellesley():
    resp = get_wellesley_data()
    return render_template('wellesley.html', data=resp)

@app.route('/mit')
def mit():
    resp = get_mit_data()
    return render_template('mit.html', data=resp)

@app.route('/harvard')
def harvard():
    resp = get_harvard_data()
    return render_template('harvard.html', data=resp)

def get_wellesley_data():
    # Data for creating scraping job
    scraping_job_creation = {
    	"sitemap_id": 331219,
    	"driver": "fulljs",
    	"page_load_delay": 2000,
    	"request_interval": 2000,
    	"proxy": 0
    }
    req = requests.post("https://api.webscraper.io/api/v1/scraping-job?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU", json=scraping_job_creation)
    resp = json.loads(req.text)
    scraping_job_id = int(resp['data']['id'])
    print(scraping_job_id)
    # scraping_job_id = 2819617
    time.sleep(30)
    url = "https://api.webscraper.io/api/v1/scraping-job/" + str(scraping_job_id).strip() + "/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU"
    pop = requests.get(url)
    # pop = requests.get("https://api.webscraper.io/api/v1/scraping-job/2819611/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU")
    #print(pop.read())
    data = json.loads(pop.text)
    print(data)
    results = ['Wellesley', data['weekly-asymptomatic-results'], data['weekly-positive-results']]
    return results # College name, weekly tests, weekly positive cases

def get_mit_data():
    scraping_job_creation = {
    	"sitemap_id": 331288,
    	"driver": "fulljs",
    	"page_load_delay": 2000,
    	"request_interval": 2000,
    	"proxy": 0
    }
    resp = requests.post("https://api.webscraper.io/api/v1/scraping-job?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU", json=scraping_job_creation)
    print(resp.text)
    return resp.text

def get_harvard_data():
    url = "https://www.harvard.edu/coronavirus/harvard-university-wide-covid-19-testing-dashboard"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='card__text')
    data = ['Harvard']
    data.append(results[0].text.strip()[:-1])
    data.append(results[1].text.strip())
    return data # College name, weekly tests, weekly positive cases

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


# url = "https://www.wellesley.edu/coronavirus/dashboard"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# results = soup.find_all('span', class_='number')
# data = ['Wellesley']
# for r in results:
#     data.append(r.text)
