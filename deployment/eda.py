import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
import scipy.stats as stats
from datetime import datetime, timedelta


def get_stock_data(symbol, start_date, end_date):
  stock_data = yf.download(symbol, start=start_date, end=end_date)
  return stock_data

symbols = ['ADRO.JK','ANTM.JK','ASII.JK','BBCA.JK','BBRI.JK','INDY.JK','KAEF.JK','PGAS.JK','SIDO.JK','TLKM.JK']
today = datetime.today().date()
end_date = today.strftime('%Y-%m-%d')
start_date = (today - timedelta(days=9*30)).strftime('%Y-%m-%d')

stock_data = get_stock_data(symbols, start_date, end_date)
stock_df = pd.DataFrame(stock_data.round())
columns = ['Adj Close', 'Close', 'Open', 'High', 'Low', 'Volume']

adx_values = {}
for symbol in symbols:
    adx = ta.trend.ADXIndicator(high=stock_data['High'][symbol], low=stock_data['Low'][symbol], close=stock_data['Close'][symbol], window=14).adx()
    adx_values[symbol] = adx.round(2)

# Menggabungkan hasil ADX ke dalam DataFrame
adx_df = pd.DataFrame(adx_values)

rsi_df = pd.DataFrame()

# Loop melalui setiap saham
for symbol in symbols:
    rsi_indicator = ta.momentum.RSIIndicator(stock_data['Adj Close'][symbol])
    rsi = rsi_indicator.rsi()
    rsi_df[symbol] = rsi.round(4)


def run():
  st.header('Stock Dataset')
  st.subheader('Muflih Hafidz Danurhadi RMT 020')

  st.markdown('---')
  penjelasan= 'saya akan menganalisa dan mem-forecast 10 saham dan memberikan opsi untuk pembelian saham 30 hari kerja yang bertujuan untuk meningkatkan profit dalam pemutaran uang di bank. melakukan analisa model forecasting dan meng improve model tersebut.'
  st.write(penjelasan)
  st.markdown('---')
  st.write('### Analisa dan Visualisasi Awal')
  opsi = st.selectbox('pilih saham:',(symbols))

  adj_close = stock_df['Adj Close'][opsi]
  close = stock_df['Close'][opsi]
  open = stock_df['Open'][opsi]
  high = stock_df['High'][opsi]
  low = stock_df['Low'][opsi]
  volume = stock_df['Volume'][opsi]
  bbc_stock_data = pd.concat([adj_close, close, open, high, low, volume], axis=1)
  bbc_stock_data.columns = columns
  st.dataframe(bbc_stock_data)
  
  st.markdown('---')
  fig = plt.figure(figsize=(15, 10))
  stock_df['Adj Close'][opsi].plot()
  st.write(f'#### Grafik Adj Close {opsi}')
  plt.grid()
  st.pyplot(fig)
  st.write(f'Max {opsi}:',stock_df['Adj Close'][opsi].max())
  st.write(f'Min {opsi}:',stock_df['Adj Close'][opsi].min())
  
  st.markdown('---')
  fig2 = plt.figure(figsize=(15, 10))
  daily_returns = stock_df['Adj Close'][opsi].pct_change()
  daily_returns.plot()
  st.write(f'#### Grafik % Change Adj Close {opsi}')
  plt.grid()
  st.pyplot(fig2)
  st.write(f'Min {opsi}:',round(stock_df['Adj Close'][opsi].pct_change().max()*100,3),'%')
  st.write(f'Min {opsi}:',round(stock_df['Adj Close'][opsi].pct_change().min()*100,3),'%')
  st.write(f'Total {opsi}:',round(stock_df['Adj Close'][opsi].pct_change().sum()*100,3),'%')
  volatilitas = round(np.std(daily_returns)*100,3)
  st.write(f'Volatilitas {opsi}:',volatilitas,'%')
  confidence_level = 0.95
  var = stats.norm.ppf(1 - confidence_level, loc=np.mean(daily_returns, axis=0), scale=volatilitas)
  st.write(f'Value at Risk {opsi} :', var.round(2),'%')
  
  st.markdown('---')
  pivot = ((high + low + close) / 3).round(2)
  support = ((2 * pivot) - high).round(2)
  resistance = ((2 * pivot) - low).round(2)
  
  pivot_data = pd.concat([pivot,support,resistance],axis=1)
  pivot_data.columns=['Pivot','Support','Resistance']
  fig3 = plt.figure(figsize=(15, 10))
  pivot_data['Pivot'].plot()
  pivot_data['Support'].plot()
  pivot_data['Resistance'].plot()
  plt.legend()
  st.write(f'#### Grafik Pivot, Support, Resistance {opsi}')
  plt.grid()
  st.pyplot(fig3)
  st.write(f'Mean Pivot {opsi}:',round(pivot_data['Pivot'].mean(),4))
  st.write(f'Mean Support {opsi}:',round(pivot_data['Support'].mean(),4))
  st.write(f'Mean Resistance {opsi}:',round(pivot_data['Resistance'].mean(),4))
  
  st.markdown('---')
  fig4 = plt.figure(figsize=(15, 10))
  rsi_df[opsi].plot(label='RSI')
  adx_df[opsi].plot(label='ADX')
  plt.legend()
  st.write(f'#### ADX dan RSI {opsi}')
  plt.grid()
  st.pyplot(fig4)
  st.write(f'Max ADX {opsi};',adx_df[opsi].max())
  st.write(f'Max RSI {opsi};',rsi_df[opsi].max())        

if __name__ == '__main__':
    run()

