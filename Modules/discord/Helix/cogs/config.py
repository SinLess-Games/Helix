from datetime import datetime

import discord
from discord.errors import Forbidden
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import ServConfig


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


class config(commands.Cog):
    """
    Tasks for backend of bot, No commands for Users.
    """

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

        self.exit_signal = None
        self.init_ok = False
        self.cached_app_info = None
        self.last_status = None

        # SqlAlchemy engine construction
        self.sql_engine = create_engine(
            f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}', echo=False)
        if not database_exists(self.sql_engine.url):
            create_database(self.sql_engine.url)
        else:
            # If DB exists prints database_exists
            # print(database_exists(self.sql_engine.url))
            pass

    @commands.command(name="Configure", alias="config")
    async def configure(self, ctx):
        """
        Configure the server settings for Helix
        """
        print(ctx.guild.id)

        Update_date = datetime.today()
        Ignored_channels = []
        Auto_roles = []
        conf = ServConfig()
        host = self.config.sql_host
        user = self.config.sql_user
        passwd = self.config.sql_passwd
        db = ctx.guild.id
        Engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{db}', echo=False)

        if ctx.author == ctx.guild.owner:  # checks if author is the owner
            global msg, Welcome_message, Leave_message, Welcome_channel_id
            # Welcome message
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(name="Step 1", value="Please enter your Welcome Message.")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            if msg.author == 920604818496684062:
                msg = await self.client.wait_for('message')
            else:
                print("MESSAGE: " + str(msg.content))
                Welcome_message = str(msg.content)

            # Leave Message
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(name="Step 2", value="Please enter your Leave Message.")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            if msg.author == 920604818496684062:
                msg = await self.client.wait_for('message')
            else:
                print("MESSAGE: " + str(msg.content))
                Leave_message = str(msg.content)

            # Welcome Channel
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(name="Step 3",
                        value="Please enter your Welcome Channel id. All you need to do is mention the channel.")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            if msg.author == 920604818496684062:
                msg = await self.client.wait_for('message')
            else:
                channel = msg.channel_mentions
                Welcome_channel_id = channel.id
                print(Welcome_channel_id)

            # Ignored Channels
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(
                name="Step 5",
                value="Please enter the channels you want Helix to ignore. All you need to do is mention the channels.")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            if msg.author == 920604818496684062:
                msg = await self.client.wait_for('message')
            else:
                channel = msg.channel_mentions
                Ignored_channels.append(channel.id)
                print(Ignored_channels)

            # Auto Roles
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(
                name="Step 6",
                value="Please enter the roles you want auto assigned to new users when they join. All you need to do is mention the roles.")
            await send_embed(ctx, e)
            msg = await self.client.wait_for('message')
            if msg.author == 920604818496684062:
                msg = await self.client.wait_for('message')
            else:
                Auto_roles.append(msg.role_mentions.role.id)
                print(Auto_roles)

            # White Listed Members ( Coming Soon )

            # Database entries
            with Session(Engine) as session:

                conf.Welcome_message = Welcome_message
                conf.Leave_message = Leave_message
                conf.WelcomeChannelID = Welcome_channel_id
                conf.IgnoredChannels = Ignored_channels
                conf.AutoRoles = Auto_roles

                conf.LastUpdate = Update_date
                session.add(conf)
                session.commit()
                session.close()
        else:
            e = discord.Embed()
            e.set_footer(text='SinLess-Games/Helix ({})'.format(self.config.version),
                         icon_url='https://imgur.com/a/wdNvSfZ')
            e.set_author(name=self.client.user.name, url='https://github.com/sinLess-Games/Helix',
                         icon_url=self.client.user.avatar_url)

            e.add_field(
                value="You are not the server owner, you must be the server owner to configure these settings.")
            await send_embed(ctx, e)


def setup(client):
    client.add_cog(config(client))
