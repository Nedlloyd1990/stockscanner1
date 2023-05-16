import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import ta
import numpy as np
import streamlit as st

st.sidebar.title("**Stock Scanner 2022**")

list_stk = ["ZYDUSLIFE.NS","ZOMATO.NS","WIPRO.NS","VEDL.NS","MCDOWELL-N.NS","ULTRACEMCO.NS","UPL.NS","TORNTPHARM.NS","TITAN.NS","TECHM.NS","TATASTEEL.NS","TATAMOTORS.NS","TATACONSUM.NS","TCS.NS","SUNPHARMA.NS","SAIL.NS","SBIN.NS","SIEMENS.NS","SHREECEM.NS","SRF.NS","SBILIFE.NS","SBICARD.NS","RELIANCE.NS","PNB.NS","PGHH.NS","POWERGRID.NS","PEL.NS","PIDILITIND.NS","PIIND.NS","PAYTM.NS","ONGC.NS","NESTLEIND.NS","NTPC.NS","NMDC.NS","MUTHOOTFIN.NS","MINDTREE.NS","MARUTI.NS","MARICO.NS","M&M.NS","LUPIN.NS","LT.NS","LTI.NS","KOTAKBANK.NS","JUBLFOOD.NS","JSWSTEEL.NS","INDIGO.NS","INFY.NS","NAUKRI.NS","INDUSINDBK.NS","INDUSTOWER.NS","IOC.NS","ITC.NS","ICICIPRULI.NS","ICICIGI.NS","ICICIBANK.NS","HDFC.NS","HINDUNILVR.NS","HINDALCO.NS","HEROMOTOCO.NS","HAVELLS.NS","HDFCLIFE.NS","HDFCBANK.NS","HDFCAMC.NS","HCLTECH.NS","GRASIM.NS","GODREJCP.NS","GLAND.NS","GAIL.NS","NYKAA.NS","EICHERMOT.NS","DRREDDY.NS","DIVISLAB.NS","DABUR.NS","DLF.NS","COLPAL.NS","COALINDIA.NS","CIPLA.NS","CHOLAFIN.NS","BRITANNIA.NS","BOSCHLTD.NS","BIOCON.NS","BHARTIARTL.NS","BPCL.NS","BERGEPAINT.NS","BANKBARODA.NS","BANDHANBNK.NS","BAJAJHLDNG.NS","BAJAJFINSV.NS","BAJFINANCE.NS","BAJAJ-AUTO.NS","AXISBANK.NS","DMART.NS","ASIANPAINT.NS","APOLLOHOSP.NS","AMBUJACEM.NS","ADANITRANS.NS","ADANIPORTS.NS","ADANIGREEN.NS","ADANIENT.NS","ACC.NS"]

dict1 = {}

current_date = st.sidebar.date_input("Select Date", datetime.today())
time_int = st.sidebar.selectbox('Select Timeframe', ('1d', '1h'))

for i in list_stk:
    stk = yf.Ticker(i)
    stk_price = stk.history(start=current_date - timedelta(days=100), end=current_date, interval=time_int)
    dataframe = pd.DataFrame(stk_price)
    ma20 = sum(dataframe.Close[-20:]) / 20
    ta1 = ta.momentum.stochrsi(dataframe.Close, 14)

    if len(ta1) >= 2:
        dict1[i] = [ta1[-2] * 100]
        dict1[i].append(ta1[-1] * 100)
        dict1[i].append(dataframe.Close[-1])
        dict1[i].append(ma20)

df = pd.DataFrame.from_dict(dict1, orient='index', columns=["Previous", "Current", "CPrice", "MA"])
df["stochrsi"] = np.where(((df.Previous < 20) & (df.Current > 20)), "up",
                          np.where(((df.Previous > 80) & (df.Current < 80)), "down", "-"))
df["Signal"] = np.where((((df.stochrsi != "-") & (df.CPrice < df.MA) & (df.Previous > 80) & (df.Current < 80)) |
                         ((df.stochrsi != "-") & (df.CPrice > df.MA) & (df.Previous < 20) & (df.Current > 20))), "yes", "-")

d2 = df[df['stochrsi'] != "-"]
d1 = pd.DataFrame(d2)
st.dataframe(d1)
