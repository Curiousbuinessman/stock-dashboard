import requests

search_term = input("Good evening sir, Which company would you like to delve into?").strip()

api_key = "7AGJPP9E1HKIOPJK"

search_url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + search_term + "&apikey=" + api_key
search_response = requests.get(search_url)
search_data = search_response.json()


if "bestMatches" in search_data and len(search_data["bestMatches"]) > 0:
    symbol = search_data["bestMatches"][0]["1. symbol"]
    print ("Great choice sir, let's get some information on " + search_term + " stock")
else: 
    print("Couldn't find a matching stock for that name.")

exit()

url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol + "&apikey=" + api_key

r = requests.get(url)
data = r.json()

if "Global Quote" in data and "05. price" in data["Global Quote"]:
    price = data["Global Quote"]["05. price"]
    print("The current price of " + symbol + " is $" + price)
else:
    print("Price data isn't available right now, possibly due to API rate limits.")




news_url = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=" + symbol + "&apikey=" + api_key

# NEWS SECTION

news_response = requests.get(news_url)
news_data = news_response.json()

print("Here are the latest news articles for " + symbol + ":")

if "feed" in news_data:
    articles = news_data["feed"]
    print("Here are the latest news articles for " + symbol + ":")
    for article in articles[:5]:
        title = article["title"]
        sentiment = article["overall_sentiment_label"]
        print(title + " -- Sentiment: " + sentiment)
else:
    print("News data isn't available right now, possibly due to API rate limits.")


print(news_data)
