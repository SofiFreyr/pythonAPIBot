import requests

from log_file_management import write_to_file, read_from_file
from order_management.create_order_data import create_order_data
from order_management.get_current_market_data import get_current_market_data


def place_order_generalized(symbol, order_type, amount):
    fresh_data = get_current_market_data()

    # api-endpoint
    create_order_endpoint = "https://api.kuna.io/v3/auth/w/order/submit"

    # generating relevant parameters
    order_data = create_order_data(symbol, order_type, "/v3/auth/w/order/submit", amount)
    order_headers = order_data[0]
    request_body = order_data[1]

    # performing the request itself
    order_response = requests.post(url=create_order_endpoint, headers=order_headers, json=request_body)

    # gathering response data
    print("Order status code: " + str(order_response.status_code))
    print("Order code reason: " + str(order_response.reason))
    print("Order message: " + str(order_response.text))

    if order_response.status_code == 200:
        print("Order response message: ", order_response.json())

    write_to_file(order_response, fresh_data)


if __name__ == '__main__':
    place_order_generalized("shibuah", "market", "-10")
    read_from_file()
