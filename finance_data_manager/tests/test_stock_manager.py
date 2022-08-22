import pytest
from finance_data_manager import stock_manager
from time import sleep
import datetime
import pandas as pd
import yfinance as yf

def test_get_price():
	success_ticker = "AAPL"
	assert stock_manager.get_price("AAPL") is not None

	broken_ticker = "NOPE"
	assert stock_manager.get_price("NOPE") is None

def test_get_price_loop():
	ticker = "AAPL"
	for i in range(20):
		current_price = stock_manager.get_price(ticker)
		time_stamp = datetime.datetime.now()
		print(time_stamp.strftime("%H:%M:%S") + ": " + str(current_price))

def test_stock_set_from_table():
	stocks = stock_manager.stock_set_from_table()
	print(stocks)

def test_bulk_download_history_from_set():
	stock_set = stock_manager.all_tickers_set(other=False)
	stock_manager.bulk_download_from_set(stock_set)

def test_bulk_get_ticker_data_from_set():
	stock_set = set()
	stock_set.add("AAPL")
	stock_set.add("MSFT")
	stock_set.add("F")
	stock_set.add("TEST")

	ticker_data = stock_manager.bulk_get_ticker_data_from_set(stock_set)

	return ticker_data

def test_ticker_to_dict():
	ticker_set = set()
	ticker_set.add("AAPL")
	ticker_set.add("MSFT")
	ticker_set.add("F")
	ticker_set.add("TM")
	ticker_set.add("TEST")
	ticker_data = stock_manager.bulk_get_ticker_data_from_set(ticker_set)
	tickers_dict_list = []

	start_time = datetime.datetime.now()
	last_time = start_time
	print("Start: " + start_time.strftime("%H:%M:%S"))
	for symbol in ticker_data.symbols:
		dict_to_append = stock_manager.ticker_to_dict(ticker_data.tickers[symbol])
		if dict_to_append is not None:
			tickers_dict_list.append(stock_manager.ticker_to_dict(ticker_data.tickers[symbol]))
		time_delta = datetime.datetime.now() - last_time
		last_time = datetime.datetime.now()
		print(time_delta)


def test_histories_json():
	yfticker = yf.Ticker("GME")
	stock_manager.histories_json_clean(yfticker)

#test_get_price()
#test_get_price_loop()
test_ticker_to_dict()
test_histories_json()