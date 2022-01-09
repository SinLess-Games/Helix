import discord
from discord.ext import commands
from discord.ext.commands import Cog

Guild = object()


class test(Cog):
    """
    Useful and fun commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.text_channel_list = []
        self.mod_color = discord.Colour(0x7289da)  # Blurple
        self.user_color = discord.Colour(0xed791d)  # Orange

    # +------------------------------------------------------------+
    # |              CLEAN THAT CHAT!                              |
    # +------------------------------------------------------------+
    @commands.command(aliases=['del', 'p', 'prune'], bulk=True, no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def purge(self, ctx, limit: int = 10):
        ''' ᗣ Clean messages from chat '''
        if not limit:
            return await ctx.send('Enter the number of messages you want me to delete.')

        if limit < 201:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            succ = f'₍₍◝(°꒳°)◜₎₎ Successfully deleted {len(deleted)} message(s)'
            await ctx.channel.send(succ, delete_after=6)

        else:
            await ctx.send(f'Cannot delete `{limit}`, try with less than 200.', delete_after=23)

    # +------------------------------------------------------------+
    # |             CLEAN CHAT FROM BOT MESSAGES!                  |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def clean(self, ctx, limit: int = 15):
        """ ᗣ Clean a only Bot's messages """
        if not limit:
            return await ctx.send('Enter the number of messages you want me to delete. ˛˛(⊙﹏⊙ ) ̉ ̉')

        if limit < 200:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author == self.bot.user)
            await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=5)

        else:
            await ctx.send(f'Cannot delete `{limit}`, try fewer messages.')


def setup(bot):
    bot.add_cog(test(bot))
