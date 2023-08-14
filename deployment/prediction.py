import streamlit as st
import pickle
import pandas as pd
import numpy as np
import ta
import tensorflow as tf
from tensorflow.keras.models import load_model
import yfinance as yf
from datetime import datetime, timedelta
import scipy.stats as stats
import matplotlib.pyplot as plt

def get_stock_data(symbol, start_date, end_date):
  stock_data = yf.download(symbol, start=start_date, end=end_date)
  return stock_data

symbols = ['ADRO.JK','ANTM.JK','ASII.JK','BBCA.JK','BBRI.JK','INDY.JK','KAEF.JK','PGAS.JK','SIDO.JK','TLKM.JK']
today = datetime.today().date()
end_date = today.strftime('%Y-%m-%d')
start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')

stock_data = get_stock_data(symbols, start_date, end_date)
stock_df_inf = pd.DataFrame(stock_data['Adj Close'].round())
columns = ['Adj Close', 'Close', 'Open', 'High', 'Low', 'Volume']


def run():
    st.header('Stock Dataset')
    st.subheader('Muflih Hafidz Danurhadi RMT 020')

    penjelasan= 'Hasil dari model improvement untuk memprediksi saham 30 hari kedepan'
    st.write(penjelasan)
    st.markdown('---')
    best_model = load_model('best_model.h5')

    y_pred_inf = best_model.predict(stock_df_inf)
    y_pred_inf_df = pd.DataFrame(y_pred_inf.round(), columns=symbols)
    st.dataframe(y_pred_inf_df)
    st.write('### Analisa dan Visualisasi Hasil Prediksi')
    symbol = st.selectbox('pilih saham:',(symbols))
    
    st.markdown('---')
    fig = plt.figure(figsize=(15, 10))
    y_pred_inf_df[symbol].plot()
    st.write(f'#### Grafik Adj Close {symbol}')
    plt.grid()
    st.pyplot(fig)
    st.write(f'Max {symbol}:',y_pred_inf_df[symbol].max())
    st.write(f'Min {symbol}:',y_pred_inf_df[symbol].min())
    
    st.markdown('---')
    fig2 = plt.figure(figsize=(15, 10))
    daily_returns_inf = y_pred_inf_df.pct_change()
    daily_returns_inf[symbol].plot()
    st.write(f'#### Grafik % Change Adj Close {symbol}')
    plt.grid()
    st.pyplot(fig2)
    st.write(f'% Max Change {symbol} :', round((y_pred_inf_df[symbol].pct_change().max())*100,4),'%')
    st.write(f'% Min Change {symbol} :', round((y_pred_inf_df[symbol].pct_change().min())*100,4),'%')
    
    volatilitas_inf = round(np.std(daily_returns_inf[symbol])*100,4)
    st.write(f'Max daily return {symbol}:',round(daily_returns_inf[symbol].max(),4),'%')
    st.write(f'Min Daily return {symbol}:',round(daily_returns_inf[symbol].min(),4),'%')
    st.write(f'Total Daily return {symbol}:',round(daily_returns_inf[symbol].sum(),4),'%')
    st.write(f'Volatilitas {symbol}:',volatilitas_inf,'%')
    
    confidence_level = 0.95
    var = stats.norm.ppf(1 - confidence_level, loc=np.mean(daily_returns_inf[symbol], axis=0), scale=volatilitas_inf)
    st.write(f'Value at Risk {symbol} :', var.round(2),'%')
    
    st.markdown('---')    
    rsi_inf_df = pd.DataFrame()

    # Loop melalui setiap saham
    rsi_indicator = ta.momentum.RSIIndicator(y_pred_inf_df[symbol])
    rsi = rsi_indicator.rsi()
    rsi_inf_df[symbol] = rsi.round(4)
    fig4 = plt.figure(figsize=(15, 10))
    rsi_inf_df[symbol].plot(label='RSI')
    plt.legend()
    st.write(f'#### RSI {symbol}')
    plt.grid()
    st.pyplot(fig4)
    st.write(f'Max RSI {symbol};',rsi_inf_df[symbol].max())
    st.write(f'Min RSI {symbol};',rsi_inf_df[symbol].min())         

    st.markdown('---') 
    st.write(f'Keputusan saham {symbol}:')  
    if daily_returns_inf[symbol].sum()>= 0 and var >=-3:
        st.write(f'stock {symbol} bagus dibeli untuk 30 hari ke depan')
    else:
        st.write(f'stock {symbol} kurang bagus dibeli untuk 30 hari ke depan')

if __name__ == '__main__':
    run()


