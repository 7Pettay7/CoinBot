# __CoinBot__

CoinBot is a Discord bot that can retreive your Coinbase portfolio information via a created API key and relay the data to a Discord server via commands or on scheduled times.

## __Dependencies__

Make sure to have these installed:

 - [Coinbase Package](https://developers.coinbase.com/api/v2#introduction)
 - [Historic_Crypto](https://github.com/David-Woroniuk/Historic_Crypto)
 - [Pandas](https://pypi.org/project/pandas/)

## __Setup__

 1. Generate Coinbase API key and secret by going to [your Coinbase settings](https://www.coinbase.com/settings/api)
 2. Create Discord bot and link to server with [this guide](https://discordpy.readthedocs.io/en/stable/discord.html)
 3. Configure `config-TEMPLATE.json` file and rename to `config.json`
 4. Run bot file

## __Using the bot__

All Discord commands should be prefixed with the specified command prefix; the default prefix is `!`. Commands and uses with table:

| Command | Explanation | Example |
| ------------- | ------------- | ------------- |
| `balance` | get balance for specific currency | `balance BTC` |
| `portfolio` | grab all of user's portfolio currencies and output them | `portfolio` |

## Roadmap

 1. Features
    - [X] Grab user's portfolio information
    - [X] Grab current and historic currency data
    - [X] Update data with each request instead of at the start of the app
    - [X] Calculate precent change of cryptocurrencies based on historic data
    - [] Optimize fetching of historical data (can take a min)
    - [] Integrate matplotlib for visual aids
    - [] Connect database to store portfolio information so the user can see their portfolio growth over time
    - [] Discord Bot
      - [X] Total portfolio output
      - [] Output specific currency info \(price, percent up/down, amount owned and total)
      - [] Use [Discord buttons](https://discordpy-message-components.readthedocs.io/en/latest/index.html) feature to implement pagination on embed of portfolio information (change page to percent up/downs)
      - [] Output data if date and time matches alert config (see [Discord Tasks](https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html))
      - [] Command to edit JSON file to update alerts \(day and time)
      - [] Get list of currencies from watchlist in config file and output pricing info
      - [] Handling for arguments that cannot be resolved
      - [] Flesh out help command

 2. Config
    - [X] Create JSON template files to grab config info from
    - [X] Flesh out setup.py to grab other general config info, such as watchlist, command prefix, etc
    - [] Config options 
      - [X] API key/secret
      - [X] Currency limit
      - [X] Discord bot token
      - [X] Alert days and times
      - [X] Changeable command prefix
      - [X] Add watchlist option where users can add currencies for pricing updates
      - [] Option to opt out of linking Coinbase account (i.e. just retrieve pricing data)
      
 3. Admin
    - [X] Select license
    - [] Improve setup guide to explain some of the configuration options in `config-TEMPLATE.json`

## License

See the LICENSE.md file for license rights and limitations (MIT).