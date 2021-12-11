# Name Helix

import typing
from datetime import datetime
from os import listdir

import discord
import sentry_sdk
import yaml
from discord.ext import commands
from models import GuildConfig, WelcomeConfig, LeaveConfig
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from cogs.help import send_embed
from utils.db_tools import ServerList, Users, Stats, Config, BlackList, Mutes

# Sentry error reporting
sentry_sdk.init(
    "https://fe349234191e4e86a83c8cd381068ab4@o901570.ingest.sentry.io/5994911",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# Discord Intents
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.messages = True
guild_subscriptions = True
fetch_offline_members = True

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless
# having issues with ruamel)
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# sends discord logging files which could potentially be useful for catching errors.
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'

# Config Variables
TOKEN = config['Token']
VERSION = config['Version']
OWNER_NAME = config['OWNER_NAME']
OWNER_ID = config['bot_owner_id']
PREFIX = config['DefaultPrefix']
host = config['SQL_Host']
user = config['SQL_UserName']
passwd = config['SQL_Password']
db = config['DefaultDatabase']

# SqlAlchemy engine construction
engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{db}', echo=False)
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # If DB exists prints database_exists
    print(database_exists(engine.url))


async def load_extensions():
    for fn in listdir("Commands"):
        if fn.endswith(".py"):
            # print(f"loading cog {fn}")
            bot.load_extension(f"Commands.{fn[:-3]}")

    for fn in listdir("Addons"):
        if fn.endswith(".py"):
            # print(f"loading cog {fn}")
            bot.load_extension(f"Addons.{fn[:-3]}")

    for fn in listdir("cogs"):
        if fn.endswith(".py"):
            # print(f"loading cog {fn}")
            bot.load_extension(f"cogs.{fn[:-3]}")


async def get_prefix(bot: commands.Bot, message: discord.Message):
    with Session(engine) as session:
        guild = session.query(ServerList).filter_by(ServerID=message.guild.id).first()
        if not guild:
            return PREFIX
        else:
            GuildData = session.query(ServerList).filter_by(ServerID=message.guild.id).first()
            return GuildData.Prefix


bot = commands.Bot(command_prefix=get_prefix, intents=intents)

bot.remove_command('help')


@bot.event
async def on_ready():
    print("Connected to db")
    print("Loading extensions")

    await load_extensions()

    print("Extensions Loaded")
    print(f'\033[1;32m Bot is ready! DEUS VULT!')

    config_activity = config['bot_activity']
    activity = discord.Game(name=config['bot_status_text'])

    await bot.change_presence(status=config_activity, activity=activity)

    async for guild in bot.fetch_guilds():

        memberList = []
        channelList = await guild.fetch_channels()
        async for member in guild.fetch_members():
            memberList.append(member)
        members = len(memberList)
        # print("members: " + str(members))
        channels = len(channelList)
        # print("channels: " + str(channels))

        ServerList.__table__.create(bind=engine, checkfirst=True)

        # create server specific databases
        with Session(engine) as session:
            serv = ServerList()

            GuildExists = session.query(ServerList).filter_by(ServerID=guild.id).first()
            if not GuildExists:
                serv.ServerID = guild.id
                serv.ServerName = guild.name
                serv.MemberCount = members
                serv.ChannelCount = channels
                serv.LastUpdate = datetime.now()
                session.add(serv)
                session.commit()
                session.close()

            else:
                session.query(ServerList).filter_by(ServerID=guild.id).update({
                    "ServerName": guild.id,
                    "MemberCount": members,
                    "ChannelCount": channels,
                    "LastUpdate": datetime.now()
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    async for guild in bot.fetch_guilds():
        Engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{guild.id}', echo=False)
        if not database_exists(Engine.url):
            create_database(Engine.url)
        else:
            # If DB exists prints database_exists
            print(database_exists(Engine.url))

        usr = Users()
        sts = Stats()
        cfg = Config()
        bl = BlackList()
        mut = Mutes()

        Users.__table__.create(bind=Engine, checkfirst=True)
        Stats.__table__.create(bind=Engine, checkfirst=True)
        Config.__table__.create(bind=Engine, checkfirst=True)
        BlackList.__table__.create(bind=Engine, checkfirst=True)
        Mutes.__table__.create(bind=Engine, checkfirst=True)

        with Session(Engine) as session:
            pass


@bot.command()
@commands.has_guild_permissions(manage_guild=True)
async def prefix(ctx: commands.Context, *, _prefix: typing.Optional[str] = None):
    """
    Sets the Prefix for you server
    """

    with Session(engine) as session:
        GuildData = session.query(ServerList).filter_by(ServerID=ctx.guild.id).first()

    if not _prefix:
        return await ctx.send(f"The current Prefix for this server is {GuildData.Prefix if GuildData else PREFIX}")

    else:
        GuildData.Prefix = _prefix
        with Session(engine) as session:
            session.query(ServerList).filter_by(ServerID=ctx.guild.id).update({
                "Prefix": _prefix,
                "LastUpdate": datetime.now()
            }, synchronize_session="fetch")
            session.commit()
            session.close()
    return await ctx.send(f"set the prefix for this server to '{_prefix}'")


@bot.event
async def on_guild_join(guild: discord.Guild):
    new_config = GuildConfig(ID=guild.id)
    await new_config.save()


@bot.event
async def on_member_join(member: discord.Member):
    welcome_config = await WelcomeConfig.filter(ID=member.guild.id).get_or_none()
    config1 = await GuildConfig.filter(ID=member.guild.id).get_or_none()
    if not config:
        return

    if config.welcome_enabled:
        # welcome messages are enabled
        emb = discord.Embed(title='Welcome', color=discord.Color.dark_gold())
        emb.set_image(url=member.avatar_url, inline=True)
        emb.description(welcome_config.message.format(member.mention), inline=True)

        send_channel = discord.utils.get(member.guild.channels, id=welcome_config.channel_id)
        await send_channel.send(embed=emb)


@bot.event
async def on_member_leave(member: discord.Member):
    leave_config = await LeaveConfig.filter(ID=member.guild.id).get_or_none()
    config1 = await GuildConfig.filter(ID=member.guild.id).get_or_none()
    if not config1:
        return

    if config1.leave_enabled:
        # welcome messages are enabled
        emb = discord.Embed(title='Welcome', color=discord.Color.dark_gold())
        emb.set_image(url=member.avatar_url, inline=True)
        emb.description(leave_config.message.format(member.mention), inline=True)

        send_channel = discord.utils.get(member.guild.channels, id=leave_config.channel_id)
        await send_channel.send(embed=emb)


@bot.command()
@commands.has_guild_permissions(manage_guild=True)
async def welcome(ctx: commands.Context):
    """
    Not for use utility
    """
    config1 = await GuildConfig.filter(ID=ctx.guild.id).get_or_none()
    welcome_config = await WelcomeConfig.filter(ID=ctx.guild.id).get_or_none()

    if config1.welcome_enabled:
        welcome_channel = discord.utils.get(ctx.channels, id=welcome_config.channel_id)
        return await ctx.send(
            f"welcome messages are ***enabled*** in this guild. All member join events will be sent to {welcome_channel.mention}")
    else:
        return await ctx.send(f"Welcome messages are not enabled for {ctx.guild.name}. To enable please")


@bot.command()
@commands.has_guild_permissions(manage_guild=True)
async def SetWelcome(ctx: commands.Context):
    """
    Allows you to configure the welcome message for your server
    """

    async def ask_welcome_message():
        try:
            msg: discord.Message = await bot.wait_for(
                "message", check=lambda x: x.author.id == ctx.author.id,
                timeout=20
            )
            return commands.TextChannelConverter().convert(ctx, msg.content)

        except commands.errors.ChannelNotFound as e:
            await ctx.send(f"Invaild Channel '{e.argument}'. Please enter a channel name again.")
            return await ask_welcome_message()

    await ctx.send("Please enter the channel where all welcome messages will be sent.")
    channel = await ask_welcome_message()

    emb = discord.Embed(title='Welcome Messages', color=discord.Color.dark_gold(),
                        description="Please send your welcome message Below. Use '{}' where you want to mention the user."
                                    f':smiley:\n')

    await send_embed(ctx, emb)

    welcome_msg = (await bot.wait_for(
        "message", check=lambda x: x.author.id == ctx.author.id,
        timeout=20
    )).content

    config1 = await GuildConfig.filter(ID=ctx.guild.id).get_or_none()
    welcome_config = await WelcomeConfig.filter(ID=ctx.guild.id).get_or_none()

    config1.welcome_enabled = True
    await config1.save()

    if not welcome_config:
        new_welcome_config = WelcomeConfig(ID=ctx.guild.id, channel_id=channel.id, message=welcome_msg)
        await new_welcome_config.save()
        emb = discord.Embed(title='Welcome Messages', color=discord.Color.dark_gold(),
                            description=f'A new config was generated for your server. '
                                        f'You Have enabled welcome Messages.'
                                        f'All Member join events will be sent to {channel.metion}'
                                        f':smiley:\n')
        await send_embed(ctx, emb)
    else:
        welcome_config.channel_id = channel.id
        welcome_config.message = welcome_msg
        await welcome_config.save()
        emb = discord.Embed(title='Welcome Messages', color=discord.Color.dark_gold(),
                            description=f'You Have Updated W elcome Config.'
                                        f'All Member join events will be sent to {channel.metion}'
                                        f':smiley:\n')
        await send_embed(ctx, emb)


@bot.command()
@commands.has_guild_permissions(manage_guild=True)
async def leave(ctx: commands.Context):
    """
    Not for use utility
    """
    welcome_config = await WelcomeConfig.filter(ID=ctx.guild.id).get_or_none()
    config1 = await GuildConfig.filter(ID=ctx.guild.id).get_or_none()
    leave_config = await LeaveConfig.filter(ID=ctx.guild.id).get_or_none()
    welcome_channel = welcome_config.channel_id

    if config1.leave_enabled:
        leave_channel = discord.utils.get(ctx.channels, id=leave_config.channel_id)
        return await ctx.send(
            f"welcome messages are ***enabled*** in this guild. All member join events will be sent to {welcome_channel.mention}")
    else:
        return await ctx.send(f"Welcome messages are not enabled for {ctx.guild.name}. To enable please")


@bot.command()
@commands.has_guild_permissions(manage_guild=True)
async def setleave(ctx: commands.Context):
    """
    allows you to set the Leave message for your server
    """

    async def ask_leave_message():
        try:
            msg: discord.Message = await bot.wait_for(
                "message", check=lambda x: x.authour.id == ctx.author.id,
                timeout=20
            )
            return commands.TextChannelConverter().convert(ctx, msg.content)

        except commands.errors.ChannelNotFound as e:
            await ctx.send(f"Invaild Channel '{e.argument}'. Please enter a channel name again.")
            return await ask_leave_message()

    await ctx.send("Please enter the channel where all welcome messages will be sent.")
    channel = await ask_leave_message()

    emb = discord.Embed(title='Leave Messages', color=discord.Color.dark_gold(),
                        description="Please send your Leave message Below. Use '{}' where you want to mention the user."
                                    f':smiley:\n')

    await send_embed(ctx, emb)

    welcome_msg = (await bot.wait_for(
        "message", check=lambda x: x.authour.id == ctx.author.id,
        timeout=20
    )).content

    config1 = await GuildConfig.filter(ID=ctx.guild.id).get_or_none()
    leave_config = await LeaveConfig.filter(ID=ctx.guild.id).get_or_none()

    config1.welcome_enabled = True
    await config1.save()

    if not leave_config:
        new_leave_config = LeaveConfig(ID=ctx.guild.id, channel_id=channel.id, message=welcome_msg)
        await new_leave_config.save()
        emb = discord.Embed(title='Leave Messages', color=discord.Color.dark_gold(),
                            description=f'A new config was generated for your server. '
                                        f'You Have enabled Leave Messages.'
                                        f'All Member Leave events will be sent to {channel.metion}'
                                        f':smiley:\n')
        await send_embed(ctx, emb)
    else:
        leave_config.channel_id = channel.id
        leave_config.message = welcome_msg
        await leave_config.save()
        emb = discord.Embed(title='Leave Messages', color=discord.Color.dark_gold(),
                            description=f'You Have Updated Leave Config.'
                                        f'All Member leave events will be sent to {channel.metion}'
                                        f':smiley:\n')
        await send_embed(ctx, emb)


bot.run(TOKEN)
