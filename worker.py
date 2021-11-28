import json
from datetime import datetime
import time
from order_management.place_order import place_order_generalized
from util.get_current_market_data import get_current_market_data
from order_management.log_file_management import read_order_history


def worker():
    current_order_history = read_order_history()
    closed_orders = []
    while 1:

        for x in range(len(current_order_history)):
            i = current_order_history[x]
            symbol = i['Order_market']
            current_tick = get_current_market_data(symbol)
            order_bid = i['Order_market_bid']
            order_ask = i['Order_market_ask']
            new_bid = current_tick[0][1]
            new_ask = current_tick[0][3]
            order_size_int = float(i['Order_size_original'])

            if order_size_int < 0 and new_bid > order_ask and new_bid-order_ask > new_bid/50:
                print(f"Market: {symbol}, "
                      f"Old bid: {order_bid}, "
                      f"New bid: {new_bid}, "
                      f"Old ask: {order_ask}, "
                      f"New ask: {new_ask}, "
                      f"new bid > order_ask = BUY")
                place_order_generalized(symbol, "market", order_size_int * -1)
                current_order_history = current_order_history.pop(x)
                closed_orders.append(x)
            elif order_size_int > 0 and new_ask > order_bid and new_ask-order_bid > new_bid/50:
                print(f"Market: {symbol}, "
                      f"Old bid: {order_bid}, "
                      f"New bid: {new_bid}, "
                      f"Old ask: {order_ask}, "
                      f"New ask: {new_ask}. "
                      f"new ask > order_bid = SELL")
                place_order_generalized(symbol, "market", order_size_int * -1)
                current_order_history = current_order_history.pop(x)
                closed_orders.append(x)

        tick_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        print(f"{tick_time} -> Tick. " + f"Closed orders so far: {len(closed_orders)}")
        time.sleep(10)

if __name__ == '__main__':
    worker()
