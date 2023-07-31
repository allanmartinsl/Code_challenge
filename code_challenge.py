import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sqlite3

# Configure the logging settings
logging.basicConfig(filename='web_scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def web_scraping(currency):
    """
    Scrapes historical currency data from Yahoo Finance for a given currency code.

    Args:
        currency (str): The currency code to scrape data for.

    Returns:
        pd.DataFrame: DataFrame containing the historical currency data.
    """
    logging.info(f"Scraping data for currency: {currency}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = f'https://finance.yahoo.com/quote/{currency}%3DX/history'
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, "html.parser")

        # Use BeautifulSoup to find and extract the currency prices from the HTML
        table = soup.find('table', {'data-test': 'historical-prices'})

        # Process the extracted data and return it
        # Extract table headers (Data, Open, High, Low, Close, Adj Close, and Volume)
        headers = table.find_all('th')
        columns = [header.text for header in headers]

        # Extract table rows (each row represents a trading day)
        data_rows = table.find_all('tr')

        # Create a list to store the data from each row
        data = []
        for row in data_rows:
            row_data = row.find_all('td')
            data.append([cell.text for cell in row_data])

        # Transform the data into a pandas DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Add a new column 'ticker' with the value of the variable 'currency' to the DataFrame
        df.insert(0, 'ticker', currency)

        # Remove the 'Volume' and 'Close' columns
        df.drop(columns=['Volume', 'Close*'], inplace=True)
        
        # Rename the 'Adj Close' column to 'Close'
        df.rename(columns={'Adj Close**': 'Close'}, inplace=True)

        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Error while fetching data for currency {currency}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error

currencies = ['BRLUSD', 'EURUSD', 'CHFUSD', 'EURCHF']
currency_data = pd.DataFrame()

for item in currencies:
    # Assuming that the 'web_scraping(item)' function returns a DataFrame with the currency data
    currency_df = web_scraping(item)

    if not currency_df.empty:
        currency_data = pd.concat([currency_data, currency_df])
    else:
        logging.warning(f"Currency data for {item} is empty.")

def storage():
    """
    Stores the scraped currency data into a SQLite database.
    """
    # Define the SQLite database filename
    db_filename = 'currency_data.db'

    # Connect to the SQLite database
    conn = sqlite3.connect(db_filename)

    # Convert the DataFrame to a SQL table
    currency_data.to_sql('currency_data', conn, if_exists='replace', index=False)

    # Close the connection to the SQLite database
    conn.close()

storage()