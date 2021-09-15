import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# function: It takes a dataframe with stock data (dataframe must contain Date and Close columns),
# a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
                             y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
                             y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()


# get the stock
tesla = yf.Ticker('TSLA')
# use history function get history share price, set the period to max
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)
print(tesla_data.head())

# use url get tesla data
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork23455606-2021-01-01'
html_data = requests.get(url).text
# We can also use the pandas read_html function using the url
html_soup = BeautifulSoup(html_data, 'html5lib')
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in html_soup.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text

    # Finally we append the data of each row to the table
    tesla_revenue = tesla_revenue.append(
        {'Date': date, 'Revenue': revenue}, ignore_index=True)

print(tesla_revenue.head())
print('-----------------------------------------------------------')

# remove  the comma and dollar sign from the Revenue column
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "")
# remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

# read_html_pandas_data = pd.read_html(url)
# #  convert the BeautifulSoup object to a string
# read_html_pandas_data = pd.read_html(str(html_soup))
# # there is only one table in this website
# tesla_revenue = read_html_pandas_data[1]
# print(tesla_revenue.head())

# get GME data
gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
print(gme_data.head())
print('----------------------------------------------')

# html data
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork23455606-2021-01-01'
html_data = requests.get(url).text
# We can also use the pandas read_html function using the url
html_soup = BeautifulSoup(html_data, 'html5lib')
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in html_soup.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text

    # Finally we append the data of each row to the table
    gme_revenue = gme_revenue.append(
        {'Date': date, 'Revenue': revenue}, ignore_index=True)

# remove  the comma and dollar sign from the Revenue column
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$', "")
# remove an null or empty strings in the Revenue column.
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
print(gme_revenue.head())
print('------------------------------------------------------')

# use function to show a plot of tesla
make_graph(tesla_data, tesla_revenue, 'Tesla')
