import discord
from discord.ext import commands
from discord import Member as DiscordMember

Guild = object()


class test(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.text_channel_list = []
        self.mod_color = discord.Colour(0x7289da)  # Blurple
        self.user_color = discord.Colour(0xed791d)  # Orange

    # some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

    @commands.command(name="slap")
    async def slap_member(self, ctx, target: DiscordMember):
        """Slaps a member."""
        await ctx.send(f"**{ctx.author.display_name}** just slapped {target.mention} silly!")
        return

    # +------------------------------------------------------------+
    # |              CLEAN THAT CHAT!                              |
    # +------------------------------------------------------------+
    @commands.command(aliases=['del', 'p', 'prune'], bulk=True, no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def purge(self, ctx, limit: int):
        ''' ᗣ Clean messages from chat '''
        if not limit:
            return await ctx.send('Enter the number of messages you want me to delete.')

        if limit < 99:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            succ = f'₍₍◝(°꒳°)◜₎₎ Successfully deleted {len(deleted)} message(s)'
            await ctx.channel.send(succ, delete_after=6)

        else:
            await ctx.send(f'Cannot delete `{limit}`, try with less than 100.', delete_after=23)

    # +------------------------------------------------------------+
    # |             CLEAN CHAT FROM BOT MESSAGES!                  |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def clean(self, ctx, limit: int = 15):
        """ ᗣ Clean a only Bot's messages """
        if not limit:
            return await ctx.send('Enter the number of messages you want me to delete. ˛˛(⊙﹏⊙ ) ̉ ̉')

        if limit < 99:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author == self.client.user)
            await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=5)

        else:
            await ctx.send(f'Cannot delete `{limit}`, try fewer messages.')


def setup(client):
    client.add_cog(test(client))
