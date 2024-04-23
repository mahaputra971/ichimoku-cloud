from pandas_datareader import data as pdr
import yfinance as yf
import time
import datetime

import matplotlib.pyplot as plt
import pandas_datareader.data as wb 

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

yf.pdr_override()

issuer_stock_codes = ['ADRO.JK', 'AKRA.JK', 'BBRM.JK', 'BYAN.JK', 'DEWA.JK', 'DOID.JK', 'DSSA.JK', 'ELSA.JK', 'GEMS.JK', 'GTSI.JK', 'HITS.JK', 'HRUM.JK', 'INDY.JK', 'ITMG.JK', 'JSKY.JK', 'KKGI.JK', 'LEAD.JK', 'MBSS.JK', 'MCOL.JK', 'MEDC.JK', 'MYOH.JK', 'PGAS.JK', 'PSSI.JK', 'PTBA.JK', 'PTIS.JK', 'PTRO.JK', 'RAJA.JK', 'RMKE.JK', 'SHIP.JK', 'SOCI.JK', 'TEBE.JK', 'TOBA.JK', 'UNIQ.JK', 'WINS.JK', 'ADMR.JK', 'AIMS.JK', 'APEX.JK', 'ARII.JK', 'ARTI.JK', 'BESS.JK', 'BIPI.JK', 'BOSS.JK', 'BSML.JK', 'BSSR.JK', 'BULL.JK', 'BUMI.JK', 'CANI.JK', 'CNKO.JK', 'DWGL.JK', 'ENRG.JK', 'ETWA.JK', 'FIRE.JK', 'GTBO.JK', 'IATA.JK', 'INPS.JK', 'ITMA.JK', 'KOPI.JK', 'MBAP.JK', 'MITI.JK', 'MTFN.JK', 'PKPK.JK', 'RIGS.JK', 'RUIS.JK']

for assets in issuer_stock_codes:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=5*365)
    data = pdr.get_data_yahoo(assets, start=start_date, end=end_date.strftime("%Y-%m-%d"))
    # df = pdr.get_data_yahoo(assets, start=start_date, end=end_date.strftime("%Y-%m-%d")) 
    # Create a new dataframe with only the 'Close column 
    # dataf = df.filter(['Close'])
    # # Convert the dataframe to a numpy array
    # dataset = dataf.values

    
    high9 = data.High.rolling(9).max() 
    Low9 = data.High.rolling(9).min()   
    high26 = data.High.rolling(26).max()
    Low26 = data.High.rolling(26).min()
    high52 = data.High.rolling(52).max()
    Low52 = data.High.rolling(52).min()
    
    data['tenkan_sen'] = (high9 + Low9) / 2
    data['kijun_sen'] = (high26 + Low26) / 2
    data['senkou_span_a'] = ((data['tenkan_sen'] + data['kijun_sen']) / 2).shift(26) 
    data['senkou_span_b'] = ((high52 + Low52) / 2).shift(26)
    data['chikou'] = data.Close.shift(-26)
    data = data.iloc[26:]

    plt.figure(figsize=(16,6))
    plt.plot(data.index, data['tenkan_sen'], lw=0.7, color='purple')
    plt.plot(data.index, data['kijun_sen'], lw=0.7, color='yellow')
    plt.plot(data.index, data['chikou'], lw=0.7, color='grey')
    plt.plot(data.index, data['Close'], lw=0.7, color='blue')
    plt.title("Ichimoku Saham : " + str(assets))
    plt.ylabel("Harga")
    kumo = data['Adj Close'].plot(lw=0.7, color='red')
    kumo.fill_between(data.index, data.senkou_span_a, data.senkou_span_b, where= data.senkou_span_a >= data.senkou_span_b, color='lightgreen')
    kumo.fill_between(data.index, data.senkou_span_a, data.senkou_span_b, where= data.senkou_span_a < data.senkou_span_b, color='lightcoral')
    plt.grid()  
    plt.savefig(f'plot_{assets}.png')
    plt.clf()  # Clear the current figure to start a new plot for the next asset

    print ("\nKode Emiten : ", assets)
    print("Close Price:", data['Close'].iloc[-1])
    print("tenkan_sen:", data['tenkan_sen'].iloc[-1])
    print("kijun_sen:", data['kijun_sen'].iloc[-1])
    print("senkou_span_a:", data['senkou_span_a'].iloc[-1])
    print("senkou_span_b:", data['senkou_span_b'].iloc[-1])
    # print("chikou:", data['chikou'].iloc[-1])
    # Get the last price and the previous price
    
    # Get the last price and the previous price
    # last_price = data['Close'].iloc[-1]
    # prev_price = data['Close'].iloc[-2]

    # # Get the last Kumo cloud components
    # last_senkou_span_a = data['senkou_span_a'].iloc[-1]
    # last_senkou_span_b = data['senkou_span_b'].iloc[-1]

    # # Get the last Kijun-Sen and Tenkan-Sen
    # last_kijun_sen = data['kijun_sen'].iloc[-1]
    # last_tenkan_sen = data['tenkan_sen'].iloc[-1]

    ######################################## SEKAN_SEN FACTOR
    # Prepare data for linear regression
    tenkan_sen = data['tenkan_sen']
    x = np.array(range(len(tenkan_sen))).reshape(-1, 1)
    y = tenkan_sen.values.reshape(-1, 1)

    # Perform linear regression
    model = LinearRegression()
    model.fit(x, y)

    # Get the slope of the line
    slope = model.coef_[0]

    # Determine the trend
    if slope > 0:
        print("The Tenkan-Sen is in an uptrend.")
    elif slope < 0:
        print("The Tenkan-Sen is in a downtrend.")
    else:
        print("The Tenkan-Sen is moving sideways.")
        
    ######################################## KIJUN_SEN FACTOR
    # Get the last closing price and the last Kijun-Sen value
    last_close = data['Close'].iloc[-1]
    last_kijun_sen = data['kijun_sen'].iloc[-1]

    # Determine the trend based on the position of the closing price relative to the Kijun-Sen line
    if last_close > last_kijun_sen:
        print("The market is in an upward trend.")
    elif last_close < last_kijun_sen:
        print("The market is in a downward trend.")
    else:
        print("The market is moving sideways.")
        
    ######################################## SENKOU_SEN (KUMO) FACTOR
    # Get the last closing price and the last Senkou Span A and B values
    last_close = data['Close'].iloc[-1]
    last_senkou_span_a = data['senkou_span_a'].iloc[-1]
    last_senkou_span_b = data['senkou_span_b'].iloc[-1]

    # Determine the market trend and potential price movements based on the position of the closing price relative to the Senkou Span A and B lines
    if last_close > last_senkou_span_a and last_senkou_span_a > last_senkou_span_b:
        print("Status: Uptrend")
    elif last_close < last_senkou_span_a and last_senkou_span_a < last_senkou_span_b:
        print("Status: Downtrend")
    elif last_close < last_senkou_span_b and last_senkou_span_a > last_senkou_span_b:
        print("Status: Will Dump")
    elif last_close > last_senkou_span_b and last_senkou_span_a < last_senkou_span_b:
        print("Status: Will Pump")
    elif last_senkou_span_b < last_close < last_senkou_span_a and last_senkou_span_a > last_senkou_span_b:
        print("Status: Uptrend and Will Bounce Up")
    elif last_senkou_span_b < last_close < last_senkou_span_a and last_senkou_span_a < last_senkou_span_b:
        print("Status: Downtrend and Will Bounce Down")
    time.sleep(1)
