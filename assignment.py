import pandas.io.data as web
import datetime
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

#Try compounding the biased returns 


# Choose your starting and ending time
start = datetime.datetime(2014, 1, 1)  #(YYYY, m, d)
end = datetime.datetime(2014, 12, 31)

# Load the csv file with the TSX Tickers, this code assume that the ticker files
# located in the same folder as the directory
tickers = pd.read_csv('TSX_Listing.csv')
tickers = list(tickers['YAHOO_TICKER'])

# Intiate the dictionnary that will store all the downloaded tick data
d = pd.DataFrame()

# Options for web.DataReader function:
"""
input 1: ticker in string form - Ex: OSPTX is for the S&P/TSX
input 2: the source (ex: 'yahoo' or 'google') to download the data from
input 3: start time in datatime.datetime format
input 4: end time in datatime.datetime format
"""
# Loop over each tickers to load the data to be stored in the dictionnary d
for tick in tickers:
    f = web.DataReader(tick, 'yahoo', start, end)
    d[tick] = f['Adj Close']  # select the adjusted close price

# how to calculate simple returns
ret = d.pct_change()
# Example on how to compute the log returns for all the stocks in d
d_lret = np.log(d) - np.log(d.shift())

print d_lret.head()
# export the return data to csv file
#d_lret.to_csv ('TSX_data2014.csv')