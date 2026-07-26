from flask import Flask, render_template, request
import requests

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    company_name = request.args.get('company_name', 'AAPL').strip().upper()


    search_url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + company_name + "&apikey=" + api_key
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if "bestMatches" in search_data and len(search_data["bestMatches"]) > 0:
        symbol = search_data["bestMatches"][0]["1. symbol"]
    else:
        symbol = company_name


    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol + "&apikey=" + api_key
    r = requests.get(url)
    data = r.json()

    if "Global Quote" in data and "05. price" in data["Global Quote"]:
        price = data["Global Quote"]["05. price"]
    else:
        price = "Price data isn't available right now, possibly due to API rate limits."

    news_url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + symbol + "&apikey=" + api_key
    news_response = requests.get(news_url)
    news_data = news_response.json()

    if "feed" in news_data:
        articles = news_data["feed"][:5]
    else:
        articles = []

    return render_template('index.html', symbol=symbol, price=price, articles=articles)

# app.run(host="127.0.0.1", port=5000)