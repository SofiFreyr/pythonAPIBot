def prepare_sell_dataset(raw_history):
    bought_orders = []
    for x in range(len(raw_history)):
        i = raw_history[x]
        if float(i['Order_size_original']) > 0:
            bought_orders.append(i)

    return bought_orders


def prepare_sell_history(raw_history):
    sell_history = []
    for x in range(len(raw_history)):
        i = raw_history[x]
        if float(i['Order_size_original']) < 0:
            sell_history.append(i)

    return sell_history
