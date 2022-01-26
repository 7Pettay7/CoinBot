import discord
from discord.ext import commands

from setup import Configuration as config
from controller import Controller
    
setup = config()
data = Controller(setup.get_secrets())

# Bot config
# ------------------------------------------------------
help_command = commands.DefaultHelpCommand(
    no_category='Commands')

bot = commands.Bot(command_prefix='!',
    help_command=help_command,
    description='CoinBot is used to retrieve cryptocurrency data along with users\' portfolio data.')

class Coinbot:
    """Class to utilize the Discord API to receive commands from user"""

    @bot.command(help='Gets balance of a specific currency in user\'s portfolio. Ex: balance BTC')
    async def balance(ctx, ticker):
        crypto = data.portfolio_data()[ticker]

        embed = discord.Embed(
            title='__**{}:**__'.format(ticker), 
            timestamp=ctx.message.created_at)

        embed.add_field(
            name='Balances:', 
            value='> Dollars: ${:.2f}\n> Units: {:.4f}'.format(
                crypto['dollars'], 
                crypto['units']))

        await ctx.send(embed=embed)

    @bot.command(help='Gets user\'s portfolio data of all owned currencies')
    async def portfolio(ctx):
        portfolio = data.portfolio_data()[0]
        portfolio_total = data.portfolio_data()[1]
        prices = data.current_data()

        embed = discord.Embed(
            title='__**Portfolio:**__')

        for key, val in portfolio.items():
            embed.add_field(
                name='{}'.format(key),
                value='> Dollars: ${:.2f}\n> Units: {:.4f}\n> Sell price: ${}'.format(
                    val['dollars'],
                    val['units'],
                    prices[key]),  
                inline=True)

        embed.add_field(name='__TOTAL__', 
            value='> ${:.2f}'.format(
                portfolio_total
        ))

        await ctx.send(embed=embed)

    @bot.event
    async def on_ready():
        print('Successfully started!')

if __name__ == '__main__':
    bot.run(setup.get_secrets()[3])