import pandas as pd
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import numpy as np
import time
import datetime
import os
while True:

 try:

    fx_pairs='AUDJPY CADJPY CHFJPY EURJPY NZDJPY USDJPY GBPJPY AUDUSD EURUSD GBPUSD NZDUSD USDCAD USDCHF AUDCAD CADCHF EURCAD GBPCAD NZDCAD AUDCHF EURCHF GBPCHF NZDCHF EURAUD EURGBP EURNZD GBPNZD GBPAUD AUDNZD'
    fx_pairs=fx_pairs.replace(' ','')

    counter1=(len(fx_pairs)/6)
    while counter1>0:
        string=fx_pairs[-6:]
        print(string)
        fx_pairs=fx_pairs[0:-6]
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        client = oandapyV20.API(access_token='insert access token here',
                                headers={"Accept-Datetime-Format":"Unix"})

        params = {
          "count": 1200,
          "granularity": "H1"
        }

        print ('Downloading ohlc data for '+string+'!')
        print('...')

        r = instruments.InstrumentsCandles(instrument=string[0:3]+'_'+string[3:6] , params=params)

        client.request(r)
        df=pd.DataFrame(r.response['candles'])
        #print(df)
        length=(len(df))-1
        low= np.asarray([])
        high= np.asarray([])
        close= np.asarray([])
        openn= np.asarray([])
        while length>0:
            specific_candle=pd.DataFrame(r.response['candles'][length])
            #print(specific_candle)
            obtain_low=specific_candle.tail(2)
            obtain_low=obtain_low.head(1)
            obtain_low=(obtain_low.mid.values)
            #print(obtain_low)
            obtain_close=specific_candle.head(1)
            obtain_close=obtain_close.mid.values
            obtain_high=specific_candle.head(2)
            obtain_high=obtain_high.tail(1)
            obtain_high=(obtain_high.mid.values)
            obtain_open=specific_candle.tail(1)
            obtain_open=obtain_open.mid.values
            #print(obtain_high)
            low=np.insert(low,0,float(obtain_low))
            high=np.insert(high,0,float(obtain_high))
            close=np.insert(close,0,float(obtain_close))
            openn=np.insert(openn,0,float(obtain_open))
            kopen= pd.DataFrame(columns=['open'], data=openn)
            khigh= pd.DataFrame(columns=['high'], data=high)
            klow=pd.DataFrame(columns=['low'], data=low)
            kclose=pd.DataFrame(columns=['close'], data=close)
            klines=pd.concat([kopen,khigh,klow,kclose,df], axis=1)

            length=length-1

        klines.mid=klines.mid.shift(-1)
        klines.complete=klines.complete.shift(-1)
        klines.time=klines.time.shift(-1)
        klines.volume=klines.volume.shift(-1)
        klines=klines.drop(columns=['mid'])
        klines.drop(klines.tail(1).index,inplace=True)
        #klines=klines.rename(columns={'complete': string})
        #print(klines)
        print (klines.head(5))
        print(klines.tail(5))
        if os.name == 'nt':
            klines.to_csv((r'E:\\OHLC\\'+string+'.csv')) #if using windows change directory
        else:
            klines.to_csv((r'/home/q/Dropbox/Dracula Blood Money Algo/H1OHLC/'+string+'.csv'))#if using linux/mac change directory 
 except Exception as e:
     print(e)
     print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
     print('Downloaded all candlestick data. sleeping for 30 min. zzz')
     time.sleep(1800)
