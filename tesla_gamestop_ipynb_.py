# -*- coding: utf-8 -*-

# IBM Data Analyst
# Python Project for Data Science
# Tesla and GameStop Stock data analysis

# Please install the following Python 3 packages before running this code
#!pip install pandas
#!pip install requests
#!pip install bs4
#!pip install html5lib
#!pip install lxml
#!pip install plotly
#!pip install matplotlib
#!pip install yfinance

"""Question 1: Use yfinance to Extract Stock Data

Reset the index, save, and display the first five rows of the tesla_data dataframe using the head function.
"""

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Download historical data for a TESLA stock
tsla = yf.Ticker("TSLA")
tsla_data = tsla.history(period="max")

# Reset the index
tsla_data.reset_index(inplace=True)

# Display the first rows
print(tsla_data.head())

"""Question 2: Use Webscraping to Extract Tesla Revenue Data

Display the last five rows of the tesla_revenue dataframe using the tail function.
"""

# Get data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data  = requests.get(url).text

# Parse HTML data
soup = BeautifulSoup(html_data, 'html.parser')

# Find the table
table = soup.find_all("tbody")[1]

# Create an empty DataFrame
tsla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Iterate through each row in table
for row in table.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    new_row = pd.DataFrame({"Date": [date], "Revenue": [revenue]})
    tsla_revenue = pd.concat([tsla_revenue, new_row], ignore_index=True)

# Clean the data
tsla_revenue["Revenue"] = tsla_revenue['Revenue'].str.replace(r',|\$',"", regex=True)
tsla_revenue.dropna(inplace=True)
tsla_revenue = tsla_revenue[tsla_revenue['Revenue'] != ""]

# Display the last 5 rows
print(tsla_revenue.tail())

"""Question 3: Use yfinance to Extract Stock Data

Reset the index, save, and display the first five rows of the gme_data dataframe using the head function.
"""

# Download historical data for a GameStop Corp. (GME) stock similar to Question 1

gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

"""Question 4: Use Webscraping to Extract GME Revenue Data

Display the last five rows of the gme_revenue dataframe using the tail function.
"""

# Get data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data2  = requests.get(url).text

# Parse HTML data
soup = BeautifulSoup(html_data2, 'html.parser')

# Find the table
table = soup.find_all("tbody")[1]

# Create an empty DataFrame
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Iterate through each row in table
for row in table.find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    new_row = pd.DataFrame({"Date": [date], "Revenue": [revenue]})
    gme_revenue = pd.concat([gme_revenue, new_row], ignore_index=True)

# Clean the data
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(r',|\$',"", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

# Last 5 rows
print(gme_revenue.tail())

"""Question 5: Plot Tesla Stock Graph
Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph.
"""

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# As if we have two different data source we've got a little bit incomplete graph for revenue

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
make_graph(tsla_data, tsla_revenue, 'Tesla Stock Data')

"""Question 6: Plot GameStop Stock Graph

Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph.

"""

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

make_graph(gme_data, gme_revenue,"GameStop Stock Data")



