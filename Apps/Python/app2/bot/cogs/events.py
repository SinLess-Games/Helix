from discord.ext import commands


class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\033[1;32m Bot is ready! DEUS VULT!')

    @commands.Cog.listener()
    async def on_error(self):
        print(f'\033[1;31m Raised an exception')


def setup(client):
    client.add_cog(events(client))
