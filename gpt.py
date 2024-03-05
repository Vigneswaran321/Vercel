import os
import sys
import time
import openai
from collections import deque
import requests
from bs4 import BeautifulSoup

api_key = os.environ.get("OPENAI_API_KEY")
client = openai.Client(api_key=api_key)

systemPrompt = "You are a News Provider Bot where you provide features like News Summarization, Latest Headlines only by translating to in English Language by creating responses in a easy to understandable format from the given Headlines:"

data = deque(maxlen=10) # Adjust the maximum length as per requirements

GPT_MODEL = "gpt-3.5-turbo"  # Adjust accordingly.

def get_latest_headlines():
    url = 'https://www.prnewswire.com/news-releases/news-releases-list/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')
    # Get the latest 10 headlines
    return [headline.text.strip() for headline in headlines[:15]]

headlines = get_latest_headlines()

def get_response(prompt_msg):
    if prompt_msg == "clear":
        data.clear()
        data.append({"role": "assistant", "content": 'hello'})
    else:
        data.append({"role": "assistant", "content": prompt_msg})

    messages = [{"role": "system", "content": systemPrompt.join(headlines)}]
    messages.extend(data)
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            max_tokens=200,
            n=1,
            temperature=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        content = response.choices[0].message.content
        return content
    except client.ErrorObject as e:
        print(e)
        return ""
