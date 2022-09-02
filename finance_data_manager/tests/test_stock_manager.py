from importlib import invalidate_caches
import pytest
from finance_data_manager import stock_manager
import pandas as pd
import yfinance as yf


@pytest.fixture
def working_yfinance_ticker():
	working_ticker_obj = yf.Ticker("AAPL")
	return working_ticker_obj

@pytest.fixture
def invalid_yfinance_ticker():
	invalid_ticker_obj = yf.Ticker("NOPE")
	return invalid_ticker_obj

@pytest.fixture
def all_tickers():
	all_tickers_set = stock_manager.all_tickers_set()
	return all_tickers_set


def test_all_tickers_set(all_tickers):
	"""Test that all tickers returns as a set and is not empty."""

	set_of_all_tickers = all_tickers
	assert set_of_all_tickers is not None
	assert type(set_of_all_tickers) is set
	assert len(set_of_all_tickers) > 0


def test_ticker_set_to_string(all_tickers):
	"""Test that set of tickers can be converted to string and is not empty."""

	set_string = stock_manager.ticker_set_to_string(all_tickers)
	assert type(set_string) is str
	assert set_string is not None
	assert len(set_string) > 0


@pytest.mark.parametrize(
	"input, is_none",
	(
		("AAPL", False),
		("DJIA", False),
		("NOPE", True),
		(-100, True),
		(["AAPL", "MSFT", "DJIA"], True),
		({"AAPL": 2, "MSFT": 3, "DJIA": False}, True),
	),
	ids=(
		"one ticker, exists",
		"one ticker, exists",
		"one ticker, does not exist",
		"bad data, does not exist",
		"list of tickers, list not supported",
		"list of tickers, dict not supported",
	),
)
def test_get_price(input, is_none):
	"""Ensure getting price returns correct object type"""

	result = stock_manager.get_price(input)

	assert result is None if is_none else result is not None

@pytest.mark.slow
def test_ticker_to_dict(working_yfinance_ticker, invalid_yfinance_ticker):
	"""Ensure converting yfinance ticker to dictionary return as accessibly dictionary and returns None if ticker is invalid."""

	assert stock_manager.ticker_to_dict(working_yfinance_ticker)['ticker'] == "AAPL"
	assert stock_manager.ticker_to_dict(invalid_yfinance_ticker) is None

@pytest.mark.slow
def test_histories_json(working_yfinance_ticker, invalid_yfinance_ticker):
	"""Ensure history json returns with data"""

	json_data = stock_manager.histories_json(working_yfinance_ticker)
	assert json_data is not None
	assert json_data[0]['label'] == 'all'

	broken_json_data = stock_manager.histories_json(invalid_yfinance_ticker)
	assert broken_json_data is None