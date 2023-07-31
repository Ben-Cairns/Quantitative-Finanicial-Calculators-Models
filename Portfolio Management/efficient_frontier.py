import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.optimize import minimize

def fetch_yahoo_finance_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']

def generate_random_portfolios(num_portfolios, num_assets):
    portfolios = []
    for _ in range(num_portfolios):
        weights = np.random.rand(num_assets)
        weights /= np.sum(weights)
        portfolios.append(weights)
    return portfolios

def portfolio_return(weights, returns):
    return np.sum(returns * weights)

def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def objective_function(weights, returns, cov_matrix, risk_free_rate):
    portfolio_return_ = portfolio_return(weights, returns)
    portfolio_volatility_ = portfolio_volatility(weights, cov_matrix)
    sharpe_ratio = (portfolio_return_ - risk_free_rate) / portfolio_volatility_
    return -sharpe_ratio

def plot_efficient_frontier(expected_returns, cov_matrix, risk_free_rate, num_portfolios=10000):
    num_assets = len(expected_returns)
    portfolios = generate_random_portfolios(num_portfolios, num_assets)
    portfolios = np.array(portfolios)

    portfolio_returns = np.dot(portfolios, expected_returns)
    portfolio_volatilities = np.array([portfolio_volatility(weights, cov_matrix) for weights in portfolios])

    results = minimize(
        objective_function,
        np.ones(num_assets) / num_assets,
        args=(expected_returns, cov_matrix, risk_free_rate),
        bounds=tuple((0, 1) for _ in range(num_assets)),
        constraints=({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}),
    )

    optimal_weights = results.x
    optimal_return = portfolio_return(optimal_weights, expected_returns)
    optimal_volatility = portfolio_volatility(optimal_weights, cov_matrix)
    optimal_sharpe_ratio = (optimal_return - risk_free_rate) / optimal_volatility
    
    # Keep track of portfolio data
    portfolio_data = []

    for i, weights in enumerate(portfolios):
        portfolio_return_ = portfolio_return(weights, expected_returns)
        portfolio_volatility_ = portfolio_volatility(weights, cov_matrix)
        sharpe_ratio = (portfolio_return_ - risk_free_rate) / portfolio_volatility_

        portfolio_data.append({
            'Portfolio': i + 1,
            'Return': portfolio_return_,
            'Volatility': portfolio_volatility_,
            'Sharpe Ratio': sharpe_ratio,
            **dict(zip(tickers, weights))
        })

    portfolio_df = pd.DataFrame(portfolio_data)
    top_10_portfolios = portfolio_df.nlargest(10, 'Sharpe Ratio')

    efficient_frontier_data = go.Scatter(
        x=portfolio_volatilities,
        y=portfolio_returns,
        mode='markers',
        marker=dict(
            size=5,
            color='blue',
            opacity=0.3,
            colorscale='Viridis'
        ),
        name='Efficient Frontier'
    )

    optimal_portfolio_data = go.Scatter(
        x=[optimal_volatility],
        y=[optimal_return],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
            symbol='star'
        ),
        name='Optimal Portfolio'
    )

    top_10_portfolios_data = go.Scatter(
        x=top_10_portfolios['Volatility'],
        y=top_10_portfolios['Return'],
        mode='markers',
        marker=dict(
            size=8,
            color='green',
            symbol='circle'
        ),
        name='Top 10 Portfolios'
    )

    layout = go.Layout(
        title='Efficient Frontier',
        xaxis=dict(title='Volatility'),
        yaxis=dict(title='Return'),
        hovermode='closest',
        showlegend=True
    )

    fig = go.Figure(data=[efficient_frontier_data, optimal_portfolio_data, top_10_portfolios_data], layout=layout)
    fig.show()
    
    return top_10_portfolios

def plot_top_10_portfolios(top_10_portfolios):
    top_10_weights = top_10_portfolios.iloc[:, 4:].values
    tickers = top_10_portfolios.columns[4:]
    portfolio_indices = [f'Portfolio {int(p)}' for p in top_10_portfolios['Portfolio']]

    bar_data = []
    for i, weights in enumerate(top_10_weights):
        bar_data.append(go.Bar(
            x=tickers,
            y=weights,
            name=portfolio_indices[i]
        ))

    layout = go.Layout(
        title='Top 10 Portfolio Weightings',
        xaxis=dict(title='Asset'),
        yaxis=dict(title='Weight'),
        barmode='stack',
        showlegend=True
    )

    fig = go.Figure(data=bar_data, layout=layout)
    fig.show()

if __name__ == "__main__":
    # Enter the tickers in the portfolio and the desired date range
    tickers = ['BHP.AX', 'CSL.AX', 'TNE.AX', 'BKW.AX', 'JBH.AX', 'PME.AX', 'RMD.AX', 'JHX.AX', 'WTC.AX', 'CAR.AX', 'QAU.AX', 'STW.AX', 'QQQ', 'VGK']
    start_date = '2013-01-01'
    end_date = '2023-07-31'

    # Fetch data from Yahoo Finance
    historical_data = fetch_yahoo_finance_data(tickers, start_date, end_date)

    # Calculate expected returns and covariance matrix
    expected_returns = historical_data.pct_change().mean() * 252
    cov_matrix = historical_data.pct_change().cov() * 252

    # Setting the risk-free rate
    risk_free_rate = 0.05

    # Plot the efficient frontier and get the top 10 optimal portfolios
    top_10_portfolios = plot_efficient_frontier(expected_returns, cov_matrix, risk_free_rate)

    # Display the DataFrame of the top 10 portfolios
    print("Top 10 Optimal Portfolios:")
    print(top_10_portfolios[['Portfolio', 'Return', 'Volatility', 'Sharpe Ratio', *tickers]])

    # Plot the top 10 portfolios' weightings
    plot_top_10_portfolios(top_10_portfolios)
