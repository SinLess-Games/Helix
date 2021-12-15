from datetime import datetime

import yaml
from discord import Embed
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy.orm import Session

from Helix.utils.db_tools import BlackList

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless
# having issues with ruamel)
with open("Helix/Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

host = config['SQL_Host']
user = config['SQL_UserName']
passwd = config['SQL_Password']


class Mod(commands.Cog):
    """
    This module handles blacklists of servers and moderates channels based on black listed words.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        db = message.guild.id
        engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{db}', echo=False)
        if message.author.id == 852957689905676368:
            return
        if message.content.startswith("H!"):
            return

        with Session(engine) as session:
            guild = session.execute('SELECT word FROM BlackList')

        blacklist = set()
        for word_tuple in guild.fetchall():  # function fixed by Parados @ stackoverflow
            blacklist.add(word_tuple[0])
        # print(blacklist)

        for word in blacklist:
            if word in message.content.lower():
                await message.delete()
                channel = message.channel
                await channel.send(
                    "Please refrain from using blacklisted words. To find out what words are blacklisted use H!blacklist",
                    delete_after=23)

                return await message.author.send(
                    f'''Your message "{message.content}" was removed for containing the blacklisted word "{word}"''')

    @commands.command(name='blacklist')
    async def blacklist(self, ctx):
        """
        displays the black listed words for a server
        """
        with Session(engine) as session:
            guild = session.execute('SELECT word FROM BlackList')

        blacklist = set()
        for word_tuple in guild.fetchall():  # function fixed by Parados @ stackoverflow
            blacklist.add(word_tuple[0])
        emb = Embed(title="Blacklisted Words", colour=0xe74c3c)
        emb.set_author(name="Helix")
        emb.add_field(name="blacklist", value=f"{blacklist}")
        return await ctx.send(embed=emb)

    @commands.command(name='add')
    async def add_word(self, ctx, *, to_be_blacklisted: str = None):
        """
        Adds a given word to blacklist
        """
        if to_be_blacklisted is None:
            # print(ctx)
            await ctx.channel.send("You need to specify a word to blacklist")
            return
        with Session(engine) as session:
            update_date = datetime.now()
            bl = BlackList()
            bl.Word = to_be_blacklisted
            bl.AddDate = update_date
            session.add(bl)
            session.commit()
            session.close()

        await ctx.send(f'Added "{to_be_blacklisted}" to the blacklist', delete_after=23)

    @commands.command(name="RemoveWord")
    async def remove_word(self, ctx, *, word: str = None):
        """
        Removes a word from blacklist
        """
        if word is None:
            return await ctx.send("You need to specify a word to remove from the blacklist")

        with Session(engine) as session:
            session.qeury(BlackList).filter_by(Word=word).delete(synchronize_session=False)
            session.commit()
            session.close()
        await ctx.send(f'Removed "{word}" from the blacklist', delete_after=23)


def setup(bot):
    bot.add_cog(Mod(bot))
