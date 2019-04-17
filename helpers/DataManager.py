

# let url = "https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?fileType=csv&fileName=" + ticker + "_holdings&dataType=fund"

# let url = "https://ts-api.cnbc.com/harmony/app/bars/" + ticker + "/30M/20181113000000/20190215000000/adjusted/EST5EDT.json"


import requests

import config


def get_closing_info(ticker):
    URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=compact&apikey=' + config.API_KEY + 'datatype=json'
    response = requests.get(URL)
    if response.status_code != 200:
        raise Exception('Somethine went wrong {}'.format(response.status_code))
    result = response.json()
    time_series = result['Time Series (Daily)']
    dates, closing_values = parse((time_series))
    return dates, closing_values


def parse(time_series):
    closing_values = []
    dates = []
    for key, value in time_series.iteritems():
        closing_values.append(float(value['4. close']) / 5)
        dates.append(key)
    return dates, closing_values


def get_percentage_difference(prices):
    percentage_difference = [100 * (b - a) / a for a, b in zip(prices[::1], prices[1::1])]
    return percentage_difference
