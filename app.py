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

@app.route('/bu')
def bu():
    resp = get_bu_data()
    return render_template('bu.html', data=resp)

@app.route('/nu')
def nu():
    resp = get_nu_data()
    return render_template('nu.html', data=resp)

@app.route('/bc')
def bc():
    resp = get_bc_data()
    return render_template('bc.html', data=resp)

@app.route('/babson')
def babson():
    resp = get_babson_data()
    return render_template('babson.html', data=resp)

@app.route('/olin')
def olin():
    resp = get_olin_data()
    return render_template('olin.html', data=resp)

@app.route('/brandeis')
def brandeis():
    resp = get_brandeis_data()
    return render_template('brandeis.html', data=resp)

@app.route('/tufts')
def tufts():
    resp = get_tufts_data()
    return render_template('tufts.html', data=resp)

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
    time.sleep(30)
    url = "https://api.webscraper.io/api/v1/scraping-job/" + str(scraping_job_id).strip() + "/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU"
    pop = requests.get(url)
    data = json.loads(pop.text)
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
    # req = requests.post("https://api.webscraper.io/api/v1/scraping-job?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU", json=scraping_job_creation)
    # resp = json.loads(req.text)
    # scraping_job_id = int(resp['data']['id'])
    # time.sleep(60)
    scraping_job_id = 2819616
    url = "https://api.webscraper.io/api/v1/scraping-job/" + str(scraping_job_id).strip() + "/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU"
    pop = requests.get(url)
    data = json.loads(pop.text)
    tests_array = ['sat-tests', 'fri-tests', 'thurs-tests', 'wed-tests', 'tues-tests', 'mon-tests', 'sun-tests']
    tests_total = 0
    for test in tests_array:
        tests_total += float(str(data[test]).replace(',', ''))
    pos_tests_array = ['sat-pos-tests', 'fri-pos-tests', 'thurs-pos-tests', 'wed-pos-tests', 'tues-pos-tests', 'mon-pos-tests', 'sun-pos-tests']
    pos_tests_total = 0
    for pos_test in pos_tests_array:
        pos_tests_total += float(str(data[pos_test]).replace(',', ''))
    # tests = float(data['sat-tests']) + float(data['fri-tests']) + data['thurs-tests'] + data['wed-tests'] + data['tues-tests'] + data['mon-tests'] + data['sun-tests']
    # pos_tests = data['sat-pos-tests'] + data['fri-pos-tests'] + data['thurs-pos-tests'] + data['wed-pos-tests'] + data['tues-pos-tests'] + data['mon-pos-tests'] + data['sun-pos-tests']
    results = ['MIT', int(tests_total), int(pos_tests_total)]
    return results # College name, weekly tests, weekly positive cases

def get_harvard_data():
    url = "https://www.harvard.edu/coronavirus/harvard-university-wide-covid-19-testing-dashboard"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='card__text')
    data = ['Harvard']
    data.append(results[0].text.strip()[:-1])
    data.append(results[1].text.strip())
    return data # College name, weekly tests, weekly positive cases

def get_bu_data():
    return "hi"

def get_nu_data():
    return "hi"

def get_bc_data():
    return "hi"

def get_babson_data():
    return "hi"

def get_olin_data():
    return "hi"

def get_brandeis_data():
    return "hi"

def get_tufts_data():
    return "hi"

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
