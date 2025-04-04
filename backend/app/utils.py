import requests

from bs4 import BeautifulSoup


def get_usd_uah_rate():
    try:
        url = "https://bank.gov.ua/ua/markets/exchangerates"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        usd_row = soup.find('td', text='Долар США').find_parent('tr')
        rate = float(usd_row.find_all('td')[1].text.replace(',', '.'))
        return rate
    except Exception:
        return 36.5