import json
import os


def write_to_file(order_response, currency_data):
    open('order_history.json', 'a+').close()

    response_json = order_response.json()
    data = {
        "Order_code": order_response.status_code,
        "Order_code_reason": order_response.reason,
        "Order_ID": response_json[0],
        "Order_market": response_json[3],
        "Order_market_bid": currency_data[0][1],
        "Order_market_ask": currency_data[0][3],
        "Order_size_original": response_json[6],
        "Order_size": response_json[7],
        "Order_type": response_json[8],
        "Order_status": response_json[13],
        "Order_price": response_json[16],
        "Order_stop_loss": response_json[19]
    }

    data_json = 'order_history.json'
    if os.path.getsize(data_json) <= 0:
        with open(data_json, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(data_json, 'r', encoding='utf-8') as f:
        file_data = json.load(f)

    file_data.append(data)

    with open(data_json, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, ensure_ascii=False, indent=4)


def read_order_history():
    with open('order_management/order_history.json', 'r', encoding='utf-8') as f:
        file_data = f.read()

    json_data = json.loads(file_data)

    return json_data