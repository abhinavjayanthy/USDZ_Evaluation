from helpers.DataManager import get_closing_info
from helpers.DataManager import get_percentage_difference
from modelGenerations.generateModel import generate_chart_model
from pxr import Usd, UsdUtils


if __name__ == '__main__':
    stage = Usd.Stage.CreateNew('assets/Final.usd')
    ticker_symbols = ['MSFT','AAPL','TSLA','GOOGL']

    for ticker_position in range(0,len(ticker_symbols)):
        dates, prices = get_closing_info(ticker_symbols[ticker_position])
        percentage_difference = get_percentage_difference(prices)
        percentage_difference = [0] + percentage_difference
        generate_chart_model(stage, ticker_position, ticker_symbols[ticker_position], prices[:20], percentage_difference[:20])

    stage.Save()
    UsdUtils.CreateNewARKitUsdzPackage('assets/Final.usd', 'assets/Final.usdz')
