from datetime import date

import yfinance as yf
import matplotlib.pyplot as plt
import seaborn


class StockData():
    def __init__(self, stock_ticker):
        stock = yf.Ticker(stock_ticker)
        start_date = input(' From Date of format 2021-01-01: ')
        end_date = input(' To Date of format 2021-01-01: ')
        today = date.today()
        print(today)
        hist = stock.history(start = start_date, end=end_date)


        # Plot
        hist['Close'].plot(figsize=(16, 9))
        plt.show()

