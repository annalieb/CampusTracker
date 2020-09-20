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
import csv
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/wellesley')
def wellesley():
    tests, pos = college_data_csv('Wellesley')
    return render_template('wellesley.html', tests=tests, pos=pos)

@app.route('/mit')
def mit():
    tests, pos = college_data_csv('MIT')
    return render_template('mit.html', tests=tests, pos=pos)

@app.route('/harvard')
def harvard():
    tests, pos = college_data_csv('Harvard')
    return render_template('harvard.html', tests=tests, pos=pos)

@app.route('/bu')
def bu():
    tests, pos = college_data_csv('BU')
    return render_template('bu.html', tests=tests, pos=pos)

@app.route('/bc')
def bc():
    tests, pos = college_data_csv('BC')
    return render_template('bc.html', tests=tests, pos=pos)

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
    results = 'Wellesley,' + data['weekly-asymptomatic-results'].replace(',', '') + ',' + data['weekly-positive-results'].replace(',', '') + '\n'
    print('scraped')
    print(results)
    return results # College name, weekly tests, weekly positive cases

def get_mit_data():
    scraping_job_creation = {
    	"sitemap_id": 331288,
    	"driver": "fulljs",
    	"page_load_delay": 2000,
    	"request_interval": 2000,
    	"proxy": 0
    }
    scraping_job_id = 2819616
    url = "https://api.webscraper.io/api/v1/scraping-job/" + str(scraping_job_id).strip() + "/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU"
    pop = requests.get(url)
    data = json.loads(pop.text)
    # Adding daily totals for tests and positive tests
    tests_array = ['sat-tests', 'fri-tests', 'thurs-tests', 'wed-tests', 'tues-tests', 'mon-tests', 'sun-tests']
    tests_total = 0
    for test in tests_array:
        tests_total += float(str(data[test]).replace(',', ''))
    pos_tests_array = ['sat-pos-tests', 'fri-pos-tests', 'thurs-pos-tests', 'wed-pos-tests', 'tues-pos-tests', 'mon-pos-tests', 'sun-pos-tests']
    pos_tests_total = 0
    for pos_test in pos_tests_array:
        pos_tests_total += float(str(data[pos_test]).replace(',', ''))
    results = 'MIT,' + str(int(tests_total)) + ',' + str(int(pos_tests_total)) + '\n'
    print('scraped')
    print(results)
    return results # College name, weekly tests, weekly positive cases

def get_harvard_data():
    scraping_job_creation = {
    	"sitemap_id": 331306,
    	"driver": "fulljs",
    	"page_load_delay": 2000,
    	"request_interval": 2000,
    	"proxy": 0
    }
    req = requests.post("https://api.webscraper.io/api/v1/scraping-job?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU", json=scraping_job_creation)
    resp = json.loads(req.text)
    scraping_job_id = int(resp['data']['id'])
    time.sleep(40)
    url = "https://api.webscraper.io/api/v1/scraping-job/" + str(scraping_job_id).strip() + "/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU"
    pop = requests.get(url)
    data = json.loads(pop.text)
    results = 'Harvard,' + data['7-days-tests'][:-1].replace(',', '') + ',' + data['7-days-pos-tests'].replace(',', '') + '\n'
    print('scraped')
    print(results)
    return results # College name, weekly tests, weekly positive cases

def get_bu_data():
    scraping_job_creation = {
    	"sitemap_id": 331315,
    	"driver": "fulljs",
    	"page_load_delay": 15000,
    	"request_interval": 2000,
    	"proxy": 0
    }
    req = requests.post("https://api.webscraper.io/api/v1/scraping-job?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU", json=scraping_job_creation)
    resp = json.loads(req.text)
    scraping_job_id = int(resp['data']['id'])
    time.sleep(60)
    url = "https://api.webscraper.io/api/v1/scraping-job/" + str(scraping_job_id).strip() + "/json?api_token=kBwQqhHkuCA1zvQXc44plXxzi0wLo90HqTWAbV01xGCMMS8YiXI1TO2hpkCU"
    pop = requests.get(url)
    data = json.loads(pop.text)
    daily_avg_tests = float(data['7-day-avg-daily-tests'][0:5].replace(',', ''))
    daily_pos_rate = float(data['7-day-avg-pos-rate'][0:4]) / 100
    results = 'BU,' + str(int(daily_avg_tests * 7)) + ',' + str(int(daily_avg_tests * 7 * daily_pos_rate)) + '\n'
    print('scraped')
    print(results)
    return results # College name, weekly tests, weekly positive cases

def get_bc_data():
    scraping_job_creation = {
    	"sitemap_id": 331319,
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
    results = ['BC', data['7-day-tests'], data['7-day-pos-tests']]
    results = 'BC,' + data['7-day-tests'].replace(',', '') + ',' + data['7-day-pos-tests'].replace(',', '') + '\n'
    print('scraped')
    print(results)
    return results # College name, weekly tests, weekly positive cases

def write_csv():
    f = open('school_data.csv', 'w')
    result_str = get_wellesley_data() + get_mit_data() + get_harvard_data() + get_bu_data() + get_bc_data()
    f.write(result_str)
    f.close()

def college_data_csv(college):
    with open('school_data_backup.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] == college:
                return row[1], row[2]

if __name__ == "__main__":
    # write_csv()
    app.debug = True
    app.run()
