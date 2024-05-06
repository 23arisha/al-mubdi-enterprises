from flask import Flask, render_template, request
import yfinance as yf
from static.ex import get_filtered_trending_tickers
from datetime import datetime
from pytz import timezone
from static.finance import isCloseMarket, get_close_time, get_off_trade_price

app = Flask(__name__)

# Set the timezone to the USA (Eastern Time Zone - ET)
us_eastern = timezone('US/Eastern')
datetime_us = datetime.now(us_eastern)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []

    if request.method == 'POST':
        symbols_input = request.form.get('symbol')

        if symbols_input:
            symbols = [symbol.strip() for symbol in symbols_input.split(',')]
            marketClose = isCloseMarket()

            for symbol in symbols:
                try:
                    stock = yf.Ticker(symbol)
                    current_price = stock.info['currentPrice']
                    open__price = stock.info['open']
                    current_time = get_close_time(symbol)
                    current_date = datetime_us.strftime("%d-%m-%Y")
                    
                    # Fetch offline trading price
                    offline_price = get_off_trade_price(symbol)

                    if offline_price is not None:
                        results.append({
                            'symbol': symbol,
                            'time': current_time,
                            'date': current_date,
                            'price': f"Current Price: {current_price}",
                            'marketClosed': True if marketClose else False,
                            'tradeOff' : f"Offline Price: {offline_price}"
                        })
                    else:
                        results.append({
                            'symbol': symbol,
                            'time': current_time,
                            'date': current_date,
                            'price': f"Current Price: {current_price}",
                            'marketClosed': False
                        })

                except Exception as e:
                    results.append({
                        'symbol': symbol,
                        'time': '',
                        'date': '',
                        'price': "Please enter valid stock symbol or double-check the spelling.",
                        'marketClosed': False
                    })
        else:
            results.append("Please enter at least one stock symbol.")

    # Fetch trending stock symbols using ex.py
    trending_tickers = get_filtered_trending_tickers()

    return render_template('index.html', results=results, trending_tickers=trending_tickers)

if __name__ == '__main__':
    app.run(debug=True)
