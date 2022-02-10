from distutils.command.config import config
import os
import json

class ConfigFileNotAlteredError(Exception):
    def __init__(self, value):
        self.value = value

class Configuration:
    """Class to get configuration information from config.json and pass it to other files"""

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def load_json(self):
        """Loads JSON data from config.json
        
        Parameters:
        none"""
        try:
            file_path = self.current_dir + '/config.json'
            with open(file_path, 'r') as f:
                config = json.load(f)

        except FileNotFoundError:
            print('\nCould not find config.json, please ensure you have renamed the JSON file to "config.json"\n')
            raise FileNotFoundError

        return config

    def get_secrets(self):
        """Get API key and secret for Coinbase account access, reads JSON file from user environment.

        TODO: if API key/secret are unaltered, that should signify that the user does not want
            to connect to their coinbase account. Should be able to then only retrieve data that
            does not require a coinbase account

        Parameters:
        none"""
        secrets = self.load_json()

        API_KEY = secrets['portfolio']['API_key']
        API_SECRET = secrets['portfolio']['API_secret']
        ACCOUNT_LIMIT = secrets['portfolio']['account_limit']
        DISCORD_TOKEN = secrets['config']['discord_token']
        
        if API_KEY == 'your_api_key' or API_SECRET == 'your_api_secret' or DISCORD_TOKEN == 'your_discord_token':
            raise ConfigFileNotAlteredError('API key, secret, or discord bot token have not been changed from default values in file "config.json"')
    
        return [API_KEY, API_SECRET, ACCOUNT_LIMIT, DISCORD_TOKEN]

    def config_options(self):
        """Gets all unsensitive configuration options from config.json

        TODO: load watchlist feature
        
        Parameters:
        none"""
        config = self.load_json()['config']

        command_prefix = config['command_prefix']
        alerts = config['alerts']
        watchlist = config['watchlist']
        return [command_prefix, alerts, watchlist]

class WriteConfiguration(Configuration):
    """Class to write to the config.json file for customization of the config options while using the bot"""

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))

    def write_watchlist(self, *args):
        """Function that is able to write data to the 'watchlist'
        item within the config.json file and returns a status code.

        Status codes:
        0 - Failed to find config file to write to
        1 - Success
        
        Parameters:
        *args - takes string arguments of currencies' ticker
        
        TODO: validation of ticker formatting and type (make sure it's a string)"""
        status_code = 0
        data = super().load_json()

        for arg in args:
            data['config']['watchlist'].append(arg)

        config_path = os.path.join(self.current_dir, 'config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=4)
            status_code = 1
        except FileNotFoundError:
            print(f'Writing data to watchlist failed...\nStatus code: {status_code}')

        return status_code

if __name__ == '__main__':
    print('auth.py is meant to run as an imported module.')