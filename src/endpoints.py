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

import time

app = Flask(__name__)
CORS(app)

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
s = Service('C:/Program Files/chromedriver-win64/chromedriver.exe')

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
        return jsonify({'jobs': jobs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

