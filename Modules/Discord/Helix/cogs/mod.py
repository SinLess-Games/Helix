from datetime import datetime

from discord import Embed
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy.orm import Session

from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import BlackList, Users, Bots


class Mod(commands.Cog):
    """
    This module handles blacklists of servers and moderates channels based on black listed words.
    """

    def __init__(self, bot, config_file=None):
        self.bot = bot
        if config_file is None:
            config_file = ConfigDefaults.Config_file
        self.config = Config(config_file)

    @commands.Cog.listener()
    async def on_message(self, message):
        _roles = []
        for role in message.author.roles:  # Iterates through each roll and adds them to a list
            _roles.append(role.name)
        roles = str(_roles)

        guild_id = message.guild.id
        user_id = message.author.id
        Engine = create_engine(
            f'mysql+pymysql://{self.config.sql_user}:{self.config.sql_passwd}@{self.config.sql_host}/{guild_id}',
            echo=False)
        dm = "coming soon"
        global guild

        if message.author.bot:
            # print("message author is a bot")
            # print(message.author.id)
            # print(self.config.Helix)
            helix = self.config.Helix
            author_id = message.author.id
            if str(author_id) == str(helix):
                # print('Message sent by helix')
                with Session(Engine) as session:
                    bot = Bots()

                    bot_exists = session.query(Bots).filter_by(UserID=self.config.Helix).first()
                    if not bot_exists:
                        bot.UserID = message.author.id
                        bot.DisplayName = message.author.display_name.encode(encoding='UTF-8')
                        bot.Discriminator = message.author.discriminator.encode(encoding='UTF-8')
                        bot.Mention = message.author.mention.encode(encoding='UTF-8')
                        bot.server = message.guild.name.encode(encoding='UTF-8')
                        bot.roles = roles.encode(encoding='UTF-8')
                        bot.DMChannel = dm.encode(encoding='UTF-8')
                        bot.usage = 1
                        bot.LastUpdate = datetime.today()
                        session.add(bot)
                        session.commit()
                        session.close()

                    else:
                        bot = session.query(Bots).filter_by(UserID=message.author.id).first()
                        use = bot.usage + 1
                        # print(use)
                        session.query(Bots).filter_by(UserID=message.author.id).update({
                            "usage": use,
                            "LastUpdate": datetime.today()
                        }, synchronize_session="fetch")
                        session.commit()
                        session.close()

            else:
                pass

        else:
            with Session(Engine) as session:
                guild = session.execute('SELECT word FROM BlackList')
                usr = Users()
                user_exists = session.query(Users).filter_by(UserID=user_id).first()
                if not user_exists:
                    usr.DisplayName = message.author.display_name.encode(encoding='UTF-8')
                    usr.UserID = message.author.id
                    usr.Discriminator = message.author.discriminator.encode(encoding='UTF-8')
                    usr.Mention = message.author.mention.encode(encoding='UTF-8')
                    usr.dm = dm.encode(encoding='UTF-8')
                    usr.roles = roles.encode(encoding='UTF-8')
                    usr.PostCount = 1
                    usr.LastUpdate = datetime.today()
                    session.add(usr)
                    session.commit()
                    session.close()
                else:
                    user = session.query(Users).filter_by(UserID=message.author.id).first()
                    post_count = user.PostCount
                    count = post_count + 1
                    session.query(Users).filter_by(UserID=message.author.id).update({
                        "PostCount": count,
                        "LastUpdate": datetime.today()
                    }, synchronize_session="fetch")
                    session.commit()
                    session.close()

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
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        Engine = create_engine(
            f'mysql+pymysql://{self.config.sql_user}:{self.config.sql_passwd}@{self.config.sql_host}/{guild_id}',
            echo=False)
        with Session(Engine) as session:
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
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        Engine = create_engine(
            f'mysql+pymysql://{self.config.sql_user}:{self.config.sql_passwd}@{self.config.sql_host}/{guild_id}',
            echo=False)
        if to_be_blacklisted is None:
            # print(ctx)
            await ctx.channel.send("You need to specify a word to blacklist")
            return
        with Session(Engine) as session:
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
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        Engine = create_engine(
            f'mysql+pymysql://{self.config.sql_user}:{self.config.sql_passwd}@{self.config.sql_host}/{guild_id}',
            echo=False)
        if word is None:
            return await ctx.send("You need to specify a word to remove from the blacklist")

        with Session(Engine) as session:
            session.qeury(BlackList).filter_by(Word=word).delete(synchronize_session=False)
            session.commit()
            session.close()
        await ctx.send(f'Removed "{word}" from the blacklist', delete_after=23)


def setup(bot):
    bot.add_cog(Mod(bot))
