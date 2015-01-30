# -*- coding: utf-8 -*-
"""
Assignment 1 Solution: Python code for grabbing data from Yahoo!Finance

Last updated: 1/7/2015

@author: CM, JS

Note: This code guides you to grab Canadian stock returns data from Yahoo!Finance.
The purpose of this assignment is to get you familiar with the Python. Enjoy! 

# Reference: http://pandas.pydata.org/pandas-docs/stable/remote_data.html
# Source file https://github.com/pydata/pandas/blob/master/pandas/io/data.py

"""
# -*- coding: utf-8 -*-

# Load packages
import pandas.io.data as web
import datetime
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

#directory = 'C:\\Users\\Adlai Fisher\\Desktop\\work\\week1\\Assignment1'
directory = 'G:\\Dropbox\\Fisher Martineau\\Week3_674\\python\\Sample code A2'

#Choose your starting and ending time
start = datetime.datetime(2014, 1, 1)
end = datetime.datetime(2014, 12, 31)

#Load the csv file with the TSX Tickers
tickers0 = pd.read_csv(directory + '\\' + 'TSX_Listing.csv')
tickers = list(tickers0['YAHOO_TICKER'])

#Intiate the dictionnary that will store all the downloaded tick data
df = pd.DataFrame()

# Options for web.DataReader function:
"""
input 1: ticker in string form - Ex: OSPTX is for the S&P/TSX
input 2: the source (ex: 'yahoo' or 'google') to download the data from
input 3: start time in datatime.datetime format
input 4: end time in datatime.datetime format
"""

for tick in tickers:
    f = web.DataReader(tick, 'yahoo', start, end)
    df[tick] = f['Adj Close']  # select the adjusted close price column

# how to calculate simple returns
ret = df.pct_change()

#Example on how to compute the log returns for all the stocks in df
d_lret2 = np.log(1+ret)
d_lret = np.log(df) - np.log(df.shift())

#mean
ret_mean=ret.mean()
lret_mean=d_lret.mean()
#variance
ret_var=ret.var()
lret_var=d_lret.var()
#standard deviation
ret_std = pd.DataFrame(ret.std())
#skewness
ret_skew=ret.skew()

#Calculate the autocorrelation
autocorr_res = []
acres_ln =[]
for i in ret.columns:
    data0 = ret[i]
    data = data0.dropna()
    corr, pval=pearsonr(data[:-1], data[1:])
    autocorr_res.append(corr)
    data1 = d_lret[i]
    data = data1.dropna()
    corr, pval=pearsonr(data[:-1], data[1:])
    acres_ln.append(corr)

out1 = pd.DataFrame(ret_mean)
out2 = out1.rename(columns={0: 'mean'})
out3 = out2.join(ret_std)
out4 = out3.rename(columns={0: 'std'})
out4['autocorr'] = autocorr_res
out4['lmn']=lret_mean.values
out4['lstd']=d_lret.std().values
out4['lac']=acres_ln
out4['skew'] = ret_skew.values


"""Apply the describe function to get the cross-sectional averages, 
St.d., min and max, and the percentiles"""

ss1 = out4.describe()
ss1 = ss1.drop('count',0)  # remove the row called count coming from describe()

out4.to_csv(directory+'\\out4.csv')  # save your output
ss1.to_csv(directory+'\\ss1.csv')
