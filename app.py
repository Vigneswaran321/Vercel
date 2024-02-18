from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)

latest_headlines = [{"text": "", "time": None}] * 10  # Initialize with empty headlines

def get_latest_headlines():
    url = 'https://www.prnewswire.com/news-releases/news-releases-list/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')
    return [headline.text.strip() for headline in headlines[:10]]  # Get the latest 10 headlines


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_latest_headlines')
def send_latest_headlines():
    headlines = get_latest_headlines()
    print('Latest headlines:', headlines)  # Add print statement to debug
    return jsonify({"headlines": headlines})

if __name__ == '__main__':
    app.run(debug=False)
