from datetime import datetime
import time
import threading
from order_management.place_order import place_order_generalized
from util.get_current_market_data import get_current_market_data
from order_management.log_file_management import read_order_history, write_market_history_to_file
from util.manage_data import form_market_stats
from util.prepare_dataset import prepare_sell_dataset
from blessed import Terminal

# Blessings
term = Terminal()


def set_market_watcher():
    current_order_history = prepare_sell_dataset(read_order_history())
    while len(current_order_history) != 0:
        time.sleep(2)
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
        write_market_history_to_file(market_data)
        #relevant_market_watcher(market_data, symbol_count)
        print_market_stats(symbols)


def print_market_stats(symbols):
    market_stats = form_market_stats(symbols)

    for x in range(len(market_stats)):
        entry = market_stats[x]
        with term.location(0, 10 + x*9):
            print("___________________________________________________________________________________________________")
            print(entry[0] + ":" + "\n")
            print(entry[1])


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

                if new_bid - order_ask > order_ask / 50:
                    with term.location(int(term.width/2), 1):
                        print(term.move_xy(int(term.width/2), 1) +
                              f"Market: {symbol}, "
                              f"Old bid: {order_bid}, "
                              f"New bid: {new_bid}, "
                              f"Old ask: {order_ask}, "
                              f"New ask: {new_ask}. "
                              f"new ask > order_bid = SELL "
                              f"Difference:{(1 - order_ask / new_bid) * 100}% "
                              f"Profit approx:{((new_bid - order_ask) * (order_size_int * -1 * 0.9975)) * 0.9975} ")
                        place_order_generalized(symbol, "market", order_size_int * -1 * 0.9975)
                        closed_orders.append(x)
                else:
                    with term.location(0, 0):
                        print(term.move_xy(0, x) +
                              f"Market: {symbol}. Current margin {'{:.10f}'.format(new_bid - order_ask)}"
                              f" Required margin: {'{:.10f}'.format(order_ask / 50)}")

        with term.location(0, term.height - 4):
            print(term.move_xy(0, term.height - 3) + f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                  + f"---> Tick.  "
                  + f"Closed orders so far: {len(closed_orders)}  "
                  + f"Order pool size: {len(current_order_history)}")

        time.sleep(30)


def relevant_market_watcher(market_data, symbol_count):
    with term.location(0, int(term.height / 2) - 1):
        print(term.move_xy(0, int(term.height / 2) - 2) +
              f"Market Watcher Data ({symbol_count} relevant markets)")
        print(term.move_xy(0, int(term.height / 2) - 1) +
              f"------------------------------------------------------------------------")

    for x in range(symbol_count):
        i = market_data[x]
        with term.location(0, int(term.height / 2) + x):
            print(f"Symbol: {i[0]}. Current Bid: {i[1]}. Current Ask: {i[3]}. 24h change: {i[6]}")
    with term.location(0, int(term.height / 2) + symbol_count + 1):
        print(f"------------------------------------------------------------------------")


if __name__ == '__main__':
    print(term.clear)

    class SellWatcher(threading.Thread):
        def run(self):
            sell_watcher()


    class SellTrendWatcher(threading.Thread):
        def run(self):
            set_market_watcher()


    app1 = SellWatcher()
    app2 = SellTrendWatcher()
    app1.start()
    app2.start()
