import yfinance as yf
from datetime import datetime

tickers = ["AAPL", "MSFT", "AMZN", "UNH"]
weights = [0.25, 0.25, 0.25, 0.25]  # Portfolio weights (sum to 1)
start_date = "2021-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')  # Convert datetime to string format

def get_stock_returns(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    daily_returns = stock_data['Adj Close'].pct_change().dropna()
    return daily_returns


def geometric_mean(returns):
    product_of_returns = 1.0
    for ret in returns:
        product_of_returns *= (1 + ret)
    
    geometric_mean = (product_of_returns ** (252 / len(returns))) - 1
    return geometric_mean

# Initialize the overall portfolio returns
portfolio_returns = None

# Calculate individual stock returns and combine them to get portfolio returns
for i, ticker in enumerate(tickers):
    stock_returns_data = get_stock_returns(ticker, start_date, end_date)
    if portfolio_returns is None:
        portfolio_returns = weights[i] * stock_returns_data
    else:
        portfolio_returns += weights[i] * stock_returns_data

# Calculate the annual arithmetic mean
daily_geometric_mean = geometric_mean(portfolio_returns)
annual_geometric_mean = daily_geometric_mean * 252

annual_geometric_mean_percentage = annual_geometric_mean * 100

print(f"Annual Geometric Mean of Portfolio: {annual_geometric_mean:.2f}%")
