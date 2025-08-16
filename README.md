# Monte Carlo Portfolio Simulation based on Historical Data

This project provides a Python-based Monte Carlo simulation framework to analyze stock portfolios using historical data. It simulates Geometric Brownian Motion (GBM) paths for individual stocks, calculates expected returns, and optimizes portfolio weights to maximize the Sharpe ratio with diversification constraints.

---

## Features

- Download historical stock price data using `yfinance`.
- Calculate daily log returns, drift, and volatility for each stock.
- Simulate multiple Monte Carlo paths using Geometric Brownian Motion (GBM).
- Compute final portfolio returns from simulated paths.
- Optimize initial portfolio weights to maximize Sharpe ratio while penalizing concentration.
- Supports multiple stocks and custom date ranges.

---

## Requirements

- Python 3.8+
- Libraries:
  - `yfinance`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `scipy`
 
```bash
pip install yfinance pandas numpy matplotlib scipy
```


## Usage

1. **Define your portfolio tickers and date range:**

```python
tickers = ["AAPL", "MSFT", "GOOGL", "SPY"]
start_date = "2015-01-01"
end_date = "2023-01-01"
```

2. Initialize the portfolio analysis:
   ```python
   portfolio = Portfolio_Analysis(tickers, start_date, end_date)
   ```
3. Generate Monte Carlo simulations and optimize initial weights:
   ```python
   portfolio.create_inital_independent_weights()
   ```

## How it works

# Stock_Profile Class
- Downloads historical stock prices.
- Calculates daily log returns, mean (mu), and standard deviation (sigma).
- Simulates GBM paths using:
  $S_{t+1} = S_t \cdot exp((\mu-0.5\sigma^2)+\sigma Z)$

Where $Z\sim \mathbb{N}(0,1)$ 
