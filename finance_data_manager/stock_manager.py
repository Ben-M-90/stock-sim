from cmath import nan
from lib2to3.pgen2.token import NAME
from re import I
from tkinter import Entry
import yfinance as yf
import pandas as pd
import sqlalchemy
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from stock_sim.settings import ENGINE as eng
from stock_sim.settings import SESSION as Session
import datetime
import pytz
import math

# Setup SQLAlchemy to connect to existing database created by Django ORM (e.g. Django migrations of models)
Base_Dec = declarative_base()
Base_Auto = automap_base()
Base_Auto.prepare(eng, reflect=True)

class StockDataTable(Base_Dec): # SQLAlchemy connection to StockData table created in Django 'main' app
	__table__ = sqlalchemy.Table('main_stock', Base_Dec.metadata, autoload=True, autoload_with=eng)

### Functions for gettings lists of tickers

def all_tickers_set(sp500=True, nasdaq=True, dow=True, other=True) -> set:
	'''
	Function to get a set of all stock tickers from S%P500, NASDAQ, DOW, and other using yahoo_fin library.
	Also removes tickers with certain stocks (e.g. bankruptcy filing, warrants, mutual funds, rights).
	Reformats ticker to a usable standard ("." to "-", "$" to "-P", remove extra hyphens).
	Returning as a set to ensure there are no duplicate tickers.
	'''
	from yahoo_fin import stock_info as si

	all_tickers = set()

	if sp500:
		sp500_set = set(symbol for symbol in pd.DataFrame(si.tickers_sp500())[0].values.tolist())
		all_tickers.update(sp500_set)
	if nasdaq:
		nasdaq_set = set(symbol for symbol in pd.DataFrame(si.tickers_nasdaq())[0].values.tolist())
		all_tickers.update(nasdaq_set)
	if dow:
		dow_set = set(symbol for symbol in pd.DataFrame(si.tickers_dow())[0].values.tolist())
		all_tickers.update(dow_set)
	if other:
		other_set = set(symbol for symbol in pd.DataFrame(si.tickers_other())[0].values.tolist())
		all_tickers.update(other_set)

	#all_tickers = set.union(sp500_set, nasdaq_set, dow_set, other_set)

	delinquent_char_list = ['W', 'R', 'P', 'Q']

	return_set = set()

	for symbol in all_tickers:
		if len(symbol) > 4 and symbol[-1] in delinquent_char_list:
			continue
		else:
			symbol = symbol.replace(".","-")
			symbol = symbol.replace("$","-P")
			symbol = symbol.split('-', 1)[0]
			symbol = symbol[0:4]
			return_set.add(symbol)

	print("Tickers in set - " + str(len(return_set)))
	return return_set

def stock_set_from_table():
	'''
	Get set of tickers out of existing Django database.
	'''
	session = Session()
	StockTable = Base_Auto.classes.main_stock
	stock_set = set()
	for stock in session.query(StockTable.ticker):
		stock_set.add(stock._data[0])
	return stock_set

def ticker_set_to_string(ticker_set):
	'''
	Converts set of tickers to space separated ticker string
	'''
	all_ticker_string = ""

	for ticker in ticker_set:
		all_ticker_string += " " + ticker

	if all_ticker_string[-1] == " ":
		all_ticker_string[-1].strip()

	return all_ticker_string	


## Functions for getting stock data

def get_data(stock_object):
		try:
			yf_stock = yf.Ticker(stock_object.ticker)
				
			stock_object.business_summary = yf_stock.info['longBusinessSummary']
			stock_object.long_name = yf_stock.info['longName']
			stock_object.city = yf_stock.info['city']
			stock_object.state = yf_stock.info['state']
			stock_object.country = yf_stock.info['country']
			stock_object.website = yf_stock.info['website']
			stock_object.logo_url = yf_stock.info['logo_url']
			stock_object.industry = yf_stock.info['industry']

			stock_object.currency_unit = yf_stock.info['financialCurrency']
			stock_object.current_price = yf_stock.info['currentPrice']
			stock_object.regular_market_price = yf_stock.info['regularMarketPrice']
			stock_object.regular_market_open = yf_stock.info['regularMarketOpen']
			stock_object.regular_market_day_high = yf_stock.info['regularMarketDayHigh']
			stock_object.regular_market_previous_close = yf_stock.info['regularMarketPreviousClose']
			stock_object.pre_market_price = yf_stock.info['preMarketPrice']
			stock_object.day_low = yf_stock.info['dayLow']
			stock_object.fifty_day_average = yf_stock.info['fiftyDayAverage']
			stock_object.two_hundred_day_average = yf_stock.info['twoHundredDayAverage']
		except:
			pass

