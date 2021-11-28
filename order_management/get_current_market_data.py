import requests


def get_current_market_data():
    # api-endpoint
    get_currency_data_endpoint = "https://api.kuna.io/v3/tickers?symbols=btcuah"

    currency_data = requests.get(get_currency_data_endpoint).json()

    #print("Bid price: " + str(currency_data[0][1]))
    #print("Ask price: " + str(currency_data[0][3]))
    #print("Change price 24h: " + str(currency_data[0][6]))
    #print("Max 24h: " + str(currency_data[0][9]))
    #print("Min 24h: " + str(currency_data[0][10]))

    return currency_data