import requests


def get_general_data():
    # api-endpoint
    all_currencies = "https://api.kuna.io/v3/currencies"
    all_markets = "https://api.kuna.io/v3/markets"

    # sending get request and saving the response as response object
    cur = requests.get(url=all_currencies)
    mar = requests.get(url=all_markets)

    # extracting data in json format if the response is 200
    if cur.status_code == 200:
        data_cur = cur.json()

        print(data_cur)

        for id in data_cur:
            print("Name: " + id['name'] + "       Code: " + id['code'])

    if mar.status_code == 200:
        data_mar = mar.json()

        print(data_mar)

        for id in data_mar:
            if id['id'].__contains__("uah"):
                print("ID: " + id['id'] + "       24h change: " + str(id['price_change']))

