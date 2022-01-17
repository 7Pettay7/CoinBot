# (MVC design) Use controller to get data and pass it in order of crypto.py -> controller.py -> bot.py

import json
import requests

from crypto import Portfolio as folio
from auth import Authorize as auth

class Controller:
    """Controller class used to pass and format data to bot from crypto module"""

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
        raise NotImplementedError

    def calculate_updown(self):
        raise NotImplementedError

if __name__ == '__main__':
    print('controller.py is meant to be ran as an imported module.')
