import requests

from bs4 import BeautifulSoup


def get_usd_uah_rate():
    try:
        url = "https://bank.gov.ua/ua/markets/exchangerates"
        print("--------------------------------")
        print("Getting USD rate from:", url)
        response = requests.get(url)
        print("Response status:", response.status_code)
        print("Response text:", response.text[:500])
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print("--------------------------------")
        print("Looking for USD row...")
        usd_row = soup.find('td', text='USD').find_parent('tr')
        print("USD row found:", usd_row)
        
        print("--------------------------------")
        print("Looking for rate...")
        rate_cell = usd_row.find('td', {'data-label': 'Офіційний курс'})
        print("Rate cell found:", rate_cell)
        
        rate = float(rate_cell.text.replace(',', '.'))
        print("--------------------------------")
        print("Rate parsed:", rate)
        return rate
    except Exception as e:
        print("--------------------------------")
        print("Error getting USD rate:", str(e))
        print("--------------------------------")
        return 41