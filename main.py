from flask import Flask, render_template, request
import yfinance as yf
from static.trending_ticks import get_filtered_trending_tickers
from datetime import datetime
from pytz import timezone
from static.finance import get_close_time, get_off_trade_price, is_market_open

app = Flask(__name__)

# Set the timezone to US Eastern Time
us_eastern = timezone('US/Eastern')

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    datetime_us = datetime.now(us_eastern)

    if request.method == 'POST':
        symbols_input = request.form.get('symbol')

        if symbols_input:
            symbols = [symbol.strip().upper() for symbol in symbols_input.split(',')]
            market_open = is_market_open()

            for symbol in symbols:
                try:
                    stock = yf.Ticker(symbol)
                    hist = stock.history(period="1d")

                    if not hist.empty:
                        last_close_price = hist['Close'].iloc[-1]
                        open_price = hist['Open'].iloc[-1]
                        current_date = datetime_us.strftime("%d-%m-%Y")
                        offline_price = get_off_trade_price(symbol)

                        result_data = {
                            'symbol': symbol,
                            'date': current_date,
                            'open': f"Open Price: {open_price:.2f}",
                            'marketClosed': not market_open
                        }

                        if market_open:
                            # Market is open → Live price
                            live_price = stock.info.get('currentPrice', last_close_price)
                            result_data['price'] = f"Live Price: {live_price:.2f}"
                            result_data['time'] = f"Market is open - {datetime_us.strftime('%I:%M %p')} EST"
                        else:
                            # Market closed → Last close price + offline price if available
                            result_data['price'] = f"Market Closed Price: {last_close_price:.2f}"
                            result_data['time'] = f"Market closed at 4:00 PM EST on {datetime_us.strftime('%A, %B %d')}"
                            if offline_price:
                                result_data['tradeOff'] = f"Offline Price (After-Hours): {offline_price}"

                        results.append(result_data)

                    else:
                        # No data available
                        results.append({
                            'symbol': symbol,
                            'time': '',
                            'date': '',
                            'price': "No data available for today.",
                            'marketClosed': not market_open
                        })

                except Exception as e:
                    results.append({
                        'symbol': symbol,
                        'time': '',
                        'date': '',
                        'price': "Please enter a valid stock symbol or double-check the spelling.",
                        'marketClosed': not market_open
                    })
        else:
            results.append("Please enter at least one stock symbol.")

    # Fetch trending stock symbols
    trending_tickers = get_filtered_trending_tickers()

    return render_template('index.html', results=results, trending_tickers=trending_tickers)

if __name__ == '__main__':
    app.run(debug=True)
