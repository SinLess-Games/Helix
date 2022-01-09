import logging

import discord
from discord.errors import Forbidden
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy.orm import Session

from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import ServerList

logger = logging.getLogger(__name__)

"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
Original concept by Jared Newsom (AKA Jared M.F.)
[Deleted] https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b
Rewritten and optimized by github.com/nonchris
https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2
You need to set three variables to make that cog run.
Have a look at line 51 to 57
"""


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot, config_file=None):
        self.bot = bot
        if config_file is None:
            config_file = ConfigDefaults.Config_file
        self.config = Config(config_file)

    def _gen_embed(self):
        """Provides a basic template for embeds"""
        e = discord.Embed()
        e.colour = 7506394
        e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                     icon_url='https://imgur.com/a/wdNvSfZ')
        e.set_author(name=self.bot.user.name, url='https://github.com/sinLess-Games/Helix',
                     icon_url=self.bot.user.avatar_url)
        return e

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """
        Shows all modules of that bot
        """

        # !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
        version = self.config.version
        host = self.config.sql_host
        user = self.config.sql_user
        passwd = self.config.sql_passwd
        db = self.config.sql_ddb
        Engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{db}', echo=False)
        with Session(Engine) as session:
            GuildData = session.query(ServerList).filter_by(ServerID=ctx.guild.id).first()
        # print(GuildData)

        prefix = GuildData.Prefix
        # print(f"prefix is {prefix}")

        # setting owner name - if you don't want to be mentioned remove line 49-60 and adjust help text (line 88)
        owner = self.config.owner
        owner_id = self.config.owner_id

        valid_user = False

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # print('No input detected')
            emb = self._gen_embed()

            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value="Below are the modules within HeliX", inline=False)

            cogs_inline = ""
            # iterating trough cogs, gathering descriptions
            for cog in self.bot.cogs:
                cogs_inline = emb.add_field(name=f'`{cog}`', value=f'{self.bot.cogs[cog].__doc__} \n')

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # setting information about author
            emb.add_field(name="About", value=f"Helix is developed by {owner} \n\
                                    This version of Helix is maintained by {owner}\n\
                                    Please visit https://github.com/SinLess-Games/Helix to submit ideas or bugs.")
            emb.set_footer(text=f"Bot is running on Version: {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=discord.Color.orange())

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                            "Would you please be so kind to report that issue to me on github?\n"
                                            "https://github.com/SinLess-Games/Helix \n"
                                            "Thank you! ~Tim",
                                color=discord.Color.red())

        # sending reply embed using our own function defined above
        # print('sending embed')
        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(Help(bot))
