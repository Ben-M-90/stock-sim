from sqlalchemy import MetaData
from sqlalchemy import insert
from sqlalchemy import Table, Column, Integer, Numeric, String, \
	ForeignKey, UniqueConstraint, CheckConstraint, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from stock_sim.settings import ENGINE as eng
from stock_sim.settings import SESSION as Session
from main.models import Stock, StockHistory

# Setup SQLAlchemy to connect to existing database created by Django ORM (e.g. Django migrations of models)
Base_Dec = declarative_base()
Base_Auto = automap_base()
Base_Auto.prepare(eng, reflect=True)

class StockData(Base_Dec): # SQLAlchemy connection to StockData table created in Django 'main' app
	__table__ = Table('main_stock', Base_Dec.metadata, autoload=True, autoload_with=eng)

class StockHistory(Base_Dec): # SQLAlchemy connection to StockHistory table created in Django 'main' app
	__table__ = Table('main_stockhistory', Base_Dec.metadata, autoload=True, autoload_with=eng)

def stock_obj_convert_django_to_sqlalchemy(django_stock_obj): # Probably don't need this. Django and Finance Data Manager should be decoupled.
	history_data_labels_string = "["
	history_data_string = "["

	for data_label in django_stock_obj.history_data_labels:
		history_data_labels_string += '"' + str(data_label) + '", '
	history_data_labels_string += "]"
	
	for data in django_stock_obj.history_data:
		history_data_string += '"' + str(data) + '", '
	history_data_string += "]"

	stock_values = {"ticker": django_stock_obj.ticker, 
				  "business_summary": django_stock_obj.business_summary,
				  "long_name": django_stock_obj.long_name,
				  "city": django_stock_obj.city,
				  "state": django_stock_obj.state,
				  "country": django_stock_obj.country,
				  "website": django_stock_obj.website,
				  "logo_url": django_stock_obj.logo_url,
				  "industry": django_stock_obj.industry,
				  "currency_unit": django_stock_obj.currency_unit,
				  "history_data_labels": history_data_labels_string,
				  "history_data": history_data_string,
				  "current_price": django_stock_obj.current_price,
				  "regular_market_price": django_stock_obj.regular_market_price,
				  "regular_market_open": django_stock_obj.regular_market_open,
				  "regular_market_day_high": django_stock_obj.regular_market_day_high,
				  "regular_market_previous_close": django_stock_obj.regular_market_previous_close,
				  "pre_market_price": django_stock_obj.pre_market_price,
				  "day_low": django_stock_obj.day_low,
				  "fifty_day_average": django_stock_obj.fifty_day_average,
				  "two_hundred_day_average": django_stock_obj.two_hundred_day_average,
				  }
	sqla_obj = Base_Auto.classes.main_stock(**stock_values)

	return sqla_obj, stock_values

def add_stock_to_database(stock_obj): # Need to redevelop without converting a django stock object to a sqlalchemy stock object.
	try:
		stock_to_add = stock_obj_convert_django_to_sqlalchemy()[0]
		session = Session()
		session.add(stock_to_add)
		session.commit()
	except:
		pass
		

def update_stock_in_database(stock_obj): # Need to redevelop without converting a django stock object to a sqlalchemy stock object.
	try:
		stock_values = stock_obj_convert_django_to_sqlalchemy()[1]
		session = Session()
		database_record = session.query(Base_Auto.classes.main_stock).filter_by(ticker = stock_obj.ticker)
		database_record.update(stock_values)
		session.commit()
	except:
		pass

def remove_stock_from_database(stock_obj):
	session = Session()

	Stock = Base_Auto.classes.main_stock

	try:
		stock_to_delete = session.query(Stock).filter_by(ticker = stock_obj.ticker).first()
		session.delete(stock_to_delete)
		session.commit()
	except:
		pass

def add_or_update_stock_to_database(stock_obj):
	try:
		add_stock_to_database(stock_obj)
	except:
		update_stock_in_database(stock_obj)