def get_price(ticker):
	'''
	Get only regular market price of a single stock using yfinance.
	'''
	from yfinance import utils as yf_utils
	from yfinance import base

	ticker_url = "{}/{}".format(base._SCRAPE_URL_, ticker)

	try:
		regularMarketPrice = yf_utils.get_json(ticker_url).get('price', {}).get('regularMarketPrice')
		return regularMarketPrice
	except Exception:
		pass

def bulk_download_history_from_set(stock_set, 
						   period="1mo", 
						   interval="1d", 
						   group_by="ticker",
						   auto_adjust=True,
						   prepost=False,
						   threads=True,
						   proxy=None):
	ticker_string = ticker_set_to_string(stock_set)

	history_data = yf.download(ticker_string, 
					period=period, 
					interval=interval, 
					group_by=group_by, 
					auto_adjust=auto_adjust, 
					prepost=prepost, 
					threads=threads, 
					proxy=proxy)

	return history_data
	
def bulk_get_ticker_data_from_set(stock_set):
	ticker_string = ticker_set_to_string(stock_set)
	ticker_data = yf.Tickers(ticker_string)

	return ticker_data

def ticker_to_dict(ticker_data):
	if ticker_data.analysis is not None:
		info = ticker_data.info

		try:
			state = info["state"]
		except:
			state = "N/A"

		ticker_dict = {"ticker": info["symbol"],
					"long_name": info["longName"],
					"_business_summary": info["longBusinessSummary"],
					"_city": info["city"],
					"_state_location": state,
					"_country": info["country"],
					"website": info["website"],
					"logo_url": info["logo_url"],
					"_industry": info["industry"],
					"_currency_unit": info["financialCurrency"],
					"regular_market_price": info["regularMarketPrice"],
					"regular_market_open": info["regularMarketOpen"],
					"regular_market_day_high": info["regularMarketDayHigh"],
					"regular_market_previous_close": info["regularMarketPreviousClose"],
					"pre_market_price": info["preMarketPrice"],
					"day_low": info["dayLow"],
					"_fifty_day_average": info["fiftyDayAverage"],
					"_two_hundred_day_average": info["twoHundredDayAverage"],
					"history_data": histories_json(ticker_data)
					}
		return ticker_dict

def histories_json(ticker):
	history_dataframes = { 
	"all": ticker.history(period="max", interval="1wk"),
	"5 years": ticker.history(period="5y", interval="1wk"),
	"2 years": ticker.history(period="2y", interval="1wk"),
	"1 year": ticker.history(period="1y", interval="1wk"),
	"ytd": ticker.history(period="ytd", interval="1d"),
	"6 months": ticker.history(period="6mo", interval="1d"),
	"3 months": ticker.history(period="3mo", interval="1d"),
	"1 months": ticker.history(period="1mo", interval="1d"),
	"5 days": ticker.history(period="5d", interval="5m"),
	"1 day": ticker.history(period="1d", interval="1m")}

	data_object = []
	for dataframe in history_dataframes:
		compiled_list = []

		for index, row in history_dataframes[dataframe].iterrows():
			if (math.isnan(row['Open']) 
		  and math.isnan(row['High']) 
		  and math.isnan(row['Low']) 
		  and math.isnan(row['Close']) 
		  and math.isnan(row['Volume'])):
				continue

			if dataframe == "1 day" or dataframe == "5 days":
				compiled_list.append({
				"x": index.strftime("%m/%d/%Y %I:%M %p"),
				"o": row['Open'], 
				"h": row['High'], 
				"l": row['Low'], 
				"c": row['Close'], 
				"v": row['Volume']})
			else:
				compiled_list.append({
				"x": index.strftime("%m/%d/%Y"),
				"o": row['Open'], 
				"h": row['High'], 
				"l": row['Low'], 
				"c": row['Close'], 
				"v": row['Volume']})


			

		data_object.append({"label": dataframe, "data": compiled_list})

	return data_object