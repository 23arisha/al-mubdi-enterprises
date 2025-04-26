import requests
from datetime import datetime
from pytz import timezone
from bs4 import BeautifulSoup
import yfinance as yf

# Set the timezone to the USA (Eastern Time Zone - ET)
us_eastern = timezone('US/Eastern')

def is_market_open():
    now = datetime.now(us_eastern)
    current_time = now.strftime("%H:%M")
    current_day = now.weekday()  # Monday = 0, Sunday = 6

    market_open_time = "09:30"
    market_close_time = "16:00"

    if current_day >= 5:  # Saturday (5) or Sunday (6)
        return False
    if market_open_time <= current_time <= market_close_time:
        return True
    return False

def get_close_time():
    now = datetime.now(us_eastern)
    if is_market_open():
        return f"Market is currently open (Time: {now.strftime('%I:%M %p')} EST)"
    else:
        return f"Market closed at 4:00 PM EST on {now.strftime('%A, %B %d')}"
    

def get_off_trade_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return info.get('postMarketPrice')
    except Exception as e:
        print(f"Error fetching offline price for {symbol}: {e}")
        return None
    

def get_market_info(symbol):
    marketClose = get_close_time()  # Determine if the market is closed
    close_time = get_close_time() if marketClose else None
    offline_price = get_off_trade_price(symbol) if marketClose else None

    return marketClose, close_time, offline_price

# Example usage:
symbol = "WW"
marketClosed, close_time, offline_price = get_market_info(symbol)
print(f"Market closed: {marketClosed}, Close Time: {close_time}, Offline Price: {offline_price}")
