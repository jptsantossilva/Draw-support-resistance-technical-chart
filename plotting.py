import pandas as pd
import numpy as np

import mplfinance as mpf

import streamlit as st

import yfinance as yf
from yahooquery import Screener

# st.set_page_config(
#     page_title="Hello",
#     page_icon="👋",
#     # layout="wide"
# )

def get_symbols_list():
    s = Screener()

    # crypto
    data = s.get_screeners('all_cryptocurrencies_us')
    symbols_crypto = [item['symbol'] for item in data['all_cryptocurrencies_us']['quotes']]
    
    # etfs us
    data = s.get_screeners('top_etfs_us')
    symbols_etfs_us = [item['symbol'] for item in data['top_etfs_us']['quotes']]
    
    # all companies within the S&P500
    tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    data = tables[0]['Symbol'].tolist()
    symbols_sp500 = [symbol.replace(".", "-") for symbol in data]

    symbols = symbols_crypto + symbols_etfs_us + symbols_sp500

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
        label='Pivot Sensitivity', 
        min_value=0, 
        max_value=9, 
        value=5,
        step=1)
    window = 50 - (window*5) 

    show_volume = st.checkbox('Show Volume', False)
    # st.form_submit_button('Apply')

def get_historical_data(symbol, period, timeframe):
    with st.spinner('Getting data...'):
        df = yf.download(symbol, period=period, interval=timeframe)
        return df

data = get_historical_data(symbol, period, timeframe)
data.index.name = 'Date'

supports = data[data.Close == data.Close.rolling(window, center=True).min()].Close       
resistances = data[data.Close == data.Close.rolling(window, center=True).max()].Close

levels = pd.concat([supports, resistances])
# list of tuples
levels_list = [(index, value) for index, value in levels.items()]

# Get the last date of plotted data
last_date = max(data.index)

# end of lines
end_of_lines = []  # List to store the new items

# Iterate over the levels2 list and add consecutive items
for i in range(len(levels_list)):
    last_item = levels_list[i][1]  # Get the last item of the current level
    # new_item = (today, last_item)  # Create a new item with today's datetime and the last item
    new_item = (last_date, last_item)  # Create a new item with today's datetime and the last item
    end_of_lines.append(new_item)

sr_list = [[levels_list[i], end_of_lines[i]] for i in range(len(levels_list))]

line_color = '#6993b0'

def plot_all():
    fig, ax = mpf.plot(
        data, 
        title=f'{symbol}',
        type=chart_type, 
        alines=dict(alines=sr_list, colors=line_color, alpha=1),
        # mav=100,
        # ema=100,
        
        style='charles',
        figsize=(15,10),
        volume=show_volume,
        # Need this setting for Streamlit
        returnfig=True
        
        )
    
    # Iterate over each aline and add text annotation
    for aline in sr_list:
        x = aline[0][0]
        y = aline[0][1]
        number = float(aline[0][1])
        if number >= 1000:
            formatted_number = int(number)
        elif number >= 1:
            formatted_number = np.around(number, decimals=2)
        else:
            formatted_number = np.around(number, decimals=6)
        text = formatted_number

        ax[0].annotate(
            text, 
            xy =(len(data), y), 
            textcoords='offset points', 
            xytext=(0,0),            
            color='#3c5c71',
            alpha=1,
            verticalalignment='center'
            )

    st.pyplot(fig)

plot_all()
