from crypto import Portfolio as folio
from auth import Authorize as auth

class Controller:
    """Controller class used to pass and format data to bot from crypto module"""

    def __init__(self, secrets):
        self.login = folio(secrets)

    def portfolio_data(self):
        balances = self.login.sort_dict(
            self.login.get_balances())
        total = self.login.get_total(balances)
        return [balances, total]

    def current_data(self):
        current_prices = self.login.current_prices(
            self.login.get_balances())
        return current_prices

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