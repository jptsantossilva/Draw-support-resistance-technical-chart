import pandas as pd
import requests

import mplfinance as mpf
import streamlit as st
import yfinance as yf
from yahooquery import Screener
# import matplotlib.pyplot as plt


# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
#     # layout="wide"
# )

def get_symbols_list():
    s = Screener()
    data = s.get_screeners('all_cryptocurrencies_us')
    # Access the 'symbol' field from the data object
    symbols = [item['symbol'] for item in data['all_cryptocurrencies_us']['quotes']]
    return symbols


symbols_list = get_symbols_list()

c1, c2, c3 = st.columns([1,1,1])
with c1:
    # trading pair
    # default_symbol = "BTC"
    symbol = st.selectbox(
        label='Symbol',
        options=symbols_list,
    index=0)
    # symbol = st.text_input(
    #     label='Symbol',
    #     value=default_symbol
    # )
    # st.write('trading_pair: ', trading_pair)
with c2:
    # timeframe
    timeframe_list = ['1d','1wk']
    timeframe = st.selectbox(
    label='Time Frame',
    options=timeframe_list)
    # st.write('timeframe:', timeframe)
with c3:
    # start date
    # Calculate the default date value
    # default_date = datetime.date.today() - datetime.timedelta(days=12*30)
    # start_date = st.date_input(
    # label="Start Date",
    # value=default_date)
    # st.write('start_date: ', str(start_date))

    period_list = ["1mo","3mo","6mo","ytd","1y","2y","5y","max"]
    period = st.selectbox(
        label="Time Period",
        options=period_list,
        index=period_list.index("6mo")
        )


# st.markdown('---')

st.sidebar.subheader('Chart Settings')
# st.sidebar.caption('Adjust charts settings and then press apply')

# with st.sidebar.form('settings_form'):
with st.sidebar:
    chart_style = 'charles'
    chart_types = [
        'candle', 'ohlc', 'line'
    ]
    chart_type = st.selectbox('Chart type', options=chart_types, index=chart_types.index('candle'))

    window = st.slider(
        label='Edge Sensitivity', 
        min_value=0, 
        max_value=9, 
        value=5,
        step=1)
    window = 50 - (window*5) 
    # st.write(f"window:{window}")

    show_volume = st.checkbox('Show Volume', False)
    # st.form_submit_button('Apply')

def get_historical_data(symbol, period, timeframe):
    with st.spinner('Getting data...'):
        df = yf.download(symbol, period=period, interval=timeframe)
        return df

data = get_historical_data(symbol, period, timeframe)

supports = data[data.Close == data.Close.rolling(window, center=True).min()].Close       
resistances = data[data.Close == data.Close.rolling(window, center=True).max()].Close

levels = pd.concat([supports, resistances])
# list of tuples
levels_list = [(index, value) for index, value in levels.items()]

# Get current timestamp
# Get today's datetime as a Timestamp object
# today = pd.Timestamp.now().normalize()

# Get the last date of plotted data
last_date = data.index[-1]

# end of lines
end_of_lines = []  # List to store the new items

# Iterate over the levels2 list and add consecutive items
for i in range(len(levels_list)):
    last_item = levels_list[i][1]  # Get the last item of the current level
    # new_item = (today, last_item)  # Create a new item with today's datetime and the last item
    new_item = (last_date, last_item)  # Create a new item with today's datetime and the last item
    end_of_lines.append(new_item)

joined_list = [[levels_list[i], end_of_lines[i]] for i in range(len(levels_list))]

fig, ax = mpf.plot(
    data, 
    title=f'{symbol}',
    type=chart_type, 
    alines=joined_list, 
    style='charles',
    figsize=(15,10),
    volume=show_volume,
    # Need this setting for Streamlit
    returnfig=True
    
    )
st.pyplot(fig)