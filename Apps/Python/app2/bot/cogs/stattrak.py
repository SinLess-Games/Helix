import logging
import discord
import datetime
import random
import traceback
import psutil
import os
import json
import mysql.connector
import re



from discord.ext import commands
from collections import Counter
from io import BytesIO


dt_format = '%Y-%m-%d %H:%M:%S'

uniques = [

]
legendaries = [

]


class StatTrak(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = mysql.connector.connect(host='192.168.86.41', user='admin', password='Shellshocker93!')
        self.c = self.conn.cursor()

    def fix_member(self, member):
        roles = ','.join([str(x.id)
                          for x in member.roles if x.name != "@everyone"])
        names = member.display_name
        self.c.execute('''INSERT OR IGNORE INTO users
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (roles, str(member.guild.id), None, member.id, names, 0, 0, 0))
        self.conn.commit()

    def fix_postcount(self, message):
        if message.guild is None:
            return
        self.c.execute('UPDATE users SET postcount = postcount + 1 WHERE (id=? AND server=?)',
                       (message.author.id, message.guild.id))
        self.conn.commit()

        # @commands.group(pass_context=True, invoke_without_command=True)

    # async def agraph(self, ctx, member : discord.Member = None):
    #     user = ctx.message.author if member is None else member
    #     a = self.c.execute('''SELECT COUNT(id), strftime("%H", timestamp) AS cnt FROM messages WHERE server=207943928018632705 GROUP BY strftime("%H", timestamp) ORDER BY strftime("%H", timestamp) ASC;''')
    #     a = a.fetchall()
    #     x_axis = [x for x in range(25)]
    #     y_axis = [x[0] for x in a]
    #     y_axis.insert(2, 0)
    #     plt.figure()
    #     x = plt.plot(x_axis, y_axis)
    #     plt.setp(x, linewidth=1)
    #     plt.xlabel('Day of the year')
    #     plt.ylabel('messages posted')
    #     plt.title("Global activity")
    #     buf = BytesIO()
    #     plt.savefig(buf, format='png', dpi=1000)
    #     buf.seek(0)
    #     xd = discord.File(fp=buf, filename="suckmydick.png")
    #     await ctx.send(file=xd)

    @commands.group(name="postcount", aliases=['pc'], invoke_without_command=True)
    async def pc(self, ctx, member: discord.Member = None):
        user = ctx.author if member is None else member
        self.c.execute('SELECT postcount FROM users WHERE (server=? AND id=?)', (ctx.guild.id, user.id))
        try:
            a = self.c.fetchone()[0]
        except TypeError:
            self.fix_member(ctx.author)
            return await ctx.send("**{}** has posted **0** messages.".format(user.name))
        else:
            await ctx.send("**{}** has posted **{}** messages.".format(user.name, a))

    @pc.command(name="top", pass_context=True)
    async def postcounttop(self, ctx):
        a = self.c.execute(
            'SELECT * FROM users WHERE (server=? AND postcount > 0) ORDER BY postcount DESC LIMIT 20', (ctx.guild.id,))
        a = a.fetchall()
        b = self.c.execute(
            'SELECT SUM(postcount) AS "hello" FROM users WHERE (server=? AND postcount > 0)', (ctx.guild.id,))
        b = b.fetchone()[0]
        post_this = ""
        rank = 1
        for row in a:
            name = f'<@{row[3]}>'
            post_this += ("{}. {} : {}\n".format(rank, name, row[5]))
            rank += 1
        post_this += "\n**{0}** posts by **{1}** chatters.".format(
            b, len([x for x in ctx.guild.members]))
        em = discord.Embed(title="Current standings:",
                           description=post_this, colour=0x14e818)
        em.set_author(name=self.bot.user.name,
                      icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=em)

    async def on_member_join(self, member):
        a = self.c.execute(
            'SELECT * FROM users WHERE (id=? AND server=?)', (member.id, member.guild.id))
        a = a.fetchall()
        if a != []:
            return
        roles = ','.join([str(x.id) for x in member.roles if (
                x.name != "@everyone")])
        self.c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (roles, member.guild.id, None, member.id, member.display_name, 0, 0, 0))
        self.conn.commit()
        # xd = self.c.execute(
        #     'SELECT * FROM userconfig WHERE (guild_id=? AND user_id=?)', (member.guild.id, member.id))
        # xd = xd.fetchall()
        # if xd == []:
        #     self.c.execute('INSERT INTO userconfig VALUES (?, ?, ?, ?, ?, ?)',
        #                    (member.guild.id, member.id, None, None, False, None))
        #     self.conn.commit()

    async def on_guild_join(self, guild):
        self.c.execute('INSERT  INTO servers VALUES (?, ?, ?, ?, ?, ?)',
                       (guild.id, None, None, None, None, '?,!'))
        self.conn.commit()
        self.c.execute('INSERT INTO logging VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (guild.id, 1, 1, 1, 1, 1, 1, 1, None))
        self.conn.commit()
        self.c.execute('''INSERT INTO role_config
                        VALUES (?, ?, ?, ?, ?)''',
                       (None, False, guild.id, None, True))
        self.conn.commit()
        self.c.execute('''INSERT INTO config
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (guild.id, None, None, True, None, None))
        self.conn.commit()
        for member in guild.members:
            roles = ','.join(
                [str(x.id) for x in member.roles if x.name != "@everyone"])
            self.c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (roles, member.guild.id, None, member.id, member.display_name, 0, 0, 0))
            self.conn.commit()
            # self.c.execute('''SELECT *
            #                   FROM userconfig
            #                   WHERE (user_id=? AND guild_id=?)''',
            #                 (member.id, member.guild.id))
            # userconfig = self.c.fetchall()
            # if userconfig == []:
            #     self.c.execute('''INSERT INTO userconfig VALUES (?, ?, ?, ?, ?, ?)''',
            #     (member.guild.id, member.id, None, None, False, None))
            #     self.conn.commit()

    async def on_message(self, message):
        if message.guild is None:
            return
        if message.guild.id in (207943928018632705, 113103747126747136):
            if message.guild.id == 207943928018632705 and random.randint(1, 10000) == 1:
                legendaryRole = discord.utils.get(
                    message.guild.roles, name='Legendary')
                await message.author.add_roles(legendaryRole)
                await message.channel.send("{} just received a legendary item: **{}**".format(message.author.mention,
                                                                                              random.choice(
                                                                                                  legendaries)))

            elif message.guild.id == 113103747126747136 and random.randint(1, 25000) == 1:
                await message.channel.send("{} just received a legendary item: **{}**".format(message.author.mention,
                                                                                              random.choice(
                                                                                                  legendaries)))
        if (random.randint(1, 5000) == 1 and message.channel.id == 251064728795873281):
            quality = random.randint(1, 6)
            legendaryRole = discord.utils.get(
                message.guild.roles, name='Unique')
            await message.author.add_roles(legendaryRole)
            await message.channel.send(
                "{} You found a unique, exile. It's a **{}l {}**".format(message.author.mention, quality,
                                                                         random.choice(uniques)))

        self.fix_postcount(message)
        if message.content == "":
            return
        self.c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (message.created_at.timestamp(), message.created_at.strftime(
                           dt_format), message.clean_content, message.id, message.author.id, message.channel.id,
                        message.guild.id))
        self.conn.commit()


def setup(bot):
    bot.add_cog(StatTrak(bot))