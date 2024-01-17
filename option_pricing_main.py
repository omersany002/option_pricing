"""
OptionPricing class for pricing options using Monte Carlo simulation and Black-Scholes model.

Dependencies:
- datetime
- scipy.stats.norm
- numba
- yfinance
- numpy

Usage:
google = OptionPricing('GOOGL', '2024-03-15', 'Call', 110)
google.main()

Written by:
Omer Sany Prakash
Graduate Student
Department of Finance
Oklahoma State University
email: omer.prakash@okstate.edu

"""

from datetime import datetime
from scipy.stats import norm
from numba import jit
import yfinance as yf
import numpy as np

class OptionPricing:
    """Option Pricing Formulas Class"""

    def __init__(self, ticker, expiry, opt_type, strike):
        """
        Initialize OptionPricing instance.

        Parameters:
        - ticker (str): Ticker symbol of the underlying asset.
        - expiry (str): Expiry date of the option in the format 'YYYY-MM-DD'.
        - opt_type (str): Type of option, either 'Call' or 'Put'.
        - strike (float): Strike price of the option.
        """
        self.underlying = ticker
        self.expiry = expiry
        self.opt_type = opt_type
        self.strike = strike
        self.steps = 500
        self.sims = 100_000
        self.capt = (datetime.strptime(self.expiry, "%Y-%m-%d") - datetime.today()).days / 365
        self.rf = yf.Ticker('^IRX').history('5d').Close.iloc[-1] / 100
        self.spot, self.sigma = self._stock_info()

    def _mkt_price(self):
        """A function to find out the underlying market price."""
        options = yf.Ticker(self.underlying).option_chain(self.expiry)
        calls, puts = options[0], options[1]
        if self.opt_type == 'Call':
            return calls.loc[calls.strike == self.strike, 'lastPrice'].iloc[0]
        if self.opt_type == 'Put':
            return puts.loc[puts.strike == self.strike, 'lastPrice'].iloc[0]
        return "Unrecognized option. Input 'Call' or 'Put'."

    def _stock_info(self):
        """Calculates spot price and sigma."""
        df = yf.Ticker(self.underlying).history('1y').Close
        sigma = (df.pct_change().std()) * (np.sqrt(252))
        return df.iloc[-1], sigma

    @staticmethod
    @jit(nopython=True)
    def geometric_path(rf, s0, sigma, t, t_steps):
        """
        Generate a path of prices over t_steps time steps using the geometric random walk model.

        Parameters:
        - rf (float): Risk-free rate.
        - s0 (float): Initial stock price.
        - sigma (float): Volatility of the stock.
        - t (float): Time period.
        - t_steps (int): Number of time steps.

        Returns:
        - List[float]: Price path.
        """
        price_path = [s0]
        for _ in range(t_steps):
            s_t = s0 * np.exp((rf - 0.5 * sigma**2) * t + sigma * np.sqrt(t) * np.random.randn())
            price_path.append(s_t)
            s0 = s_t
        return price_path

    def _mc_simulation(self):
        """Runs simulations to find final prices."""
        interval = self.capt / self.steps
        final_prices = []
        for _ in range(self.sims):
            prices = self.geometric_path(self.rf, self.spot, self.sigma, interval, self.steps)
            final_prices.append(prices[-1])
        return final_prices

    def _mc_option_payoffs(self):
        """Calculates payoffs from options."""
        final_prices = self._mc_simulation()
        if self.opt_type == 'Call':
            payoffs = np.maximum(np.array(final_prices) - self.strike, 0)
            return np.mean(payoffs)
        if self.opt_type == 'Put':
            payoffs = np.maximum(self.strike - np.array(final_prices), 0)
            return np.mean(payoffs)
        return "Unrecognized option. Input 'Call' or 'Put'"

    def mc_call_prc(self):
        """Calculates the price of a call option."""
        avg_payoff = self._mc_option_payoffs()
        price = avg_payoff * np.exp((self.rf * -1) * self.capt)
        print(f'Monte Carlo Simulation: {price.item():.2f}')

    def black_sholes_price(self):
        """Calculates option price using Black-Scholes model."""
        d1 = (np.log(self.spot / self.strike) +
              (self.rf + self.sigma**2 / 2) * self.capt) / (self.sigma * np.sqrt(self.capt))
        d2 = d1 - self.sigma * np.sqrt(self.capt)
        if self.opt_type == "Call":
            price = self.spot * norm.cdf(d1) - self.strike * \
                np.exp((-1 * self.rf) * self.capt) * norm.cdf(d2)
        elif self.opt_type == "Put":
            price = self.strike * np.exp((-1 * self.rf) * self.capt) * \
                norm.cdf(-d2) - self.spot * norm.cdf(-d1)
        else:
            price = "Option type not recognized. Please use 'Call' or 'Put'."

        print(f'Black and Sholes Model: {price.item():.2f}')

    def main(self):
        """Reports the three different prices."""
        print('Option Pricing:')
        print(f'Option Type: {self.opt_type} | Strike Price: {self.strike}')
        print(f'Option name: {self.underlying} | Spot Price: {self.spot:.2f}')
        print(f'Market Price: {self._mkt_price():.2f}')
        self.mc_call_prc()
        self.black_sholes_price()

# Creating an instance and running the functions
google = OptionPricing('GOOGL', '2024-03-15', 'Call', 110)
google.main()
