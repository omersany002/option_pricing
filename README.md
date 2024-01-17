# option_pricing

Overview
The OptionPricing class provides a tool for pricing options using Monte Carlo simulation and the Black-Scholes model. It is designed to calculate option prices for both Call and Put options based on various parameters such as the underlying asset's ticker symbol, option expiry date, option type, and strike price.

Dependencies
datetime
scipy.stats.norm
numba
yfinance
numpy
Usage
To use the OptionPricing class, follow these steps:

Initialize an instance of the OptionPricing class with the required parameters:

python
Copy code
google = OptionPricing('GOOGL', '2024-03-15', 'Call', 110)
Run the main function to obtain option prices using Monte Carlo simulation and the Black-Scholes model:

python
Copy code
google.main()
Written by
Omer Sany Prakash
Graduate Student
Department of Finance
Oklahoma State University
Email: omer.prakash@okstate.edu

Parameters
ticker (str): Ticker symbol of the underlying asset.
expiry (str): Expiry date of the option in the format 'YYYY-MM-DD'.
opt_type (str): Type of option, either 'Call' or 'Put'.
strike (float): Strike price of the option.
Functions
_mkt_price()
Description: Finds the underlying market price.
Output: Market price of the option.
_stock_info()
Description: Calculates the spot price and sigma (volatility).
Output: Spot price and sigma.
geometric_path(rf, s0, sigma, t, t_steps)
Description: Generates a path of prices over time using the geometric random walk model.
Parameters:
rf (float): Risk-free rate.
s0 (float): Initial stock price.
sigma (float): Volatility of the stock.
t (float): Time period.
t_steps (int): Number of time steps.
Output: List of price path.
_mc_simulation()
Description: Runs simulations to find final prices using Monte Carlo simulation.
Output: List of final prices.
_mc_option_payoffs()
Description: Calculates payoffs from options based on the final prices.
Output: Mean payoff.
mc_call_prc()
Description: Calculates the price of a call option using Monte Carlo simulation.
black_sholes_price()
Description: Calculates option price using the Black-Scholes model.
main()
Description: Reports the option pricing using market price, Monte Carlo simulation, and Black-Scholes model.
Example
python
Copy code
# Creating an instance and running the functions
google = OptionPricing('GOOGL', '2024-03-15', 'Call', 110)
google.main()
Note: Ensure that the required dependencies are installed before using the OptionPricing class.
