# Monte Carlo Portfolio Simulation based on Historical Data

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

T = 2
STEPS = 252
DELTA_T = T/STEPS
RF = 0.04

class Portfolio_Analysis:
    def __init__(self, tickers, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers = tickers

        # Collect Data
        self.stock_profiles = [Stock_Profile(ticker, start_date, end_date) for ticker in tickers]


    def calculate_independent_MC_returns(self,n_simulations):
        paths = []

        for stock in self.stock_profiles:
            stock_paths = np.zeros((n_simulations, STEPS+1))

            for i in range(n_simulations):
                stock_paths[i] = stock.simulate_GBM_path()
            paths.append(self.final_returns_from_paths(stock_paths))
            
        return np.array(paths, dtype=float)

    def final_returns_from_paths(self, stock_paths):
        return stock_paths[:,-1] / stock_paths[:,0] -1
    
    def neg_sharpe_diversified(self, w, all_returns, risk_free=0.4, lf_reg=0.05):
        w = np.array(w, dtype=float)
        all_returns = np.array(all_returns, dtype=float)

        port_returns = all_returns.dot(w)
        mean_r = np.mean(port_returns)
        std_r = np.std(port_returns, ddof=1)
        
        if std_r <= 0:
            return 1e6

        sharpe = (mean_r - risk_free) / std_r

        # Penalize large weights to encourage diversification
        penalty = lf_reg * np.sum(w**2)

        return -sharpe + penalty


    def optimize_inital_weights(self, paths):
        lf_reg = 0.01
        bounds = [(0.0, 1.0) for _ in range(len(self.tickers))]
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0},)
        x0 = np.ones(len(self.tickers)) / len(self.tickers)
        res_b = minimize(self.neg_sharpe_diversified, x0, args=(paths, RF, lf_reg),
                 method='SLSQP', bounds=bounds, constraints=constraints,
                 options={'maxiter': 200, 'ftol': 1e-8})
        weights_opt = res_b.x
        print("Optimal Inital Independent Weights is: ", weights_opt)
        return weights_opt

    def create_inital_independent_weights(self):
        paths = self.calculate_independent_MC_returns(1000)
        for path in paths:
            print(np.mean(path))
        print(type(paths))
        weights_opt = self.optimize_inital_weights(paths.T)
        

        
class Stock_Profile:
    def __init__(self, ticker, start_date, end_date, steps=252):
        self.ticker = ticker
        self.steps = steps

        # Download adjusted close prices
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=True
        )

        # Check if data exists
        if data.empty:
            raise ValueError(f"No data found for {ticker} between {start_date} and {end_date}")

        # Extract 'Close' column as a Series of floats
        if 'Close' in data.columns:
            self.prices = data['Close'].astype(float).squeeze()
        else:
            self.prices = data.iloc[:, 0].astype(float).squeeze()

        # Initialize stock price array
        self.stock_price = np.zeros(steps + 1, dtype=float)
        self.stock_price[0] = self.prices.iloc[-1].item()  # safe scalar float

        # Compute daily log returns
        self.returns = np.log(self.prices / self.prices.shift(1)).dropna()

        # Compute drift and volatility
        self.mu = self.returns.mean()
        self.sigma = self.returns.std()

    def simulate_GBM_path(self):
        for t in range(1, len(self.stock_price)):
            Z = np.random.normal()
            self.stock_price[t] = self.stock_price[t-1] * np.exp(
                (self.mu - 0.5 * self.sigma**2) + self.sigma * Z
            )
        return self.stock_price.copy()



tickers = ["AAPL", "MSFT", "GOOGL", "SPY"]
start_date = "2015-01-01"
end_date = "2023-01-01"

portfolio = Portfolio_Analysis(tickers, start_date, end_date)
portfolio.create_inital_independent_weights()
