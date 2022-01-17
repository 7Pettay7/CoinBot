import os
import getpass
import json

class ConfigFileNotAlteredError(Exception):
    def __init__(self, value):
        self.value = value

class Authorize:
    """TODO: seperate actions by sensitive info and configuration options (i.e. create another class for config options)"""

    def get_secrets():
        """Get API key and secret for Coinbase account access, reads JSON file from user environment.

        Parameters:
        none
        """
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            secrets_file = current_dir + '/config.json'

            with open(secrets_file, 'r') as f:
                config = json.load(f)
            
            API_KEY = config['portfolio']['API_key']
            API_SECRET = config['portfolio']['API_secret']
            ACCOUNT_LIMIT = config['portfolio']['account_limit']
            DISCORD_TOKEN = config['config']['discord_token']
            
            if API_KEY == 'your_api_key' or API_SECRET == 'your_api_secret' or DISCORD_TOKEN == 'your_discord_token':
                raise ConfigFileNotAlteredError('API key, secret, or discord bot token have not been changed from default values in file "config.json"')
        
            return [API_KEY, API_SECRET, ACCOUNT_LIMIT, DISCORD_TOKEN]

        except FileNotFoundError as error:
            print(error)
            print('Please ensure you have renamed the JSON file to "config.json"')
        

if __name__ == '__main__':
    print('auth.py is meant to run as an imported module.')