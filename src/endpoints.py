from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
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

@app.route('/scrape/google', methods=['POST'])
def scrapeGoogle():

    data = request.json
    query = data.get('description')
    if not query:
        return jsonify({'error': 'Google Query is required'}), 400

    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')

    # URL encode the query
    encoded_query = urllib.parse.quote_plus(query)
    s = Service('C:/Program Files/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    time.sleep(2)
    driver.maximize_window()
    url=f'https://www.google.com/search?q=jobs%20london%20{encoded_query}&jbr=sep:0&udm=8&ved=2ahUKEwip7Iq026mIAxXFWUEAHTNoAccQ3L8LegQIIRAM'
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH,"//*[@id='W0wltc']/div").click()
    time.sleep(3)
    for i in range(10):
        driver.execute_script('window.scrollBy(0, 3000)')
        time.sleep(random.randint(1,5))
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        specific_div = soup.find('div', class_='ZNyqGc')
        jobs=[]

        for a_tag in specific_div.find_all('a', href=True):
            jobs.append(a_tag['href'])

        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500