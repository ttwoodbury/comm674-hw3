
# Load packages
import pandas.io.data as web
import datetime
import pandas as pd
import numpy as np
import random
from scipy.stats import pearsonr
from pandas.io.data import get_quote_yahoo, _yahoo_codes


def autocorr(x):
	autocorr = []

	for i in x.columns:
		data = x[i].dropna()
		corr, pval=pearsonr(data[:-1], data[1:])
		autocorr.append(corr)

	return autocorr

def rebalenced_returns(stocks, sample = 'd'):
  	rets = stocks.pct_change(freq = sample)
  	# return list(rets.mean(axis = 1)

def hold_returns(stocks, sample = 'd'):
		weights = (1/stocks.iloc[[0]]).T
		stocks = stocks.dot(weights)
		return list(stocks.pct_change(freq  = sample))


#returns should be a data frame
def summary_stats(returns):
	# how to calculate simple returns
	ret = returns.pct_change()

	#Example on how to compute the log returns for all the stocks in df
	d_lret2 = np.log(1+ret)
	d_lret = np.log(returns) - np.log(returns.shift())

	# #Calculate the autocorrelation
	autocorr_res = autocorr(ret)
	acres_ln = autocorr(d_lret)
	
	#mean
	ret_mean= ret.mean()
	lret_mean= d_lret.mean().values	
	#variance
	ret_var= ret.var()
	lret_var= d_lret.var().values
	#standard deviation
	ret_std = ret.std().values
	#skewness
	ret_skew= ret.skew().values

	d = {'mean': ret_mean, 'std': ret_std, 'autocorr': autocorr_res, 'lmn': lret_mean, 
	'lstd': d_lret.std(), 'lac': acres_ln, 'skew': ret_skew}

	return pd.DataFrame(d)


def main():

	start = datetime.datetime(2014, 1, 1)
	end = datetime.datetime(2014, 12, 31)

	#Load the csv file with the TSX Tickers
	tickers = pd.read_csv('TSX_Listing.csv')
	tickers = list(tickers['YAHOO_TICKER'])

	#companylist.csv is a list of the first 120 stocks from Google Finance with a
	#market cap under $100 million.  
	tick_lowcap = pd.read_csv('companylist.csv')
	tick_lowcap = list(tick_lowcap.Symbol)
	tick_lowcap = random.sample(tick_lowcap,30) #take 30 low cap stocks at random


	#Intiate the dictionnary that will store all the downloaded tick data
	df_tsx = pd.DataFrame()

	for tick in tickers:
	    f = web.DataReader(tick, 'yahoo', start, end)
	    df_tsx[tick] = f['Adj Close']

	# df_small = pd.DataFrame()

	# for tick in tick_lowcap:
	#  		f = web.DataReader(tick, 'yahoo', start, end)
	#  		df_small[tick] = f['Adj Close']

	out1 = summary_stats(df_tsx)
	#out2 = summary_stats(df_small)

	print hold_returns(df_tsx)
	print rebalenced_returns(df_tsx)
	# d_daily = {'tsx - buy/hold': hold_returns(df_tsx),'tst - rebalenced': rebalenced_returns(df_tsx)}
	
	# d_monthly = {'tsx - buy/hold': hold_returns(df_tsx, 'M'),'tst - rebalenced': rebalenced_returns(df_tsx, 'M')}

	# d_daily = {'small - buy/hold': hold_returns(df_small), 'tsx - buy/hold': hold_returns(df_tsx),
	# 	'small - rebalenced': rebalenced_returns(df_small), 'tst - rebalenced': rebalenced_returns(df_tsx)}
	
	# d_monthly = {'small - buy/hold': hold_returns(df_small, 'M'), 'tsx - buy/hold': hold_returns(df_tsx, 'M'),
	# 	'small - rebalenced': rebalenced_returns(df_small, 'M'), 'tst - rebalenced': rebalenced_returns(df_tsx, 'M')}

	# ss1 = out1.describe().drop('count',0) 
	# ss2 = pd.DataFrame(d_daily)
	
	# #ss3 = pd.DataFrame(d_monthly).describe().drop('count',0)

	# out1.to_csv('out1.csv')  # save your output
	# #out2.to_csv('out2.csv')
	# ss1.to_csv('ss1.csv')
	# ss2.to_csv('ss2.csv')
	# ss3.to_csv('ss3.csv')



if __name__ == "__main__":
	main()