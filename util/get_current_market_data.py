import requests


def get_current_market_data(market_symbols):
    # api-endpoint
    get_currency_data_endpoint = "https://api.kuna.io/v3/tickers?symbols="+market_symbols

    currency_data = requests.get(get_currency_data_endpoint).json()

    return currency_data
