import requests
import time
import numpy as np
import pandas as pd


def get_products():
    api_url = 'https://api.pro.coinbase.com/products'
    results = requests.get(api_url).json()
    df = pd.json_normalize(results)
    df = df[df.quote_currency == 'USD']
    df = df[df.fx_stablecoin != True]
    tickers = list(df['id'])
    tickers.sort()
    return tickers


def get_market_data(product_id, granularity, start_time, end_time, variable):
    api_url = 'https://api.exchange.coinbase.com/products/' + product_id + '/candles'
    request_headers = {
        'granularity': str(granularity),
        'start': str(start_time),
        'end': str(end_time)
    }
    results = requests.get(api_url, headers=request_headers).json()
    df = pd.DataFrame(results, columns=['time', 'open', 'high', 'low', product_id + ' ' + 'close', 'volume'])
    price_lst = list(df[product_id + ' ' + 'close'])
    time_lst = list(df['time'])
    if variable:
        return price_lst
    else:
        return time_lst


def get_all_price(granularity, start_time, end_time):
    df = []
    tickers = get_products()
    df.append(get_market_data(tickers[0], granularity, start_time, end_time, False))
    for i in tickers:
        df.append(get_market_data(i, granularity, start_time, end_time, True))
    df = pd.DataFrame(np.array(df)).T
    tickers.insert(0, 'time')
    df.set_axis(tickers, axis=1, inplace=True)
    print(df)
    return df


# Tim to Finish
def get_index_price(granularity, start_time, end_time):
    df = get_all_price(granularity, start_time, end_time)
    # [...]
    return df


get_index_price(60, int(time.time()), '')
