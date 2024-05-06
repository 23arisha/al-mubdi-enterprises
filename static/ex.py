import requests
from bs4 import BeautifulSoup

def get_filtered_trending_tickers():

    url = "https://finance.yahoo.com/trending-tickers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send a GET request with headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'a' tags with attribute 'data-test' set to 'quoteLink'
    ticker_elements = soup.find_all('a', attrs={'data-test': 'quoteLink'})

    # Extract text content (tickers) from the 'a' tags
    trend_tickers = [element.text.strip() for element in ticker_elements]

    filtered_tickers = [ticks for ticks in trend_tickers if "-" not in ticks and "^" not in ticks]

    # If the length is less than 10, populate with additional tickers
    if len(filtered_tickers) < 10:
        additional_tickers = ['ASXC', 'BMR', 'PGY', 'GRRR', 'CYTO', 'LIPO', 'OCTO', 'IFRX']
        filtered_tickers += additional_tickers

    return filtered_tickers

filtered_trends = get_filtered_trending_tickers()
print(filtered_trends)
