import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import random
import boto3
import time

s3 = boto3.client('s3')
BUCKET_NAME = 'job-webscrape'
ACCEPTED_FILE_PATH = '/accepted/'
ACCEPTED_FILE_NAME = 'accepted.json'
ACCEPTED_KEY = ACCEPTED_FILE_PATH + ACCEPTED_FILE_NAME

DECLINED_FILE_PATH = '/declined/'
DECLINED_FILE_NAME = 'declined.json'
DECLINED_KEY = DECLINED_FILE_PATH + DECLINED_FILE_NAME

app = Flask(__name__)
CORS(app)

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
s = Service('C:/Program Files/chromedriver-win64/chromedriver.exe')


def load_links_from_s3(bucketKey):
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=bucketKey)
        links = json.loads(obj['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        links = []
    return links

def save_links_to_s3(bucketKey,links):
    links_json = json.dumps(links)
    s3.put_object(Bucket=BUCKET_NAME,Key=bucketKey, Body=links_json)

@app.route('/job/accepted', methods=['POST'])
def saveAccepted():
    data = request.get_json()
    if not data or 'link' not in data:
        return jsonify({'error': 'data not complete'}), 400

    link = data['link']

    accepted_links = load_links_from_s3(ACCEPTED_KEY)

    accepted_links.append(link)

    save_links_to_s3(ACCEPTED_KEY,accepted_links)

    return jsonify({'message': 'retrieved link and saved link to s3 bucket', 'link': link}), 200

@app.route('/job/declined', methods=['POST'])
def saveDeclined():
    data = request.get_json()
    if not data or 'link' not in data:
        return jsonify({'error': 'data not complete'}), 400

    link = data['link']

    declined_links = load_links_from_s3(DECLINED_KEY)

    declined_links.append(link)

    save_links_to_s3(DECLINED_KEY,declined_links)

    return jsonify({'message': 'retrieved link and saved link to s3 bucket', 'link': link}), 200


@app.route('/scrape/google', methods=['POST'])
def scrapeGoogle():

    data = request.json
    query = data.get('description')
    if not query:
        return jsonify({'error': 'Google Query is required'}), 400


    # URL encode the query
    encoded_query = urllib.parse.quote_plus(query)
    driver = webdriver.Chrome(service=s, options=chrome_options)
    time.sleep(random.randint(1,3))
    driver.maximize_window()
    url=f'https://www.google.com/search?q=jobs%20london%20{encoded_query}&jbr=sep:0&udm=8&ved=2ahUKEwip7Iq026mIAxXFWUEAHTNoAccQ3L8LegQIIRAM'
    driver.get(url)
    time.sleep(random.randint(1,3))
    driver.find_element(By.XPATH,"//*[@id='W0wltc']/div").click()
    time.sleep(random.randint(1,3))
    for i in range(10):
        driver.execute_script('window.scrollBy(0, 3000)')
        time.sleep(random.randint(1,5))
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        specific_div = soup.find('div', class_='ZNyqGc')
        jobs=[]

        for a_tag in specific_div.find_all('a', href=True):
            job_link = a_tag['href']
            job_name_div = a_tag.find('div', class_='tNxQIb PUpOsf')
            job_name = job_name_div.get_text(strip=True)

            jobs.append ({
                'link': job_link,
                'name': job_name
            })

        driver.close()
        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape/linkedin', methods=['POST'])
def scrapeLinked():
    data = request.json
    query = data.get('description')
    if not query:
        return jsonify({'error': 'LinkedIn needs a query'}), 400

    encoded_query = urllib.parse.quote_plus(query)

    driver = webdriver.Chrome(service=s)
    time.sleep(random.randint(1,3))
    driver.maximize_window()
    url=f"https://www.linkedin.com/jobs/search?keywords={encoded_query}&location=London%20Area%2C%20United%20Kingdom&geoId=90009496&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    driver.get(url)
    time.sleep(random.randint(1,3))
    try:
        soup = BeautifulSoup(driver.page_source,'html.parser')
        specific_div = soup.find('ul', class_='jobs-search__results-list')
        jobs = []

        for job_item in specific_div.find_all('li'):  # Loop through each <li> element (job listing)
            a_tag = job_item.find('a', href=True)  # Find the <a> tag
            job_link = a_tag['href'] if a_tag else "No link found"  # Extract the href

            job_name_div = job_item.find('span', class_='sr-only')  # Find the <span> inside the same <li>
            job_name = job_name_div.get_text(strip=True) if job_name_div else "No job name found"

            jobs.append({
                'link': job_link,
                'name': job_name
            })

        driver.close()
        return jsonify({'jobs': jobs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

