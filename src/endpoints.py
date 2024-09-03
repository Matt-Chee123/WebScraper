from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)
@app.route('/scrape/', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [h.get_text() for h in soup.find_all(['h1','h2','h3'])]
        return jsonify({'links': links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
