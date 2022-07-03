from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, Numeric, String, \
	ForeignKey, UniqueConstraint, CheckConstraint, DateTime, Index
from datetime import datetime
from dotenv import load_dotenv
import os, sys

env_path = sys.path[1] + '/.env'
load_dotenv(env_path)

db_path = os.getenv("ENGINE_DB_PATH")

engine = create_engine(db_path)

metadata = MetaData(bind=engine)

connection = engine.connect()

users = Table('main_customuser', metadata, autoload=True)

stocks = Table('stocks', metadata,
			   Column('stock_id', Integer(), primary_key=True),
			   Column('stock_name', String(50), index=True),
			   Column('stock_symbol', String(5), unique=True),
			   )

portfolio = Table('portfolio', metadata,
				  Column('portfolio_id', Integer(), primary_key=True),
				  Column('user_id', ForeignKey('main_customuser.id'))
				  )

trades = Table('trades', metadata,
				Column('trade_id', Integer(), primary_key=True),
				Column('portfolio_id', ForeignKey('portfolio.portfolio_id')),
				Column('stock_id', ForeignKey('stocks.stock_id')),
				Column('quantity', Integer()),
				Column('price', Numeric(12, 2))
				)

metadata.create_all(engine)