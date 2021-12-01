import json
import os
import time


def write_order_to_file(order_response, currency_data):
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


def write_market_history_to_file(market_history):
    open('market_history.json', 'a+').close()

    data_json = 'market_history.json'
    if os.path.getsize(data_json) <= 0:
        with open(data_json, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
            f.close()

    with open(data_json, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
        f.close()

    for x in range(len(market_history)):
        market = market_history[x]
        file_data.append({
            "Log_time": time.time(),
            "Symbol": market[0],
            "Current_bid": market[1],
            "Current_ask": market[3],
            "24h_change": market[6],
        })

    with open(data_json, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, ensure_ascii=False, indent=4)
        f.close()


def read_order_history():
    with open('order_management/order_history.json', 'r', encoding='utf-8') as f:
        file_data = f.read()

    json_data = json.loads(file_data)

    return json_data
