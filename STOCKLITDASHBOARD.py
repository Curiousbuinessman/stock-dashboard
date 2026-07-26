import streamlit as st
import requests

st.title("Stock Dashboard")

symbol = st.text_input("Which stock would you like to delve into", "AAPL").strip().upper()

if st.button("Search"):
    api_key = "7AGJPP9E1HKIOPJK"

    url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol + "&apikey=" + api_key
    r = requests.get(url)
    data = r.json()


if "Global Quote" in data and "05. price" in data["Global Quote"]:
        price = data["Global Quote"]["05. price"]
        st.subheader("Price")
        st.write("The current price of " + symbol + " is $" + price)
else:
        st.write("Price data isn't available right now, possibly due to API rate limits.")

news_url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + symbol + "&apikey=" + api_key
news_response = requests.get(news_url)
news_data = news_response.json()

st.subheader("News")
if "feed" in news_data:
        articles = news_data["feed"]
        for article in articles[:5]:
            title = article["title"]
            sentiment = article["overall_sentiment_label"]
            st.write(title + " -- Sentiment: " + sentiment)
else:
        st.write("News data isn't available right now, possibly due to API rate limits.")