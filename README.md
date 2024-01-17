# option_pricing

## Overview
The OptionPricing class provides a tool for pricing options using Monte Carlo simulation and the Black-Scholes model. It is designed to calculate option prices for both Call and Put options based on various parameters such as the underlying asset's ticker symbol, option expiry date, option type, and strike price.

Dependencies
-datetime
-scipy.stats.norm
-numba
-yfinance
-numpy

## Usage
To use the OptionPricing class, follow these steps:
- Initialize an instance of the OptionPricing class with the required parameters:
  * ticker (str): Ticker symbol of the underlying asset.
  * expiry (str): Expiry date of the option in the format 'YYYY-MM-DD'.
  * opt_type (str): Type of option, either 'Call' or 'Put'.
  * strike (float): Strike price of the option.
