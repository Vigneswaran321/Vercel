from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import datetime
from gpt import get_response

app = Flask(__name__, static_folder='static')

latest_headlines = [{"text": "", "time": None}] * \
    10  # Initialize with empty headlines


def get_latest_headlines():
    url = 'https://www.prnewswire.com/news-releases/news-releases-list/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')
    # Get the latest 10 headlines
    return [headline.text.strip() for headline in headlines[:10]]


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route('/news')
def news():
    return render_template('news.html')

@app.route("/get", methods=["GET", "POST"])
def gpt_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/get_latest_headlines')
def send_latest_headlines():
    headlines = get_latest_headlines()
    print('Latest headlines:', headlines)  # Add print statement to debug
    return jsonify({"headlines": headlines})


if __name__ == '__main__':
    app.run(debug=False)
