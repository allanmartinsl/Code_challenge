# test_web_scraping.py

import pytest
import pandas as pd
import sqlite3

# Import the function to be tested
from code_challenge import web_scraping, storage

# Define a fixture to set up and tear down the database
@pytest.fixture
def setup_database():
    # Create an in-memory SQLite database for testing
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()

# Test web_scraping function
def test_web_scraping():
    # Test a valid currency code
    currency_code = 'BRLUSD'
    result_df = web_scraping(currency_code)
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty
    assert all(col in result_df.columns for col in ['ticker', 'Date', 'Open', 'High', 'Low', 'Close'])

    # Test an invalid currency code (should return an empty DataFrame)
    invalid_currency = 'INVALID'
    result_df = web_scraping(invalid_currency)
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.empty

# Test storage function
def test_storage(setup_database):
    # Assuming that currency_data DataFrame is not empty (you can create test data for currency_data if needed)
    currency_data = pd.DataFrame()
    currency_data['ticker'] = ['BRLUSD', 'EURUSD']
    currency_data['Date'] = ['2023-07-03', '2023-07-02']
    currency_data['Open'] = [0.2090, 1.0908]
    currency_data['High'] = [0.2102, 1.0931]
    currency_data['Low'] = [0.2086, 1.0872]
    currency_data['Close'] = [0.2090, 1.0908]

    # Store the test data in the in-memory database
    storage()

    # Connect to the in-memory database and retrieve the stored data
    conn = setup_database
    query = "SELECT * FROM currency_data"
    result_df = pd.read_sql_query(query, conn)

    # Verify if the data is correctly stored in the database
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty
    assert result_df.equals(currency_data)

# Run the tests with pytest
