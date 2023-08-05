import yfinance as yf
import pandas as pd

risk_free_rate = 0.04

# Macro variables
macro_variables = {
    'gdp_growth': 0.02,
    'inflation': 0.02,
    'credit_growth': 0.06,
}

# Enter desired assets and date range
stock_tickers = ['AAPL', 'MSFT', 'AMZN', 'UNH']
start_date = '2020-01-01'
end_date = '2023-07-01'

# Input beta values for each stock against each macroeconomic factor
beta_values = {
    'AAPL': {'gdp_growth': 1.5, 'inflation': 1.2, 'credit_growth': 0.4},
    'MSFT': {'gdp_growth': 1.2, 'inflation': 1.5, 'credit_growth': 0.35},
    'AMZN': {'gdp_growth': 1.8, 'inflation': 1.9, 'credit_growth': 0.6},
    'UNH': {'gdp_growth': 1.0, 'inflation': 1.0, 'credit_growth': 0.2},
}

def calculate_beta(daily_returns, calculate_std_dev):
    # Calculate the standard deviation of daily returns for each stock
    std_devs = calculate_std_dev(daily_returns)
    
    # Initialize a DataFrame to store betas
    betas = pd.DataFrame(index=daily_returns.columns, columns=macro_variables.keys())
    
    for stock_ticker in daily_returns.columns:
        # Get the beta values for the current stock
        stock_betas = beta_values.get(stock_ticker)
        
        if stock_betas is not None:
            # Calculate beta for each stock against each macro factor
            for macro_factor, beta in stock_betas.items():
                betas.loc[stock_ticker, macro_factor] = beta
    
    return betas

def expected_return(betas, stock_ticker):
    macro_factors = pd.Series(macro_variables)
    stock_betas = betas.loc[stock_ticker]
    expected_return = risk_free_rate + (macro_factors * stock_betas).sum()
    return expected_return

def apt():
    data = yf.download(stock_tickers, start=start_date, end=end_date)
    close_prices = data['Adj Close']
    
    # Calculate daily returns
    daily_returns = close_prices.pct_change().dropna()
    
    # Calculate betas
    betas = calculate_beta(daily_returns, calculate_std_dev=pd.DataFrame.std)
    
    # Display the results
    print("Stock Ticker  Expected Return")
    for ticker in stock_tickers:
        beta = betas.loc[ticker]
        exp_return = expected_return(betas, ticker)
        print(f"{ticker:6}            {exp_return:.4f}")

if __name__ == "__main__":
    apt()

