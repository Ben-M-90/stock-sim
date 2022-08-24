from ast import Set, Str
import pytest
from finance_data_manager import stock_manager
from time import sleep
import datetime
import pandas as pd
import yfinance as yf
import json

def test_all_tickers_set():
	all_tickers_set = stock_manager.all_tickers_set()
	assert all_tickers_set is not None
	assert type(all_tickers_set) is set
	assert len(all_tickers_set) > 0

def test_ticker_set_to_string():
	set_string = stock_manager.ticker_set_to_string(stock_manager.all_tickers_set())
	assert type(set_string) is str
	assert set_string is not None
	assert len(set_string) > 0

def test_get_price():
	assert stock_manager.get_price("AAPL") is not None

	assert stock_manager.get_price("DJIA") is not None
	assert stock_manager.get_price("NOPE") is None
	assert stock_manager.get_price(-100) is None
	assert stock_manager.get_price(["AAPL", "MSFT", "DJIA"]) is None
	assert stock_manager.get_price({"AAPL": 2, "MSFT": 3, "DJIA": False}) is None

def test_ticker_to_dict():
	assert stock_manager.ticker_to_dict(yf.Ticker("AAPL"))['ticker'] == "AAPL"
	assert stock_manager.ticker_to_dict(yf.Ticker("NOPE")) is None

def test_histories_json():
	json_data = stock_manager.histories_json(yf.Ticker("GME"))
	assert json_data is not None
	assert json_data[0]['label'] == 'all'