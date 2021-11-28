import requests

from order_management.log_file_management import write_to_file
from order_management.create_request_headers import create_request_headers
from util.get_current_market_data import get_current_market_data


def place_order_generalized(symbol, order_type, amount):
    fresh_data = get_current_market_data(symbol)

    # api-endpoint
    create_order_endpoint = "https://api.kuna.io/v3/auth/w/order/submit"

    # generating relevant parameters
    request_body = {
        "symbol": symbol,
        "type": order_type,
        "amount": amount,
        "price": int(fresh_data[0][3])
    }
    order_headers = create_request_headers("/v3/auth/w/order/submit", request_body)

    # performing the request itself
    order_response = requests.post(url=create_order_endpoint, headers=order_headers, json=request_body)

    # gathering response data
    # print("Order status code: " + str(order_response.status_code))
    # print("Order code reason: " + str(order_response.reason))
    # print("Order message: " + str(order_response.text))

    # if order_response.status_code == 200:
    #     print("Order response message: ", order_response.json())

    write_to_file(order_response, fresh_data)

if __name__ == '__main__':
    place_order_generalized("shibuah", "market", "-5000")
