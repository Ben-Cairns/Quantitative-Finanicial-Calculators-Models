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

def arithmetic_mean(returns):
    return sum(returns) / len(returns)

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
daily_arithmetic_mean = arithmetic_mean(portfolio_returns)
annual_arithmetic_mean = daily_arithmetic_mean * 252

annual_arithmetic_mean_percentage = annual_arithmetic_mean * 100

print(f"Annual Arithmetic Mean of Portfolio: {annual_arithmetic_mean_percentage:.2f}%")



