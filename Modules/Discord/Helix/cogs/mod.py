import mysql.connector

from discord import Embed
from discord.ext import commands
from mysql.connector import errorcode
from datetime import datetime


class Mod(commands.Cog):
    """
    This module handles blacklists of servers and moderates channels based on black listed words.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 852957689905676368:
            return
        if message.content.startswith("H!"):
            return
        global cnx
        global cursor
        msg = message.content
        try:
            cnx = mysql.connector.connect(
                host='192.168.86.78',
                user='Admin',
                password='Shellshocker93!',
                database=f"{message.guild.id}"
            )
            # exception occurred
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f'\033[1;31m Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'\033[1;31m Database does not exist')
            else:
                print(f'\033[1;31m {err}')
        if cnx.is_connected():
            # print(f'Message Recieved.\n " {msg} " \n')
            cursor = cnx.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print(f'\033[1;32m You\'re connected to database: \033[3;34m', record)
        cursor.execute('SELECT word FROM blacklist')
        blacklist = set()
        for word_tuple in cursor.fetchall():  # function fixed by Parados @ stackoverflow
            blacklist.add(word_tuple[0])
        # print(blacklist)

        for word in blacklist:
            if word in message.content.lower():
                await message.delete()
                channel = message.channel
                await channel.send(
                    "Please refrain from using blacklisted words. To find out what words are blacklisted use H!blacklist", delete_after=23)

                return await message.author.send(
                    f'''Your message "{message.content}" was removed for containing the blacklisted word "{word}"''')
        cnx.close()

    @commands.command(name='blacklist')
    async def blacklist(self, ctx):
        """
        displays the black listed words for a server
        """
        global cnx
        global cursor
        try:
            cnx = mysql.connector.connect(
                host='192.168.86.78',
                user='Admin',
                password='Shellshocker93!',
                database=f"{ctx.guild.id}"
            )
            # exception occurred
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f'\033[1;31m Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'\033[1;31m Database does not exist')
            else:
                print(f'\033[1;31m {err}')
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print(f'\033[1;32m You\'re connected to database: \033[3;34m', record)
        cursor.execute('SELECT word FROM blacklist')
        blacklist = set()
        for word_tuple in cursor.fetchall():  # function fixed by Parados @ stackoverflow
            blacklist.add(word_tuple[0])
        emb = Embed(title="Blacklisted Words", colour=0xe74c3c)
        emb.set_author(name="Helix")
        emb.add_field(name="blacklist", value=f"{blacklist}")
        return await ctx.send(embed=emb)
        cnx.close()

    @commands.command(name='add')
    async def add_word(self, ctx, *, to_be_blacklisted: str = None):
        """
        Adds a given word to blacklist
        """
        if to_be_blacklisted is None:
            # print(ctx)
            await ctx.channel.send("You need to specify a word to blacklist")
            return
        global cnx
        global cursor
        try:
            cnx = mysql.connector.connect(
                host='192.168.86.78',
                user='Admin',
                password='Shellshocker93!',
                database=f"{ctx.guild.id}"
            )
            # exception occurred
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f'\033[1;31m Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'\033[1;31m Database does not exist')
            else:
                print(f'\033[1;31m {err}')
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print(f'\033[1;32m You\'re connected to database: \033[3;34m', record)
        update_date = datetime.now()
        add_word = ("INSERT INTO blacklist"
                    "(word, Last_Update)"
                    "VALUES (%s, %s)"
                    )
        data_word = (to_be_blacklisted, update_date)
        cursor.execute(add_word, data_word)
        cnx.commit()
        await ctx.send(f'Added "{to_be_blacklisted}" to the blacklist', delete_after=23)

        cnx.close()

    @commands.command(name="RemoveWord")
    async def remove_word(self, ctx, *, word: str = None):
        """
        Removes a word from blacklist
        """
        if word is None:
            return await ctx.send("You need to specify a word to remove from the blacklist")

        global cnx
        global cursor
        try:
            cnx = mysql.connector.connect(
                host='192.168.86.78',
                user='Admin',
                password='Shellshocker93!',
                database=f"{ctx.guild.id}"
            )
            # exception occurred
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f'\033[1;31m Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'\033[1;31m Database does not exist')
            else:
                print(f'\033[1;31m {err}')
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print(f'\033[1;32m You\'re connected to database: \033[3;34m', record)
        words = word
        cursor.execute(f'''DELETE FROM blacklist WHERE word = "{words}"''')
        cnx.commit()
        await ctx.send(f'Removed "{word}" from the blacklist', delete_after=23)


def setup(bot):
    bot.add_cog(Mod(bot))
