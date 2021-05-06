# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:09:58 2021

@author: Babacan
"""
import numpy as np
import time
from datetime import datetime
import pandas as pd

from binance.client import Client
import requests

import matplotlib.pyplot as plt

FILENAME = 'credentials.txt'

    
class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """
    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)


if __name__ == '__main__':
    symbol = "BNBUSDT"
    interval = Client.KLINE_INTERVAL_15MINUTE
    
    connection = BinanceConnection(FILENAME)
    try :
        #interval: required e.g 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        klines = connection.client.get_historical_klines(symbol, interval, "15 day ago UTC")
        #klines = client.get_historical_klines(symbol, interval, "1 Dec, 2017", "1 Jan, 2018")  # start & end
        #klines = client.get_historical_klines(symbol, interval, "1 Jan, 2017")     #start
        
    except requests.exceptions.Timeout as e:
        print('Something went wrong. Error occured at %s. Wait for 1 min.' % (datetime.now()))
        print(e)
    
    open_time = [int(entry[0]) for entry in klines]
    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]

    open_date = pd.to_datetime(open_time, unit='ms')
    
    df = pd.DataFrame({'open':open, 'close':close, 'high':high, 'low':low, 'open_time':open_time})
    
    plt.plot(df['close'])
    plt.title("Price of" + str(symbol))
    plt.xlabel("Open Time")
    plt.ylabel("Value")
    plt.show()
    plt.savefig(str(symbol) + '.jpg')
    plt.close()
    
    df.to_excel("output.xlsx", sheet_name=symbol, index = False, header=True)
    

    
    