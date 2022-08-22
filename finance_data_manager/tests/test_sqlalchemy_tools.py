from unittest import mock
from finance_data_manager import sqlalchemy_tools as sqla_tools
from finance_data_manager import stock_data as sd



def create_mock_stock_object():
	mock_stock_object = sd.Stock("TEST")
	mock_stock_object.business_summary = "Testing Inc. is the leading authority on testing for testing purposes."
	mock_stock_object.long_name = "Testing Inc."
	mock_stock_object.city = "Testering"
	mock_stock_object.state = "TS"
	mock_stock_object.country = "Testinistan"
	mock_stock_object.website = "https://www.testing.com/"
	mock_stock_object.logo_url = "https://www.testing.com/logo.png"
	mock_stock_object.industry = "Testing"
	mock_stock_object.currency_unit = "TSD"
	mock_stock_object.history_data_labels = "['1/1/2022', '1/2/2022', '1/3/2022', '1/4/2022', '1/5/2022']"
	mock_stock_object.history_data = "[1, 2, 3, 4, 5]"
	mock_stock_object.current_price = 1
	mock_stock_object.regular_market_price = 2
	mock_stock_object.regular_market_open = 3
	mock_stock_object.regular_market_day_high = 4
	mock_stock_object.regular_market_previous_close = 5
	mock_stock_object.pre_market_price = 6
	mock_stock_object.day_low = 7
	mock_stock_object.fifty_day_average = 8
	mock_stock_object.two_hundred_day_average = 9

	return mock_stock_object


def test_add_update_remove_stocks_to_database():
	mock_stock_object = create_mock_stock_object()

	sqla_tools.add_stock_to_database(mock_stock_object)
	sqla_tools.add_stock_to_database(mock_stock_object) # This should do nothing. Stock is already in database so adding flows to except then to pass.

	mock_stock_object.regular_market_price = mock_stock_object.regular_market_price * 2 # Change something with stock to update it in database.
	sqla_tools.update_stock_in_database(mock_stock_object)

	sqla_tools.remove_stock_from_database(mock_stock_object)

test_add_update_remove_stocks_to_database()
