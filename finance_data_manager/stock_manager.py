from types import NoneType
import pandas as pd
import math

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

	return return_set

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

def get_price(ticker):
	'''
	Get only regular market price of a single stock using yfinance.
	'''
	from yfinance import utils as yf_utils
	from yfinance import base

	ticker_url = "{}/{}".format(base._SCRAPE_URL_, ticker)

	regularMarketPrice = yf_utils.get_json(ticker_url).get('price', {}).get('regularMarketPrice')
	return regularMarketPrice

def ticker_to_dict(yfinance_ticker):
	'''
	Convert yfinance ticker to dictionary of data.
	'''
	if yfinance_ticker.analysis is not None:
		info = yfinance_ticker.info

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
					"history_data": histories_json(yfinance_ticker)
					}

		if type(ticker_dict) == NoneType:
			return None
		return ticker_dict

def histories_json(ticker):
	'''
	Return Json serialized history data for given yfinance ticker.
	'''
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