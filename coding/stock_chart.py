# filename: stock_chart.py

import yfinance as yf
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# download the stock price
nvda = yf.download('NVDA', start='2022-01-01')
tesla = yf.download('TSLA', start='2022-01-01')

# plot NVDA's stock price
plt.figure(figsize=(14, 7))
plt.plot(nvda.index, nvda.Close, label='NVDA', color='blue')

# plot Tesla's stock price
plt.plot(tesla.index, tesla.Close, label='TESLA', color='red')

plt.title('NVDA and TESLA price change YTD')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.grid()
plt.show()