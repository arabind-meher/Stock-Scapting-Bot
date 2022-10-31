import requests
from requests.exceptions import Timeout
from bs4 import BeautifulSoup


def get_stock_data(symbol: str):
    url = f'https://site.financialmodelingprep.com/financial-summary/{symbol}'

    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')

        name = soup.find('h4', class_='company-name').text.strip()
        price = soup.find('h4', class_='company-price').text.strip()
        change = soup.find('div', class_='company-change').text.strip()

        return name, price, change
    except Timeout:
        return 'timeout'
    except AttributeError:
        return 'not-found'
