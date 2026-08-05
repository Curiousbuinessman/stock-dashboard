from flask import Flask, render_template, request
import requests
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

app = Flask(__name__)

top_gainers_url = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=" + api_key
top_gainers_response = requests.get(top_gainers_url)
top_movers_data = top_gainers_response.json()

top_gainers = top_movers_data.get("top_gainers", [])[:5]
top_losers = top_movers_data.get("top_losers", [])[:5]
most_actively_traded = top_movers_data.get("most_actively_traded", [])[:5]

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


    overview_url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=" + symbol + "&apikey=" + api_key
    overview_response = requests.get(overview_url) 
    overview_data = overview_response.json()

    if "Name" in overview_data:
        official_name = overview_data["Name"]
        sector = overview_data["Sector"]
    else:
        official_name = "Company name not found"
        sector = "Sector not found"

    news_url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + symbol + "&apikey=" + api_key
    news_response = requests.get(news_url)
    news_data = news_response.json()


    if "feed" in news_data:
        articles = news_data["feed"][:5]
        for article in articles:
            raw_time = article["time_published"]
            parsed = datetime.strptime(raw_time, "%Y%m%dT%H%M%S")
            article["time_published"] = parsed.strftime("%B %d, %Y %I:%M %p")
    else:
        articles = []



    return render_template('index.html', symbol=symbol, price=price, articles=articles, official_name=official_name, sector=sector, top_gainers=top_gainers, top_losers=top_losers, most_actively_traded=most_actively_traded)






if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)