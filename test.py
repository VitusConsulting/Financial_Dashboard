import pandas as pd
import numpy as np
import requests
import streamlit as st

url = "https://financialmodelingprep.com/api/v3/symbol/NASDAQ"
headers = {
    'apikey': 'YOUR API KEY',
}

response = requests.get(url, params=headers)

nasdaq_data = response.json()
nasdaq_data = pd.DataFrame(nasdaq_data)

symbol_nasdaq = nasdaq_data['symbol']
all_symbols = symbol_nasdaq.copy()

# Set the dashboard layout to fill the screen
st.set_page_config(layout="wide")

# Put the title
st.title('NASDAQ Financial Stock Dashboard')
st.write('Data provided by Financial Modeling Prep. Dashboard powered by Streamlit')

with st.sidebar:
    # User input for searching the company symbol
    user_input = st.text_input("Search for a Company Symbol:", "")

    # Filter the symbol list based on user input
    filtered_symbols = symbol_nasdaq[symbol_nasdaq.str.contains(user_input, case=False)].tolist()

    # Symbol that was not selected
    remaining_symbols = [symbol for symbol in symbol_nasdaq.tolist() if symbol not in filtered_symbols]

    # Combine all the symbol plus placeholder
    all_symbols = ['Select the company'] + filtered_symbols + remaining_symbols

    # Find the index of user_input in all_symbols. If not found, default to 0 ('Select the company')
    index_to_select = all_symbols.index(user_input) if user_input in all_symbols else 0

    # Display the selection search box
    selected_symbol = st.selectbox(label='Company Selection', options=all_symbols, index=index_to_select)

url = "https://financialmodelingprep.com/api/v3/quote/AAPL"
headers = {
    'apikey': 'YOUR API KEY',
}

response = requests.get(url, params=headers)

stock = response.json()
stock = pd.DataFrame(stock)

if selected_symbol == 'Select the company':
    st.write('No data yet')
else:
    # Acquire the stock information
    req = f"https://financialmodelingprep.com/api/v3/quote/{selected_symbol}"

    response = requests.get(req, params=headers)

    stock_quote = response.json()

    # Select the important data
    stock_name = stock_quote[0]['name']
    stock_price = stock_quote[0]['price']
    stock_chg = stock_quote[0]['changesPercentage']
    stock_vol = stock_quote[0]['volume']

    # Put the information of the company
    st.write(f'Stock information for {selected_symbol} : {stock_name} ')

    # Display the stock price, the percentage changes, and the volume
    st.metric("Price", f"$ {stock_price}", f"{stock_chg} %")
    st.metric("Volume", f"$ {stock_vol}")

url = "https://financialmodelingprep.com/api/v3/profile/AAPL"
headers = {
    'apikey': 'YOUR API KEY',
}

response = requests.get(url, params=headers)

comp = response.json()
comp = pd.DataFrame(comp)

if selected_symbol == 'Select the company':
    st.write('No data yet')
else:
    # Acquire the company profile data
    req = f"https://financialmodelingprep.com/api/v3/profile/{selected_symbol}"

    response = requests.get(req, params=headers)
comp_info = response.json()

    # Select the important information
comp_desc = comp_info[0]['description']
comp_web = comp_info[0]['website']
comp_name = comp_info[0]['companyName']

st.header(f'Company information for {selected_symbol} : {comp_name} ', divider='gray')

    # Put the description of the company with the website
st.text_area("Company Description", f"{comp_desc}")
st.write(f"Visit [Company Website]({comp_web}) for more information.")

url = "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual"

response = requests.get(url, params=headers)

inc = response.json()
inc = pd.DataFrame(inc)

url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/AAPL?period=annual"

response = requests.get(url, params=headers)

bss = response.json()
bss = pd.DataFrame(bss)

# Acquire the income statement data
req = f"https://financialmodelingprep.com/api/v3/income-statement/{selected_symbol}?period=annual"
response = requests.get(req, params=headers)
income_info = response.json()
income_info = pd.DataFrame(income_info)

# Acquire the balance sheet data
req = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{selected_symbol}?period=annual"
response = requests.get(req, params=headers)
bss_info = response.json()
bss_info = pd.DataFrame(bss_info)

st.header(f'Company information for {selected_symbol} : {comp_name} ', divider='gray')

st.text_area("Company Description", f"{comp_desc}", key="unique_key_for_description")
st.write(f"Visit [Company Website]({comp_web}) for more information.")

# Divide the chart area into two segment
col1_cha, col2_cha = st.columns(2)

with col1_cha:
    st.subheader('Revenue Chart')
    st.line_chart(income_info, x="fillingDate", y="revenue")

with col2_cha:
    st.subheader('Balance Sheet Chart')
    st.line_chart(bss_info, x="fillingDate", y=["totalAssets", "totalEquity", "totalDebt"])

