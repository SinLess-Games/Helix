import os

from Helix.bot import Helix
from Helix.flask import run_flask, stop_flask


def run():
    bot = Helix()
    for filename in os.listdir('./Helix/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'Helix.cogs.{filename[:-3]}')
    bot.run()
    run_flask()


if __name__ == '__main__':
    run()
