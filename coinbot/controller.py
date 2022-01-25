import json
import requests

from crypto import Portfolio as folio
from auth import Authorize as auth

class Controller:
    """Controller class used to pass and format data to bot from crypto module
    
    TODO: cleanup unneeded self variables"""

    def __init__(self, secrets):
        self.login = folio(secrets)

    def portfolio_data(self):
        self.balances = self.login.sort_dict(
            self.login.get_balances())
        self.total = self.login.get_total(self.balances)
        return [self.balances, self.total]

    def current_data(self):
        self.current_prices = self.login.current_prices(
            self.login.get_balances())
        return self.current_prices

    def historic_data(self):
        balances = self.portfolio_data()[0]
        dates = self.login.get_dates()
        return self.login.historic_prices(balances, dates)

    def percent_change(self):
        current_prices = self.current_data()
        historic_prices = self.historic_data()
        return self.login.percent_change(historic_prices, current_prices)

if __name__ == '__main__':
    print('controller.py is meant to be ran as an imported module.')