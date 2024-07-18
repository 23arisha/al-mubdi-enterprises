import requests
from bs4 import BeautifulSoup

def get_close_time(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div element with the specified ID
        div_element = soup.find('span', {'class': 'svelte-1dnpe7s'})

        # Extract the content inside the div element
        if div_element:
            close_time = div_element.text.strip()
            return close_time
        else:
            return None

def get_off_trade_price(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        fin_streamer = soup.find('fin-streamer', class_="price svelte-mgkamr")
        
        if fin_streamer:
            value = fin_streamer.text.strip()
            return value
        else:
            return None
        
def isCloseMarket():
    closetime= "At close:4:00PM EST"
    return closetime

print(get_off_trade_price('pgy'))