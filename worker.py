from datetime import datetime
import time
import threading
from order_management.place_order import place_order_generalized
from util.get_current_market_data import get_current_market_data
from order_management.log_file_management import read_order_history, write_market_history_to_file
from util.prepare_dataset import prepare_sell_dataset


def sell_watcher():
    current_order_history = prepare_sell_dataset(read_order_history())
    closed_orders = []
    while len(closed_orders) < len(current_order_history):
        # iterating over orders to look if there's any profit to be had
        for x in range(len(current_order_history)):
            if closed_orders.count(x) == 0:
                i = current_order_history[x]
                symbol = i['Order_market']
                current_tick = get_current_market_data(symbol)
                order_bid = i['Order_market_bid']
                order_ask = i['Order_market_ask']
                new_bid = current_tick[0][1]
                new_ask = current_tick[0][3]
                order_size_int = float(i['Order_size_original'])

                if new_ask > order_bid and new_bid-order_ask > order_ask/25:
                    print(f"Market: {symbol}, "
                          f"Old bid: {order_bid}, "
                          f"New bid: {new_bid}, "
                          f"Old ask: {order_ask}, "
                          f"New ask: {new_ask}. "
                          f"new ask > order_bid = SELL "
                          f"Difference:{(1 - order_ask/new_bid)*100}% ")
                    place_order_generalized(symbol, "market", order_size_int * -1 * 0.9975)
                    closed_orders.append(x)

        tick_time = datetime.now().strftime('%d/%m/%Y %H:%M')
        print(f"{tick_time} -> Tick. " +
              f"Closed orders so far: {len(closed_orders)}" +
              f"  Order pool size: {len(current_order_history)}")
        time.sleep(60)


def relevant_market_watcher():
    done = 1
    while done:
        time.sleep(180)
        current_order_history = prepare_sell_dataset(read_order_history())
        symbol_count = 0
        symbols = ""

        for x in range(len(current_order_history)):
            i = current_order_history[x]['Order_market']
            if symbols.find(i) == -1:
                symbol_count = symbol_count + 1
                if len(symbols) == 0:
                    symbols = f"{i}"
                else:
                    symbols = symbols + f",{i}"

        market_data = get_current_market_data(symbols)

        print(f"Market Watcher Data ({symbol_count} relevant markets)")

        for x in range(len(market_data)):
            i = market_data[x]
            print(f"Symbol: {i[0]}. Current Bid: {i[1]}. Current Ask: {i[3]}. 24h change: {i[6]}")

        write_market_history_to_file(market_data)


if __name__ == '__main__':

    class SellWatcher(threading.Thread):
        def run(self):
            sell_watcher()

    class SellTrendWatcher(threading.Thread):
        def run(self):
            relevant_market_watcher()


    app1 = SellWatcher()
    app2 = SellTrendWatcher()
    app1.start()
    app2.start()
