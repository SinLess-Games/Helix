import os
import threading

from Helix.bot import Helix


def main():
    bot = Helix()
    for filename in os.listdir('./Helix/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'Helix.cogs.{filename[:-3]}')
    bot.loop.run_until_complete(bot.run())


if __name__ == '__main__':
    threading.Thread(target=main()).start()
