import pandas as pd
import yfinance as yf

def get_stock_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data

def calculate_std_dev(stock_returns):
    return stock_returns.std()

def calculate_beta_and_capm(daily_returns, risk_free_rate, market_expected_return):
    # Calculate the standard deviation of daily returns for each stock
    std_devs = calculate_std_dev(daily_returns)
    
    # Calculate the correlation of each stock with the market
    correlations_with_market = daily_returns.corrwith(daily_returns['^GSPC'])
    
    betas = correlations_with_market * std_devs * std_devs['^GSPC'] / std_devs['^GSPC']**2
    
    # Calculate the CAPM for each stock
    capm = risk_free_rate + betas * (market_expected_return - risk_free_rate)
    
    return std_devs, betas, capm

#Input the desired stocks and date range
stock_tickers = ['AAPL', 'CVX', 'MSFT', '^GSPC'] 
start = '2022-01-01'
end = '2023-01-01'

# Inputs
risk_free_rate = 0.04
market_expected_return = 0.09

# Fetch historical data and calculate daily returns
stock_data = pd.DataFrame()
for ticker in stock_tickers:
    data = get_stock_data(ticker, start, end)
    stock_data[ticker] = data['Close'] 

daily_returns = stock_data.pct_change().dropna()

# Calculate standard deviation, beta, and CAPM for each stock
std_devs, betas, capm = calculate_beta_and_capm(daily_returns, risk_free_rate, market_expected_return)

# Round the CAPM values to 2 decimal places
capm_rounded = (capm * 100).round(2)

# Create a DataFrame to display the results
results_df = pd.DataFrame({
    'Beta': betas,
    'CAPM': capm_rounded.apply(lambda x: f"{x}%")
})

print(results_df)

