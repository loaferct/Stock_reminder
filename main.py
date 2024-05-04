import requests
from datetime import datetime, timedelta
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_url = 'https://www.alphavantage.co/query'
stock_api_key = 'xxxxxxxxxxxxx'
news_api_key = 'xxxxxxxxxxxxxx'


## To find the date of yesterday and day before yesterday
today = datetime.today()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

day_before_yesterday = today - timedelta(days=2)
day_before_yesterday_str = day_before_yesterday.strftime('%Y-%m-%d')

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameters ={
    'function' : 'TIME_SERIES_DAILY',
    'symbol' : STOCK,
    'apikey' : stock_api_key
}


stock_response = requests.get(stock_url, params = stock_parameters)
price_data = stock_response.json()
yesterday_price = float(price_data['Time Series (Daily)'][yesterday_str]['4. close'])
day_before_yesterday_price = float(price_data['Time Series (Daily)'][day_before_yesterday_str]['4. close'])

percent_change = float((yesterday_price-day_before_yesterday_price)/(yesterday_price))*100



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_url = 'https://newsapi.org/v2/everything?'
news_parameters = {
    'q' : 'tesla',
    'from' : yesterday_str,
    'sortBy' : 'popularity',
    'apikey' : news_api_key
}
titles = []
news_response = requests.get(news_url, params = news_parameters)
news_data = news_response.json()
articles = news_data['articles']
for number in range(0,3):
    titles.append(articles[number]['title'])


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title to your phone number. 
account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client = Client(account_sid, auth_token)


message = client.messages \
                    .create(
                        body=percent_change,
                        from_='+12564xxxxx',
                        to='+9779842222222'
                    )

for title in titles:
    message = client.messages \
                    .create(
                        body=title,
                        from_='+12564xxxxx',
                        to='+9779842222222'
                    )

