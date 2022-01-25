from coinbase.wallet.client import Client
from Historic_Crypto import HistoricalData
from Historic_Crypto import LiveCryptoData
from datetime import datetime, timedelta

from auth import Authorize as auth

class Portfolio:
    """Get user's Coinbase portfolio data by using the base Coinbase API via API key. The Coinbase API documentation can be found here: https://developers.coinbase.com/api/v2#introduction
     
        Is able to retrieve total portfolio value, each cryptocurrency owned and its value.
    
        TODO: what happens if client cannot be authorized?
        """

    def __init__(self, secrets):
        self.__client = Client(secrets[0], secrets[1])
        self.accounts = self.__client.get_accounts(limit=secrets[2])

    # Portfolio reports
    # ------------------------------------------------------
    def get_balances(self):
        """Get owned crptocurrencies and amounts, returns dictionary in format of:
        {
            'CRYPTO': {
                'units': 0, 
                'dollars': 0
            }
        }
        Parameters:
        none"""
        balances = { }
        for wallet in self.accounts.data:

            currency_ticker = str(
                wallet.balance.currency)
            amount_owned = float(
                wallet.balance.amount)
            worth = float(
                wallet.native_balance.amount)

            if amount_owned > 0:
                balances[currency_ticker] = dict(
                    units=amount_owned, 
                    dollars=worth)
            else:
                continue

        return balances

    def get_total(self, crypto):
        """Get the total dollar amount for the user's portfolio
        Parameters:
        crypto - a dictionary in the format of {'CRYPTO': {'units': int, 'dollars': int}}"""
        total = 0
        for value in crypto.values():
            total += value['dollars']

        return total

    # Pricing reports
    # ------------------------------------------------------
    def current_prices(self, crypto):
        """Gets current prices of crypto and returns a new dict of the user's owned currencies with their current sell prices
        
        Parameters:
        crypto - a dictionary in the format of {'CRYPTO': {'units': int, 'dollars': int}}"""
        current_prices = { }
        for key in crypto:
            current_price = LiveCryptoData(key + '-USD', verbose=False).return_data()
            current_prices[key] = float(current_price.price[0])
        return current_prices

    def get_dates(self):
        """Grabs current date to be able to calculate previous crytocurrency prices from a day, a week, a month, and three months before. These intervals are hardcoded due to some inconsistencies that were found within Historic_Crypto's results when going back further.

        Parameters:
        none
        """
        today = datetime.now()
        days = 1
        dates = [ ]

        # Historic_Crypto requires a specific date format of YYYY-MM-DD-HH-MM
        # can get correct format using %Y-%m-%d and concatenating '-00-00'
        for i in range(4):
            t = today - timedelta(days=days)
            t = t.strftime('%Y-%m-%d')
            t += '-00-00'
            dates.append(t)

            if i < 1:
                days = 7
            elif i < 2:
                days = 30
            elif i < 3:
                days = 90

        return dates

    def historic_prices(self, crypto, dates):
        """Gets closing sell price of owned cryptocurrencies from four time intervals and returns dict in the format of:   

        {
            'CRYPTO': {
                'yesterday': int,
                'one_week': int,
                'one_month': int,
                'three_months': int
                }
            }
        }

        NOTE: With the Historic Crytpto library using the Coinbase Pro API to retreive data, some older data is not available. So, the furthest back the data will go is currently 3 months

        Parameters:
        crypto - a dictionary in the format of {'CRYPTO': {'units': int, 'dollars': int}}
        dates - a list containing dates to grab historical pricing data from, reads in the order of [current price, yesterday, one week, one month, three months]

        TODO: optimize the speed of this by having it only grab historical prices and not current prices as well
        """

        historic_prices = { }
        for key in crypto:
            ticker_currency = key + '-USD'

            for index, day in enumerate(dates):
                try:
                    if index < 1:
                        older_data = HistoricalData(
                            ticker_currency, 
                            86400, 
                            day, 
                            verbose=False).retrieve_data()
                    
                    else:
                        day_after = datetime.now().strptime(day[:10],
                            '%Y-%m-%d') + timedelta(days=1)
                        day_after = day_after.strftime('%Y-%m-%d') + '-00-00'

                        older_data = HistoricalData(
                            ticker_currency, 
                            86400, 
                            day, 
                            day_after, 
                            verbose=False).retrieve_data()

                    older_data = float(older_data.close[0])
                    #print(older_data)

                    if index < 1:
                        historic_prices[key] = dict()
                        historic_prices[key]['yesterday'] = older_data
                    elif index < 2:
                        historic_prices[key]['one_week'] = older_data
                    elif index < 3:
                        historic_prices[key]['one_month'] = older_data
                    elif index < 4:
                        historic_prices[key]['three_months'] = older_data

                except:
                    print('Could not retreive data for {} at date {}'.format(key, day))

        return historic_prices

    def percent_change(self, historic_prices, current_prices):
        """Calculates percent change of a cryptocurrency based on their past prices
        
        Parameters:
        historic_prices - a dictionary in the format of {
            'CRYPTO': {
                'yesterday': int,
                'one_week': int,
                'one_month': int,
                'three_months': int }}
        current_prices - a dictionary in the format of {'CRYPTO': int }"""
        percent_up = lambda old_price, new_price: (
            (new_price - old_price) / old_price) * 100
        
        percent_down = lambda old_price, new_price: (
            (old_price - new_price) / old_price) * 100

        percent_changes = { }
        for key, value in historic_prices.items():
            percent_changes[key] = list()
            current_price = current_prices[key]
            up_or_down = lambda old_price: current_price > old_price

            for old_price in value.values():
                if up_or_down(old_price):
                    up = percent_up(old_price, current_price)
                    percent_changes[key].append('+{:.2f}%'.format(up))
                elif not up_or_down(old_price):
                    down = percent_down(old_price, current_price)
                    percent_changes[key].append('-{:.2f}%'.format(down))
        
        return percent_changes

    # Formatting
    # ------------------------------------------------------
    def sort_dict(self, crypto):
        """Sort cryptocurrency dictionary from highest dollar amount to lowest
        Parameters: 
        crypto - a dictionary in the format of {'CRYPTO': {'units': int, 'dollars': int}}"""
        most_to_least = sorted([i['dollars'] for i in crypto.values()], reverse=True)
        sorted_dict = { }

        for item in most_to_least:
            for key, value in crypto.items():
                if value['dollars'] == item:
                    sorted_dict[key] = value
                else:
                    continue
        
        return sorted_dict

    def __str__(self):
        crypto = self.sort_dict(
            self.get_price_data(
                self.get_balances(), 
                self.get_dates()))
        for key, value in crypto.items():
            print('{}: ${:.2f} | ${:.2f}'.format(
                key, 
                value['dollars'], 
                value['historical_data']['current_price']))
        return 'Total: ${:.2f}'.format(self.get_total(crypto))

if __name__ == '__main__':
    print('crypto.py is meant to be run as an imported module')