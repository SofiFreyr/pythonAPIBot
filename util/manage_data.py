import pandas as pd


def form_market_stats(relevant_symbols):
    with open('market_history.json', 'r', encoding='utf-8') as f:
        file_data = f.read()

    df = pd.DataFrame(pd.read_json(file_data))

    market_history_by_symbol = df.loc[df["Symbol"].isin(relevant_symbols.split(","))] \
        .groupby(["Symbol"])

    market_mean = market_history_by_symbol.mean()
    market_median = market_history_by_symbol.median()
    market_historic_max = market_history_by_symbol.max()
    market_historic_min = market_history_by_symbol.min()

    return [
        ["Market mean over time", market_mean],
        ["Market median over time", market_median],
        ["Market historic minimum", market_historic_max],
        ["Market historic maximum", market_historic_min]
    ]


if __name__ == '__main__':
    print(form_market_stats("eosuah")[1])
