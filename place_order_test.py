import json
import time
import hashlib
import requests
import hmac

from keyring.backends import null


def get_current_market_data():

    # api-endpoint
    get_currency_data_endpoint = "https://api.kuna.io/v3/tickers?symbols=btcuah"

    currency_data = requests.get(get_currency_data_endpoint).json()

    print("Bid price: " + str(currency_data[0][1]))
    print("Ask price: " + str(currency_data[0][3]))
    print("Change price 24h: " + str(currency_data[0][6]))
    print("Max 24h: " + str(currency_data[0][9]))
    print("Min 24h: " + str(currency_data[0][10]))

    return currency_data


def create_auth_headers(symbol, url):
    public_key = "uHM6vrJgni8QtNo9QIh944t5Pi2xPAH7fGvZLnr0"
    secret_key = "aNsPFSVGiJX8Ib0FGJ3OEgACFTTJxGLpuweV1Y8Y"

    # generating relevant parameters
    nonce = str(int(time.time()))
    request_body = json.loads('{"symbol": "btcuah", "type": "market", "amount": "0.00002"}')
    # generating HEX signature for the request
    signature_string = f"{url}{nonce}{json.dumps(request_body, separators=(',', ':'))}"
    signature_hex = hmac.new(bytes(secret_key, 'utf-8'), bytes(signature_string, 'utf-8'), digestmod=hashlib.sha384)

    # generating headers for the request
    order_headers = {'accept': 'application/json', 'content-type':'application/json', 'kun-nonce': nonce,
                     'kun-apikey': public_key, 'kun-signature': signature_hex.hexdigest()}

    return order_headers


def place_order_btcuah():
    fresh_data = get_current_market_data()

    # api-endpoint
    create_order_endpoint = "https://api.kuna.io/v3/auth/pro/w/order/submit"

    # generating relevant parameters
    order_headers = create_auth_headers('btcuah', "/v3/auth/pro/w/order/submit")
    request_body = json.loads('{"symbol": "btcuah", "type": "market", "amount": "0.000002"}')

    # performing the request itself
    order_response = requests.post(url=create_order_endpoint, headers=order_headers, data=request_body)

    # gathering response data
    print("Order status code: " + str(order_response.status_code))
    print("Order message: " + str(order_response.reason))

    if order_response.status_code == 200:
        print("Order response message: " + order_response.json())


if __name__ == '__main__':
    place_order_btcuah()
