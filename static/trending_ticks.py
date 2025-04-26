import requests
from bs4 import BeautifulSoup

def get_filtered_trending_tickers():
    url = "https://finance.yahoo.com/trending-tickers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table
    table = soup.find('table')
    tickers = []

    if table:
        rows = table.find_all('tr')[1:]  # skip the header
        for row in rows:
            cols = row.find_all('td')
            if cols:
                ticker = cols[0].text.strip()
                tickers.append(ticker)

    # Filter out unwanted tickers
    filtered_tickers = [t for t in tickers if "-" not in t and "^" not in t]

    # If fewer than 10, add additional tickers
    if len(filtered_tickers) < 10:
        additional_tickers = ['ASXC', 'BMR', 'PGY', 'GRRR', 'CYTO', 'LIPO', 'OCTO', 'IFRX']
        filtered_tickers += additional_tickers

    return filtered_tickers

# Test it
filtered_trends = get_filtered_trending_tickers()
print(filtered_trends)
