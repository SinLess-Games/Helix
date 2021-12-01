from discord.ext import commands


class events(commands.Cog):
    """
    Event handlers for Helix
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\033[1;32m Bot is ready! DEUS VULT!')

    @commands.Cog.listener()
    async def on_error(self):
        print(f'\033[1;31m Raised an exception')


def setup(bot):
    bot.add_cog(events(bot))
