from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from bs4 import BeautifulSoup
import requests
import urllib.parse

app = Flask(__name__)
CORS(app)

@app.route('/scrape/google', methods=['POST'])
def scrape():
    data = request.json
    query = data.get('description')
    if not query:
        return jsonify({'error': 'Google Query is required'}), 400

    # URL encode the query
    encoded_query = urllib.parse.quote_plus(query)
    google_url = f"https://www.google.com/search?q={encoded_query}&sca_esv=1c4a2bf3bd651b6a&rlz=1C1AVFC_en-GBGB850GB850&sxsrf=ADLYWIKNp2n0T1vGmA-5LPyrD1j1gLdZAQ%3A1725461526607&ei=FnTYZuvYJImRhbIPtJen2AQ&ved=2ahUKEwi24cOjzamIAxXqW0EAHYfJCXwQ3L8LegQIIRAM&uact=5&oq=jobs%20london%20graduate%20software%20developer&gs_lp=Egxnd3Mtd2l6LXNlcnAiJ2pvYnMgbG9uZG9uIGdyYWR1YXRlIHNvZnR3YXJlIGRldmVsb3BlcjIKEAAYsAMY1gQYRzINEAAYsAMY1gQYRxjJAzIKEAAYsAMY1gQYRzIKEAAYsAMY1gQYRzIKEAAYsAMY1gQYRzIKEAAYsAMY1gQYRzIKEAAYsAMY1gQYRzIKEAAYsAMY1gQYRzIOEAAYgAQYsAMYkgMYigVIlApQAFgAcAN4AZABAJgBAKABAKoBALgBA8gBAPgBApgCA6ACDZgDAIgGAZAGCZIHATOgBwA&sclient=gws-wiz-serp&jbr=sep:0&udm=8"

    try:
        # Make the request with a user-agent header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        response = requests.get(google_url, headers=headers)
        response.raise_for_status()

        # Parse the response content
        soup = BeautifulSoup(response.text, 'html.parser')
        specific_div = soup.find('div', class_='ZNyqGc')

        # Extract headings (h1, h2, h3)
        if not specific_div:
            return jsonify({'error': 'Specific div not found'}), 404

        # Extract all hrefs within <a> tags inside the specific <div>
        jobs = []
        for a_tag in specific_div.find_all('a', href=True):
            jobs.append(a_tag['href'])
        return jsonify({'jobs': jobs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
