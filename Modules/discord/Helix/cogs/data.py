import discord
from discord.errors import Forbidden
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import Model


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


def check(content):
    def inner_check(message):
        return message.content == content

    return inner_check


class Data(commands.Cog):

    def __init__(self, client, config_file=None):
        if config_file is None:
            config_file = ConfigDefaults.Config_file

        self.config = Config(config_file)
        self.client = client

        self.VERSION = self.config.version
        self.OWNER_ID = self.config.owner_id
        self.prefix = self.config.prefix
        self.sql_host = self.config.sql_host
        self.sql_user = self.config.sql_user
        self.sql_passwd = self.config.sql_passwd
        self.sql_ddb = self.config.sql_ddb

        self.sql_engine = create_engine(
            f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}', echo=False)
        if not database_exists(self.sql_engine.url):
            create_database(self.sql_engine.url)
        else:
            # If DB exists prints database_exists
            # print(database_exists(self.sql_engine.url))
            pass

    @commands.command(name="add-data")
    async def add_data(self, ctx):
        """
        Add data to model database
        """
        print(ctx.author.id)
        if ctx.author is self.client:
            print("bot response detected.")
            pass
        elif ctx.author.id == 241693350711787522:
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(name="Data Table", value="Please enter the category Tag for the data Table")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            Tag = msg.content
            print(Tag)

            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(name="Data Table", value="Please enter the Word for the data Table")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            Word = msg.content
            print(Word)

            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)
            e.add_field(name="Data Table", value=f"Please enter the Response to '{Word}' for the data Table")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            Response = msg.content
            print(Response)

            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)
            e.add_field(
                name="Data Table",
                value=f"Please enter the Context for '{Word}', for the data Table. If no context reply with None")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            Context = msg.content
            print(Context)

            m = Model()
            with Session(self.sql_engine) as session:
                data_exists = session.query(Model).filter_by(Word=Word).first()
                if data_exists:
                    e = discord.Embed()
                    e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                                 icon_url='https://imgur.com/a/wdNvSfZ')
                    e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                                 icon_url=self.client.user.avatar_url)
                    e.add_field(
                        name="Data Table", value=f"{Word} Already Exists in the Model Table.")
                    await send_embed(ctx, e)
                else:
                    m.Tag = Tag
                    m.Word = Word
                    m.Response = Response
                    m.context = Context

                    session.add(m)
                    session.commit()
                    session.close()
        else:
            e = discord.Embed(title="Bot Owner Error")
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)
            e.add_field(name="Error occured", value="You are not the owner of this bot!")
            await send_embed(ctx, e)
            print("You are not the owner of this bot")


def setup(client):
    client.add_cog(Data(client))
