import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Using the Ticker module we can create an object that will allow us to access functions to extract data.
# To do this we need to provide the ticker symbol for the stock, here the company is Apple and the ticker symbol is AAPL.
apple = yf.Ticker("AAPL")
apple_info = apple.info
print('The country of Apple is: ', apple_info['country'])
apple_info['sector']

# Extracting Share Price
# Using the history() method we can get the share price of the stock over a certain period of time.
# Using the period parameter we can set how far back from the present to get data.
# The options for period are 1 day (1d), 5d, 1 month (1mo) , 3mo, 6mo, 1 year (1y), 2y, 5y, 10y, ytd, and max.
# The format that the data is returned in is a Pandas DataFrame
apple_share_price_data = apple.history(period="max")
print(apple_share_price_data.head())
# We can reset the index of the DataFrame with the reset_index function.
# We also set the inplace paramter to True so the change takes place to the DataFrame itself.
apple_share_price_data.reset_index(inplace=True)

# plot the Open price against the Date:
apple_share_price_data.plot(x="Date", y="Open")
plt.show()

# Extracting Dividends. The period of the data is given by the period defined in the 'history` function.
apple.dividends  # period is max
apple.dividends.plot()
plt.show()
